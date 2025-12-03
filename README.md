# STEM3 Project

## Making a GoPiGo Robot navigate a labyrinth through colors

**Sensors:**
- camera
- distance sensor
  
**Reacting to:**
- Red: stop moving
- Blue: turn left
- Purple: turn right
- combination of color: turn around (not jet implemented)

![Labyrinth](https://github.com/NxNelly/STEM3/blob/main/Labyrinth.jpeg)

## Street Light made with ESP32

- KY-034 LE Flash-Module
- Button with Touchpin input

![Street Light](https://github.com/NxNelly/STEM3/blob/main/Ampel.jpeg)
### Arduino Code

```
const int ledPinRed = 14;
const int ledPinGreen = 12;
bool LED_RED = true;
const int touchPin = T4;
bool touchDetected = false;

void onTouch() {
  touchDetected = true;
  Serial.println("Touch detected");
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  touchSetDefaultThreshold(15);
  touchAttachInterrupt(touchPin, onTouch, 0);

  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinGreen, OUTPUT);

  if (LED_RED) {
    digitalWrite(ledPinRed, HIGH); 
    digitalWrite(ledPinGreen, LOW);
  } else {
    digitalWrite(ledPinRed, LOW); 
    digitalWrite(ledPinGreen, HIGH);
  } 
}
void toggleLED() {
  if (LED_RED) {
    //if red is already on switch to green
    digitalWrite(ledPinRed, LOW);
    digitalWrite(ledPinGreen, HIGH);
    LED_RED = false;

  } else {
    //if red is off switch to red
    digitalWrite(ledPinRed, HIGH);
    digitalWrite(ledPinGreen, LOW);
    LED_RED = true;
  }
}

void loop() {
  if (touchDetected) {
    touchDetected = false;
    if (touchInterruptGetLastStatus(touchPin)) {
      Serial.println("Touch");
      toggleLED();
    } else {
      Serial.println("Release");
    }
  }
}
```
