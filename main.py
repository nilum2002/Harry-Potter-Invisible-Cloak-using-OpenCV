import cv2
import numpy as np
import time

# Get the camera feed
capture_video = cv2.VideoCapture(0)
cv2.namedWindow("Invisible Cloak", cv2.WINDOW_NORMAL)

# Give time to warm up the camera
time.sleep(1)

click = 0
background = None
selected_hsv = None
hsv = None

print("Capturing background... Please move out of the frame!")

# Capture the background in 60 frames
for i in range(60):
    # return_val gives a boolean value whether the video captured or not
    return_val, background = capture_video.read()
    if return_val == False:
        continue

# Flip the background frame horizontally
background = np.flip(background, axis=1)

if not capture_video.isOpened():
    print("Error in Web Cam")
    exit()

print("Background captured!")
print("Now click on the object you want to make invisible")
print("Press Q to exit")

def capture_color(event, x, y, flags, param):
    global selected_hsv
    global click
    global hsv
    global frame
    
    if event == cv2.EVENT_LBUTTONDOWN:
        click += 1
        
        # Get BGR values at clicked position
        b, g, r = frame[y, x]
        
        # Convert to HSV format
        hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)
        selected_hsv = hsv[0][0]
        
        print(f"Color selected! HSV values: {selected_hsv}")

# Main loop to read and display frames
while capture_video.isOpened():
    return_val, frame = capture_video.read()
    if not return_val:
        break
    
    # Flip frame horizontally to match background
    frame = np.flip(frame, axis=1)
    
    # Set mouse callback for color selection
    cv2.setMouseCallback("Invisible Cloak", capture_color)
    
    if click >= 1:
        h, s, v = selected_hsv
        
        # Define tolerance for HSV range
        h_tol = 10
        s_tol = 50
        v_tol = 50
        
        # Create HSV range with proper bounds and data type
        lower_range = np.array([max(int(h) - h_tol, 0), max(int(s) - s_tol, 0), max(int(v) - v_tol, 0)], dtype=np.uint8)
        upper_range = np.array([min(int(h) + h_tol, 179), min(int(s) + s_tol, 255), min(int(v) + v_tol, 255)], dtype=np.uint8)
        
        # Convert current frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for the selected color
        mask = cv2.inRange(hsv_frame, lower_range, upper_range)
        
        # Morphological operations to clean up the mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
        
        # Create inverse mask
        mask2 = cv2.bitwise_not(mask)
        
        # Apply masks to create the invisible effect
        # Part 1: Background where the cloak is detected
        res1 = cv2.bitwise_and(background, background, mask=mask)
        # Part 2: Current frame where the cloak is not detected
        res2 = cv2.bitwise_and(frame, frame, mask=mask2)
        
        # Combine both parts
        final_output = cv2.add(res1, res2)
        
        cv2.imshow("Invisible Cloak", final_output)
    else:
        # Show normal frame before color selection
        cv2.imshow("Invisible Cloak", frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
capture_video.release()
cv2.destroyAllWindows()