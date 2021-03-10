import numpy as np
import cv2
     
cap = cv2.VideoCapture(0)
img = cv2.imread('bliss.png') # new background 640x480 -- webcam size

if not cap.isOpened():
    cap.open()

# Press C to capture background
while(True):
    # captures actual background
    ret, orig_back = cap.read()

    cv2.imshow('capture background', orig_back)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cv2.destroyWindow('capture background')

# converts background to grayscale and adds blur
orig_back = cv2.cvtColor(orig_back, cv2.COLOR_BGR2GRAY)
orig_back = cv2.GaussianBlur(orig_back, (21,21), 0)

while(True):
    ret, frame = cap.read()

    # converts current frame to grayscale and adds blur
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (21,21), 0)

    # calc absolute difference betweeen current frame and background frame
    diff = cv2.absdiff(blurred, orig_back)
    diff = cv2.GaussianBlur(diff, (21,21), 0)

    # apply threshold to filter the foreground/background pixels, and dilate to try fill the gaps
    ret, threshold = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    mask = cv2.dilate(threshold, None, iterations=2)

    # inverts fore/background in order to apply the mask
    inv_mask = cv2.bitwise_not(mask)

    # apply the inverted mask in the new background (bliss)
    new_bg = cv2.bitwise_and(img, img, None, inv_mask)

    # applys the mask in the current frame
    res = cv2.bitwise_and(frame, frame, None, mask)

    # adds both the "masked foreground" and "masked new background"
    merged = cv2.add(res, new_bg)

    cv2.imshow('frame', merged)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) == 27: # ESC to exit
        break


cap.release()
cv2.destroyAllWindows()