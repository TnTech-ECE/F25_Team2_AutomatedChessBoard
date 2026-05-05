#include <AccelStepper.h>
#include <EEPROM.h>

// pin definitions
#define STEP_A    2
#define DIR_A     3
#define EN_A      4
#define DIAG_A    5

#define STEP_B    6
#define DIR_B     7
#define EN_B      8
#define DIAG_B    9

#define MAGNET_PIN 10

// motion constants
#define SQUARE_SIZE_MM     57.15f
#define STEPS_PER_MM       40.0f
#define STEPS_PER_SQUARE   (long)(SQUARE_SIZE_MM * STEPS_PER_MM)

// board extents (in chess squares)
#define BOARD_COLS         8
#define BOARD_ROWS         14
// valid head range (centers of edge squares are the limits)
#define X_MIN  0.5f
// 7.5
#define X_MAX  ((float)BOARD_COLS - 0.5f)
#define Y_MIN  0.5f
// 13.5
#define Y_MAX  ((float)BOARD_ROWS - 0.5f)

// EEPROM layout
#define EEPROM_MAGIC      0xAB
#define EEPROM_ADDR_MAGIC 0
// long (4 bytes)
#define EEPROM_ADDR_A     2
#define EEPROM_ADDR_B     6

// global variables
AccelStepper motorA(AccelStepper::DRIVER, STEP_A, DIR_A);
AccelStepper motorB(AccelStepper::DRIVER, STEP_B, DIR_B);

bool magnetState    = false;
bool faultOccurred  = false;
bool piReady = false;


// EEPROM help functions

void savePosition() {
  long a = motorA.currentPosition();
  long b = motorB.currentPosition();
  EEPROM.update(EEPROM_ADDR_MAGIC, EEPROM_MAGIC);
  EEPROM.put(EEPROM_ADDR_A, a);
  EEPROM.put(EEPROM_ADDR_B, b);
}

bool loadPosition() {
  if (EEPROM.read(EEPROM_ADDR_MAGIC) != EEPROM_MAGIC) return false;
  long a, b;
  EEPROM.get(EEPROM_ADDR_A, a);
  EEPROM.get(EEPROM_ADDR_B, b);
  motorA.setCurrentPosition(a);
  motorB.setCurrentPosition(b);
  return true;
}

void clearSavedPosition() {
  EEPROM.update(EEPROM_ADDR_MAGIC, 0x00);
}


// fault tolerance

bool checkFault() {
  if (digitalRead(DIAG_A) == HIGH || digitalRead(DIAG_B) == HIGH) {
    // disable drivers
    digitalWrite(EN_A, HIGH);
    digitalWrite(EN_B, HIGH);
    motorA.stop();
    motorB.stop();
    magnetOff();
    faultOccurred = true;
    // preserve where last stopped
    savePosition();
    return true;
  }
  return false;
}

void enableDrivers() {
  digitalWrite(EN_A, LOW);
  digitalWrite(EN_B, LOW);
  faultOccurred = false;
}


// magnet functions

void magnetOn() {
  digitalWrite(MAGNET_PIN, HIGH);
  magnetState = true;
}

void magnetOff() {
  digitalWrite(MAGNET_PIN, LOW);
  magnetState = false;
}


// CoreXY move (low level movement)

void moveToSteps(long a, long b) {
  if (faultOccurred) return;
  motorA.moveTo(a);
  motorB.moveTo(b);
  while (motorA.distanceToGo() != 0 || motorB.distanceToGo() != 0) {
    if (checkFault()) return;
    motorA.run();
    motorB.run();
  }
  savePosition();
}

// XY coordinate moves
// square-unit float variables to step positions

float clampX(float x) { return (x < X_MIN) ? X_MIN : (x > X_MAX) ? X_MAX : x; }
float clampY(float y) { return (y < Y_MIN) ? Y_MIN : (y > Y_MAX) ? Y_MAX : y; }

