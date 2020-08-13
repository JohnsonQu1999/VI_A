const int KEY_0 = 2, KEY_1 = 3, KEY_2 = 4, KEY_3 = 5;
const int SW_0 = 6, SW_1 = 7, SW_2 = 8, SW_3 = 9, SW_4 = 10, SW_5 = 11, SW_6 = 12, SW_7 = 13;
int inByte;

void setup() {
  Serial.begin(9600);

  for (int a = 2; a <= 13; a++) {   //Setting pins as outputs
    pinMode(a, OUTPUT);
  }

  Serial.println("Initialized.");
}

void loop() {
  if(Serial.available() > 0){
    inByte = Serial.read();

    switch(inByte){
      case '!':
        pressKey(KEY_0);
        break;
      case '"':
        unPressKey(KEY_0);
        break;
      case '#':
        pressKey(KEY_1);
        break;
      case '$':
        unPressKey(KEY_1);
        break;
      case '%':
        pressKey(KEY_2);
        break;
      case '&':
        unPressKey(KEY_2);
        break;
      case '\'':
        pressKey(KEY_3);
        break;
      case '(':
        unPressKey(KEY_3);
        break;
      //==============================//
      case ')':
        flipSwitch(SW_0);
        break;
      case '*':
        flopSwitch(SW_0);
        break;
      case '+':
        flipSwitch(SW_1);
        break;
      case ',':
        flopSwitch(SW_1);
        break;
      case '-':
        flipSwitch(SW_2);
        break;
      case '.':
        flopSwitch(SW_2);
        break;
      case '/':
        flipSwitch(SW_3);
        break;
      case '0':
        flopSwitch(SW_3);
        break;
      case '1':
        flipSwitch(SW_4);
        break;
      case '2':
        flopSwitch(SW_4);
        break;
      case '3':
        flipSwitch(SW_5);
        break;
      case '4':
        flopSwitch(SW_5);
        break;
      case '5':
        flipSwitch(SW_6);
        break;
      case '6':
        flopSwitch(SW_6);
        break;
      case '7':
        flipSwitch(SW_7);
        break;
      case '8':
        flopSwitch(SW_7);
        break;
      case '\n':
        Serial.println("Discarded new line character");
        break;
      default:
        Serial.println("An unspecified character was received.");
        Serial.println(inByte);
    }
  }
}

void pressKey(const int key) {
  digitalWrite(key, LOW);
}

void unPressKey(const int key) {
  digitalWrite(key, HIGH);
}

void flipSwitch(const int sw) {
  digitalWrite(sw, HIGH);
}

void flopSwitch(const int sw) {
  digitalWrite(sw, LOW);
}

void cycleKeys() {
  pressKey(KEY_0);
  delay(1000);
  unPressKey(KEY_0);
  pressKey(KEY_1);
  delay(1000);
  unPressKey(KEY_1);
  pressKey(KEY_2);
  delay(1000);
  unPressKey(KEY_2);
  pressKey(KEY_3);
  delay(1000);
  unPressKey(KEY_3);
}

void cycleSwtiches() {
  flipSwitch(SW_0);
  delay(1000);
  flopSwitch(SW_0);
  flipSwitch(SW_1);
  delay(1000);
  flopSwitch(SW_1);
  flipSwitch(SW_2);
  delay(1000);
  flopSwitch(SW_2);
  flipSwitch(SW_3);
  delay(1000);
  flopSwitch(SW_3);
  flipSwitch(SW_4);
  delay(1000);
  flopSwitch(SW_4);
  flipSwitch(SW_5);
  delay(1000);
  flopSwitch(SW_5);
  flipSwitch(SW_6);
  delay(1000);
  flopSwitch(SW_6);
  flipSwitch(SW_7);
  delay(1000);
  flopSwitch(SW_7);
}

