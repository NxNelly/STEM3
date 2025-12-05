# STEM3 Project

## Making a GoPiGo Robot navigate a labyrinth through colors
- camera
- distance sensor
  
**Reacting to:**

- Red: stop moving
- Blue: turn left
- Purple: turn right

Not yet implemented:

- combination of color: turn around
- white: speed up

Watch Herbie drive [here](https://drive.google.com/file/d/1tTPGwo-7tFivDUDQQjQeDab6EtDQBzbJ/view?usp=drive_link), and see their point of view [here](https://drive.google.com/file/d/1n7Z22nHQU-6b_2p118t-VAgT7UZXwiAB/view?usp=drive_link)

![Labyrinth](https://github.com/NxNelly/STEM3/blob/main/Labyrinth.jpeg)

### Code

![Full code here](/herbie.py)

```
#main logic
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        time.sleep(2)  

        while True:
            # measure distance
            distance = 1e18
            if dist_sensor:
                distance = dist_sensor.read()  

            # capture image
            camera.capture(output, format='rgb', use_video_port=True)

            # check colors
            redAmount=lookForColor(output,"red")
            purpleAmount=lookForColor(output,"purple")
            blueAmount=lookForColor(output,"blue")
            

            # main main logic

            if distance<MIN_DIST_CM:
                # distance related colors:
                if purpleAmount>0:
                    # turn left 
                    print("purple")
                    gpg.turn_degrees(-90)
                    time.sleep(0.3)
                    gpg.forward()
                        

                elif blueAmount>0:
                    # turn right
                    print("blue")
                    gpg.turn_degrees(90)
                    time.sleep(0.3)
                    gpg.forward()
                
                else:
                    # close object with no color detected
                    print("no color spotted, turn softly")
                    gpg.turn_degrees(30)
                    time.sleep(0.3)
                    gpg.forward()

            # non distance related
            else:
                if redAmount>0:
                    #stop
                    print("red - stop")
                    gpg.stop()

                else:
                    gpg.forward()

            time.sleep(0.1)

except KeyboardInterrupt:
    print("terminate program")

finally:
    gpg.stop()
```


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