void moveToXY(float xSq, float ySq) {
  xSq = clampX(xSq);
  ySq = clampY(ySq);
  // round
  long xSteps = (long)(xSq * STEPS_PER_SQUARE + 0.5f);
  long ySteps = (long)(ySq * STEPS_PER_SQUARE + 0.5f);
  long a = xSteps + ySteps;
  long b = xSteps - ySteps;
  moveToSteps(a, b);
}

void currentXY(float &xSq, float &ySq) {
  long a = motorA.currentPosition();
  long b = motorB.currentPosition();
  xSq = (float)(a + b) / 2.0f / (float)STEPS_PER_SQUARE;
  ySq = (float)(a - b) / 2.0f / (float)STEPS_PER_SQUARE;
}

// coordinate mapping
// Pi row or column to square units
// Pi rows 1–8 (playing field)
// (Pi row 1 to physical row 4) TO (Pi row 8 to physical row 11)
// Pi row 9 (black pawn discard) = physical row 13
// Pi row 10 (black special discard) = physical row 14
// Pi row 11 (white special discard) = physical row 1
// Pi row 12 (white pawn discard) = physical row 2

float piRowToPhysY(int piRow) {
  int physRow;
  switch (piRow) {
    // white special discard
    case 11: physRow =  1; break;

    // white pawn discard
    case 12: physRow =  2; break;

    // playing field bottom
    case  1: physRow =  4; break;

    case  2: physRow =  5; break;
    case  3: physRow =  6; break;
    case  4: physRow =  7; break;
    case  5: physRow =  8; break;
    case  6: physRow =  9; break;
    case  7: physRow = 10; break;

    // playing field top
    case  8: physRow = 11; break;

    // black pawn discard
    case  9: physRow = 13; break;

    // black special discard
    case 10: physRow = 14; break;

    // fallback
    default: physRow =  1; break;
  }
  // center of current row
  return (float)physRow - 0.5f;
}

float colToPhysX(int col) {
  // col 0 = a, 7 = h
  return (float)col + 0.5f;
}


// piece movement engine
void chooseExitEdge(float cx, float cy, int dx, int dy, float &ex, float &ey) {
  int adx = abs(dx);
  int ady = abs(dy);

  if (adx == 0 && ady == 0) {
    ex = cx + 0.5f; ey = cy;
    return;
  }

  if (adx == 0) {
    if (cx + 0.5f >= (float)BOARD_COLS) {
      ex = cx - 0.5f;
    } else {
      ex = cx + 0.5f;
    }
    ey = cy;
  } else if (ady == 0) {
    ex = cx;
    if (cy + 0.5f >= (float)BOARD_ROWS) {
      ey = cy - 0.5f;
    } else {
      ey = cy + 0.5f;
    }
  } else {
    // diagonal or knight = move to corner of source square toward the destination
    ex = cx + ((dx > 0) ? 0.5f : -0.5f);
    ey = cy + ((dy > 0) ? 0.5f : -0.5f);
  }
}

void chooseEntryEdge(float cx, float cy, int dx, int dy, float &ex, float &ey) {
  int adx = abs(dx);
  int ady = abs(dy);

  if (adx == 0 && ady == 0) {
    ex = cx - 0.5f; ey = cy;
    return;
  }

  if (adx == 0) {
    if (cx + 0.5f >= (float)BOARD_COLS) {
      ex = cx - 0.5f;
    } else {
      ex = cx + 0.5f;
    }
    ey = cy;
  } else if (ady == 0) {
    ex = cx;
    if (cy + 0.5f >= (float)BOARD_ROWS) {
      ey = cy - 0.5f;
    } else {
      ey = cy + 0.5f;
    }
  } else {
    // diagonal or knight = entry point on horizontal edge "lane" at destination column's center X
    ex = cx;
    ey = cy + ((dy > 0) ? 0.5f : -0.5f);
  }
}

void straightEdgeTravel(float fromX, float fromY, float toX,   float toY) {
  moveToXY(toX, toY);
}

void diagonalStaircaseTravel(float startX, float startY,
                             int dx, int dy, int steps) {
  float x = startX;
  float y = startY;
  float stepY = (dy > 0) ? (float)steps : (float)(-steps);

  // travel full Y distance along vertical edge lane
  y += stepY;
  moveToXY(x, y);

  // travel full X distance along horizontal edge lane (entry edge X handles the final position)
}