//void start() {
//  //The starting sequence of the robot
//  //Turn to the left, then go forwards, then stop
//  //Notes about the 5 second delay: if we leave the code as is, 5 seconds start counting down from when you plug in the power supply
//  //Or, you we can put a button and wait for a button push.
//  //Methods used: left(), forward(), off()
//
//  while (!digitalRead(startButton)) {
//  }
//
//  delay(5000);
//
//  right();
//  delay(150);
//  forward();
//  delay(1000);
//  off();
//}
//
//void activeSearch() {
//  //Looks for the other robot by turning in a circle until the enemy is detected
//  //Methods used: right(), getDist(), off()
//  left();
//
//  while (getDist() > criticalDist) {
//  }
//
//  off();
//}
//
//void randomSearch() {
//  //The robot keeps going forwards until it hits the edge of the ring, afterwhich it turns around a certain amount and continues to go forwards
//  //This continues to iterate until the enemy is detected
//  //Methods used: forward(), getDist(), checkQRD(), off()
//  forward();
//
//  while (getDist() > criticalDist) {
//    checkQRD();
//  }
//
//  off();
//}
//
//void checkQRD() {
//  //Defines appropriate reactions to 8 different combinations of Sumobot position
//  //Robot position is defined by the combination of QRDs that are indicating they are on the ring
//  //Methods used: qrd(), forward(), back(), left(), right()
//  if (qrd(qrd0) || qrd(qrd1) || qrd(qrd2) || qrd(qrd3)) {
//    if (qrd(qrd0) && qrd(qrd1)) {
//      back();
//      delay(100);       //set an appropriate delay for it to back up enough
//      left();
//      delay(1000);      //set an appropriate delay for it to turn 120°
//      forward();
//    }
//    else if (qrd(qrd1) && qrd(qrd2)) {
//      left();
//      delay(300);       //set an appropriate delay for the robot to turn 90°
//      forward();
//    }
//    else if (qrd(qrd2) && qrd(qrd3)) {
//      forward();
//    }
//    else if (qrd(qrd3) && qrd(qrd0)) {
//      right();
//      delay(300);       //set an appropriate delay for the robot to turn 90°
//      forward();
//    }
//    else if (qrd(qrd0)) { //120° will be adequate for the following I think
//      right();
//      delay(450);       //set an appropriate delay for the robot to turn 120°
//      forward();
//    }
//    else if (qrd(qrd1)) {
//      right();
//      delay(450);       //set an appropriate delay for the robot to turn 120°
//      forward();
//    }
//    else if (qrd(qrd2)) {
//      forward();
//    }
//    else if (qrd(qrd3)) {
//      forward();
//    }
//  }
//}
//
//void attack() {
//  //This method is only called after either activeSearch() or randomSearch() have terminated. Those methods only terminate when the enemy bot is infront of it
//  //The robot keeps going forward as long as the robot is in front of it
//  //If the robot loses sight of the enemy, it checks left or right (see checkLeftRight() )
//  //If checkLeftRight() returns true, that means it has relocated the enemy; if it returns false, it means it can't find it.
//  //true causes the robot to keep attacking
//  //false causes the robot to leave this method
//  //Methods used: forward(), getDist(), checkLeftRight()
//  boolean keepAttacking = true;
//
//  while (keepAttacking) {
//    forward();
//    if (getDist() > criticalDist && confirmNoEnemy()) {
//      Serial.println("checking");
//      keepAttacking = checkRightLeft();
//    }
//  }
//}
//
//boolean confirmNoEnemy() {
//  int counter = 0;      //Counts how many times getDist() > criticalDist
//
//  for (int a = 0; a < 10; a++) {
//    if (getDist() > criticalDist) {
//      counter++;
//      Serial.println("checking 10 times");
//    }
//  }
//
//  if (counter >= 8) {
//    Serial.println(counter);
//    return true;
//  }
//  return false;
//}
//
//boolean checkRightLeft() {
//  //Turns to the left in 10° increments, checking for the enemy with each increment. After turning a full 40° it turns 80° to the right
//  //If the enemy is found the robot stops moving and indicates that it has found it by returning true
//  //If not it indicates it cannot find the enemy and returns false
//  //Methods used: getDist(), left(), off(), right()
//  for (int a = 0; a < 4; a++) {   //set an appropriate delay so it turns left 40° in total
//    right();
//    delay(100);                   //set an appropriate delay so it turns left 10° each time
//    off();
//    Serial.println("check right");
//    Serial.println(getDist());
//    if (getDist() < criticalDist) {
//      return true;
//    }
//  }
//
//  for (int a = 0; a < 8; a++) {   //set an appropriate delay so it turns right 80° in total
//    left();
//    delay(100);                   //set an appropriate delay so it turns right 10° each time
//    off();
//    Serial.println("check left");
//    Serial.println(getDist());
//    if (getDist() < criticalDist) {
//      return true;
//    }
//  }
//  return false;
//}
//
//void evade() {
//  //This method is only called when the attack() method terminates, meaning it cannot not find the enemy.
//  //This just assumes the enemy is coming from the side, so it backs up a little bit then turns to the side
//  //Methods used: back(), qrd(), right(), off()
//
//  float startTime = millis();
//  float endTime = millis();
//
////  Serial.println(endTime);
//
//  while (endTime - startTime < 300) {    //checking to see how long the robot has been reversing for. Only stop this sequence once it reverses an appropriate time. Maybe 1000ms?
//    Serial.println(endTime);
//    back();
//    //    if (qrd(qrd0) || qrd(qrd1) || qrd(qrd2) || qrd(qrd3)) {
//    //      break;
//    //    }
//    endTime = millis();
//  }
//  right();
//  delay(300);         //set an appropriate delay so it turns right enough
//  off();
//}
//
////=== MAJOR methods ABOVE ===//
//
////=== Motor methods BELOW ===//
////General comments for all motor methods follow below:
////If the robot does not exhibit the expected behaviour, simply change the wiring
//
//void forward() {
//  //Makes the robot go forwards
//  digitalWrite(mLeftBack, HIGH);
//  digitalWrite(mLeftFor, LOW);
//  digitalWrite(mRightBack, HIGH);
//  digitalWrite(mRightFor, LOW);
//}
//
//void back() {
//  //Makes the robot go backwards
//  digitalWrite(mLeftFor, HIGH);
//  digitalWrite(mLeftBack, LOW);
//  digitalWrite(mRightFor, HIGH);
//  digitalWrite(mRightBack, LOW);
//}
//
//void left() {
//  //Makes the robot pivot left
//  //The right motor goes forwards and the left motor goes backwards
//  digitalWrite(mLeftFor, HIGH);
//  digitalWrite(mLeftBack, LOW);
//  digitalWrite(mRightBack, HIGH);
//  digitalWrite(mRightFor, LOW);
//}
//
//void right() {
//  //Makes the robot pivot right
//  //The left motor goes forwards and the right motor goes backwards
//  digitalWrite(mLeftBack, HIGH);
//  digitalWrite(mLeftFor, LOW);
//  digitalWrite(mRightFor, HIGH);
//  digitalWrite(mRightBack, LOW);
//}
//
//void off() {
//  //Stops the robot
//  //It could be HIGH or LOW. Both combinations BRAKE the motors
//  digitalWrite(mLeftFor, LOW);
//  digitalWrite(mLeftBack, LOW);
//  digitalWrite(mRightFor, LOW);
//  digitalWrite(mRightBack, LOW);
//}
//
////=== Motor methods ABOVE ===//
//
////=== Ultra Sonic Sensor methods BELOW === //
//
//float getDist() {
//  //First turns off trigger to ensure a clean signal. Sends high to trigPin for 10e-6s. Turns off trigger
//  //Records the length of the pulse in e-6s; the length of the pulse represents how long it took for the signal to reach the ultrasonic sensor again
//  //pulseIn() --> times how long a pulse lasts (either HIGH or LOW, you specify) at a specified pin
//  //Performs a calculation for distance in cm and returns the distance
//  digitalWrite(trigPin, LOW);
//  delayMicroseconds(2);
//  digitalWrite(trigPin, HIGH);
//  delayMicroseconds(10);
//  digitalWrite(trigPin, LOW);
//
//  float duration = pulseIn(echoPin, HIGH);
//  float distanceCm = ((343 * duration) / 10000) / 2;
//
//  return distanceCm;
//}
//
////=== Ultra Sonic Sensor methods ABOVE === //
//
////=== QRD methods BELOW === //
//
//boolean qrd(const int pinNum) {
//  //When calling this method specify which pin you want to read
//  //Black ~4V
//  //White <1V
//  //Returns true if it detects that the QRD is above the ring
//  //Returns false if it detects that the QRD is within the ring
//  float voltage = (analogRead(pinNum) * 5) / 1023;
//  if (voltage < 1) {
//    return true;
//  }
//  return false;
//}
//
////=== QRD methods ABOVE === //
////=== Used with permission from Johnson Qu (March 24 2018) ===///
