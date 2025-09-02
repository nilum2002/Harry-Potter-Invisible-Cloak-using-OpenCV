import cv2 
import numpy as np 
import time 


# get the camera feed 
capture_video = cv2.VideoCapture(0)

cv2.namedWindow("Invisible Cloak", cv2.WINDOW_NORMAL)
# give time to worm up the camera
time.sleep(1)

background = None
selected_hsv = None

# capture the background in 60
for i in range(60):
    # return val gives a boolean vale wether the video captured or not 
    return_val , background = capture_video.read()
    if return_val == False:
        continue
background = np.flip(background, axis =1) # flip of the frame 


if not capture_video.isOpened():
    print("Error in Web Cam")
    exit()

print("Press Q for exit ")


def capture_color(event , x, y, flags , parm):
    
    global selected_hsv

    if event == cv2.EVENT_LBUTTONDOWN:
        b, g,r = frame[y, x] # get bgr values

        # convert to ths HSV format
        hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)
        selected_hsv = hsv[0][0]
        

# read the display frames
while (capture_video.isOpened()):
    return_val, frame = capture_video.read()
    if not return_val:
        break

    cv2.imshow("Invisible Cloak", frame)
    # capture the color
    cv2.setMouseCallback("Invisible Cloak", capture_color)
    # colors = np.flip(colors, axis= 1)
    print(selected_hsv)
    # exit for q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




capture_video.release()
cv2.destroyAllWindows()