void knightLTravel(float startX, float startY, int dx, int dy) {
  float x = startX;
  float y = startY;
  int adx = abs(dx);
  int ady = abs(dy);
  float stepX = (dx > 0) ? 1.0f : -1.0f;
  float stepY = (dy > 0) ? 1.0f : -1.0f;

  // start at exit edge (cx ± 0.5, cy) on vertical edge lane
  // travel longer leg along current edge lane, then shorter leg along horizontal edge lane (to entry edge)

  if (ady >= adx) {
    // long leg in Y (travel along vertical edge lane)
    for (int i = 0; i < ady; i++) {
      y += stepY;
      moveToXY(x, y);
    }
    // short leg in X (at (cx ± 0.5, destY) and need to reach entry edge at (destCx - 0.5, destY))
    // for dx=1 at cx+0.5 = destCx-0.5, already arrived
    // for dx=2, would need one more step (not valid knight move)
  } else {
    // long leg in X (first move to horizontal edge lane by going to (cx ± 0.5, cy ± 0.5))
    y += stepY * 0.5f;
    moveToXY(x, y);
    // travel along horizontal edge lane
    for (int i = 0; i < adx; i++) {
      x += stepX;
      moveToXY(x, y);
    }
    // short leg in Y (travel to entry edge)
    // at (destCx + 0.5, cy ± 0.5) and need to reach (destCx - 0.5, destCy) = travel along vertical edge lane (shift first)
    x -= stepX * 0.5f;
    moveToXY(x, y);
    for (int i = 0; i < ady - 1; i++) {
      y += stepY;
      moveToXY(x, y);
    }
    y += stepY * 0.5f;
    moveToXY(x, y);
  }
}


// full piece move
void movePiece(int srcCol, int srcPiRow, int dstCol, int dstPiRow) {

  // home signal: "src == dst"
  if (srcCol == dstCol && srcPiRow == dstPiRow) {
    float px = colToPhysX(srcCol);
    float py = piRowToPhysY(srcPiRow);
    magnetOff();
    moveToXY(px, py);
    return;
  }

  // convert to physical square centers
  // source center X
  float sx = colToPhysX(srcCol);
  // source center Y
  float sy = piRowToPhysY(srcPiRow);
  // destination center X
  float dx_f = colToPhysX(dstCol);
  // destination center Y
  float dy_f = piRowToPhysY(dstPiRow);

  // direction in square units
  int totalDx = (int)roundf(dx_f - sx);
  int totalDy = (int)roundf(dy_f - sy);

  int dirX = (totalDx > 0) ? 1 : (totalDx < 0) ? -1 : 0;
  int dirY = (totalDy > 0) ? 1 : (totalDy < 0) ? -1 : 0;

  // determine move type
  int adx = abs(totalDx);
  int ady = abs(totalDy);
  bool isStraight = (dirX == 0 || dirY == 0);
  bool isDiagonal = (adx == ady && adx > 0);
  bool isKnight   = ((adx == 1 && ady == 2) || (adx == 2 && ady == 1));

  // approach: (magnet OFF) move directly to edge midpoint of the source square
  // use exit edge since needs to passthrough center
  float exitX, exitY;
  chooseExitEdge(sx, sy, totalDx, totalDy, exitX, exitY);

  magnetOff();
  // direct path (magnet off)
  moveToXY(exitX, exitY);

  // move to source center
  moveToXY(sx, sy);

  // turn on magnet
  magnetOn();
  delay(200);

  // return to exit-edge midpoint (magnet on, single axis move)
  moveToXY(exitX, exitY);

  // travel to destination (magnet on, edge lanes only)

  float entryX, entryY;
  chooseEntryEdge(dx_f, dy_f, totalDx, totalDy, entryX, entryY);

  if (isStraight) {
    straightEdgeTravel(exitX, exitY, entryX, entryY);
  } else if (isDiagonal) {
    diagonalStaircaseTravel(exitX, exitY, dirX, dirY, adx);
    moveToXY(entryX, entryY);
  } else if (isKnight) {
    knightLTravel(exitX, exitY, totalDx, totalDy);
    // after L-travel, should be at entry edge of destination
    // move precisely to entry edge (in case of float drift)
    moveToXY(entryX, entryY);
  } else {
    // general case = fall back to L-shaped path
    knightLTravel(exitX, exitY, totalDx, totalDy);
    moveToXY(entryX, entryY);
  }

  // enter destination center
  moveToXY(dx_f, dy_f);

  // release magnet
  magnetOff();
  delay(200);
}


