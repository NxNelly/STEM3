import easygopigo3 as easy
import picamera
import numpy as np
import time

# initialize
gpg = easy.EasyGoPiGo3()
gpg.set_speed(160)

dist_sensor = gpg.init_distance_sensor()
print("dist_sensor ",dist_sensor)

# camera setup
output = np.empty((480, 640, 3), dtype=np.uint8)

# safety distance
MIN_DIST_CM = 12

# THIS FUNCTION WAS FULLY WRITTEN BY AI (based on a working but slow self written one)
def rgb_image_to_hsv(img):
    # img: (H, W, 3) in [0..255], RGB
    img = img.astype(np.float32) / 255.0

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    maxc = np.max(img, axis=2)
    minc = np.min(img, axis=2)
    delta = maxc - minc

    # H
    h = np.zeros_like(maxc)

    # Vermeide Division durch 0
    mask = delta != 0

    r_is_max = (maxc == r) & mask
    g_is_max = (maxc == g) & mask
    b_is_max = (maxc == b) & mask

    h[r_is_max] = ((g[r_is_max] - b[r_is_max]) / delta[r_is_max]) % 6
    h[g_is_max] = ((b[g_is_max] - r[g_is_max]) / delta[g_is_max]) + 2
    h[b_is_max] = ((r[b_is_max] - g[b_is_max]) / delta[b_is_max]) + 4

    h = h * 60.0  # in Grad 0..360

    # S
    s = np.zeros_like(maxc)
    nonzero = maxc != 0
    s[nonzero] = delta[nonzero] / maxc[nonzero]

    # V
    v = maxc

    return h, s, v

def lookForColor(img, color):
    # downscale image
    small = img[::4, ::4, :]

    h, s, v = rgb_image_to_hsv(small)

    # HSV-Thresholds
    # for whatever reason the python match expression didn't work in the gopigo notebook editor for us
    if color == "green": #technically not needed as of now
        mask = (h >= 75) & (h < 155) & (s > 0.3) & (v > 0.2)

    elif color == "red":
        mask = ((h < 10) | (h >= 345)) & (s > 0.5) & (v > 0.5)

    elif color == "blue":
        mask = (h >= 145) & (h < 240) & (s > 0.3) & (v > 0.2)
        
    elif color == "purple":
        mask = (h >= 255) & (h < 290) & (s > 0.3) & (v > 0.2)
    else:
        return 0

    #amount of fitting pixels
    count = np.count_nonzero(mask)

    return count if count >= 100 else 0


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
            # greenAmount = lookForColor(output,"green")
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
                    # close object with no color detected, in our case: there is probably a color to recognize that is not recognized
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








# putting our own rgb to hsv function here because i feel bad about using the ai one
def rgbToHsv(r,g,b):
    #get value between 0 and 1
    r=r/255
    g=g/255
    b=b/255

    max=0
    min=0
    def getDelta(max,min):
        return max-min
    
    #functions for all max cases
    def rMax(r,g,b):
        if g>b:
            min=b
        else:
            min=g
        h=60*(((g-b)/getDelta(r,min))%6)
        return h, min
    
    def gMax(r,g,b):
        if r>b:
            min=b
        else:
            min=r
        h=60*((b-r)/getDelta(g,min)+2)
        return h,min
    
    def bMax(r,g,b):
        if r>g:
            min=g
        else:
            min=r
        h=60*((r-g)/getDelta(b,min)+4)
        return h,min
    
    #hue
    h=0
    if (r==b and r==g):
        max,min=r
        h=0
    elif (r>g and r>b):
        max=r
        h,min=rMax(r,g,b)
    elif (g>r and g>b):
        max=g
        h,min=gMax(r,g,b)
    else:
        max=b
        h,min=bMax(r,g,b)

    #saturation
    s=0
    if not(max==0):
        s=(max-min)/max

    #value
    v=max

    return h,s,v