// UART command parser
// binary format is 2 bytes per comman:d
// byte 1 (source): high nibble = col (a=1...h=8), low nibble = row (1...12)
// byte 2 (dest):   same as above

// special: "src==dst" is home signal, so navigate to position (without magnet on)
// startup handshake: Pi sends 0x11 after mic ready, Arduino waits before accepting move commands
// response: 0x01 = ACK (move complete), 0x00 = NACK (parse error or fault)

void sendAck()  { Serial.write((uint8_t)0x01); }
void sendNack() { Serial.write((uint8_t)0x00); }

// main
void setup() {
  Serial.begin(115200);

  pinMode(EN_A, OUTPUT);
  pinMode(EN_B, OUTPUT);
  pinMode(MAGNET_PIN, OUTPUT);
  pinMode(DIAG_A, INPUT_PULLUP);
  pinMode(DIAG_B, INPUT_PULLUP);

  magnetOff();
  enableDrivers();

  motorA.setMaxSpeed(4000);
  motorA.setAcceleration(1500);
  motorB.setMaxSpeed(4000);
  motorB.setAcceleration(1500);

  // assume head is at physical home on startup
  clearSavedPosition();

  // home to (0,0)
  //motorA.setCurrentPosition(0);
  //motorB.setCurrentPosition(0);

  // home to (0.5,0.5)
  long xSteps = (long)(0.5f * STEPS_PER_SQUARE + 0.5f);
  long ySteps = (long)(0.5f * STEPS_PER_SQUARE + 0.5f);
  motorA.setCurrentPosition(xSteps + ySteps);
  motorB.setCurrentPosition(xSteps - ySteps);

  // flush garbage bytes from startup
  delay(500);
  while (Serial.available()) Serial.read();
}

void loop() {
  if (!piReady) {
    // wait for Pi to send 0x11 (as "ready" signal)
    while (Serial.available()) {
      if (Serial.read() == 0x11) {
        piReady = true;
        break;
      }
    }
    return;
  }



  if (Serial.available() >= 2) {
    uint8_t srcByte = Serial.read();
    uint8_t dstByte = Serial.read();

    int srcCol = ((srcByte >> 4) & 0x0F) - 1;
    int srcRow = srcByte & 0x0F;
    int dstCol = ((dstByte >> 4) & 0x0F) - 1;
    int dstRow = dstByte & 0x0F;

    if (srcCol < 0 || srcCol > 7 ||
        dstCol < 0 || dstCol > 7 ||
        srcRow < 1 || srcRow > 12 ||
        dstRow < 1 || dstRow > 12) {
      while (Serial.available()) Serial.read();
      sendNack();
      return;
    }

    if (faultOccurred) {
      enableDrivers();
    }

    movePiece(srcCol, srcRow, dstCol, dstRow);

    if (faultOccurred) {
      sendNack();
    } else {
      clearSavedPosition();
      sendAck();
    }
  }




  //if (faultOccurred) { while (1); }

  //Serial.println("Test 1: Diagonal a1 -> c3");
  //movePiece(0, 1, 2, 3);
  //delay(3000);
  
  
  /*
  Serial.println("Test 2: Knight a1 -> b3");
  movePiece(0, 1, 1, 3);
  delay(3000);
  */

  
  /*
  Serial.println("Test 3: Straight a1 -> a6");
  movePiece(0, 1, 0, 6);
  delay(3000);
  */

  /*
  Serial.println("Test 4: a11 -> c1 (L-shaped)");
  movePiece(0, 11, 2, 1);
  delay(3000);
  */
  
  //Serial.println("test done, halting");
  //while (1);
  
}
