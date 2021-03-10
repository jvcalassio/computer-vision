import numpy as np
import cv2 as cv
import glob

OBJ_DISTANCE = 30 # cm - distance from objects to the camera
OBJ_SIZE = 14.5 # cm - pen size

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('calibration/*.png')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (8,6), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#print(len(objpoints))
print("Intrinsic matrix K:\n", mtx)

click_positions_size = [] # stores clicked positions to calc size
click_positions_dist = [] # stores clicked positions to calc distance

def mouse_cb_size(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONUP:
        if(len(click_positions_size) < 2):
            cv.circle(img_1, (x,y), 5, (0,0,255), -1) # marks red dot
            click_positions_size.append((x,y))
            print((x,y))

def mouse_cb_dist(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONUP:
        if(len(click_positions_size) < 2):
            cv.circle(img_2, (x,y), 5, (0,255,0), -1) # marks green dot
            click_positions_dist.append((x,y))
            print((x,y))

orig_img = cv.imread('pic.png')

img_1 = orig_img.copy()
img_2 = orig_img.copy()

cv.namedWindow('Object size')
cv.setMouseCallback('Object size', mouse_cb_size)

cv.namedWindow('Object distance')
cv.setMouseCallback('Object distance', mouse_cb_dist)

while(1):
    cv.imshow('Object size', img_1)
    cv.imshow('Object distance', img_2)

    if(len(click_positions_size) == 2):
        x0, y0 = click_positions_size[0]
        x1, y1 = click_positions_size[1]

        Ki = np.linalg.inv(mtx) # K ^ -1
        r0 = Ki.dot([x0, y0, 1]) # d1 on hartley slides ( Ki * [x0, y0, 1] )
        r1 = Ki.dot([x1, y1, 1]) # d2 on hartley slides ( Ki * [x1, y1, 1] )

        # cos theta = (d1 * d2) / ( norm(d1) * norm(d2) )
        cos = r0.dot(r1) / (np.linalg.norm(r0) * np.linalg.norm(r1))
        angle_rad = np.arccos(cos) # theta

        print("angle: ", np.rad2deg(angle_rad), "deg") # theta (degrees)

                                                        # tan(theta/2) = (opposite/2) / adjacent
        size = np.tan( angle_rad/2 ) * OBJ_DISTANCE * 2 # opposite = tan(theta/2) * adjacent * 2
        
        print("size: ", size )

        click_positions_size = []
        img_1 = orig_img.copy()
        cv.putText(img_1, str(size) + "cm" , (150, 445), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    if(len(click_positions_dist) == 2):
        x0, y0 = click_positions_dist[0]
        x1, y1 = click_positions_dist[1]

        Ki = np.linalg.inv(mtx) # K ^ -1
        r0 = Ki.dot([x0, y0, 1]) # d1 on hartley slides ( Ki * [x0, y0, 1] )
        r1 = Ki.dot([x1, y1, 1]) # d2 on hartley slides ( Ki * [x1, y1, 1] )

        # cos theta = (d1 * d2) / ( norm(d1) * norm(d2) )
        cos = r0.dot(r1) / (np.linalg.norm(r0) * np.linalg.norm(r1))
        angle_rad = np.arccos(cos) # theta

        print("angle: ", np.rad2deg(angle_rad), "deg") # theta (degrees)

                                                    # tan(theta/2) = (opposite/2) / adjacent
        dist = (OBJ_SIZE / 2) / np.tan(angle_rad/2) # adjacent = (opposite/2) / tan(theta/2)

        print("dist:", dist)

        click_positions_dist = []
        img_2 = orig_img.copy()
        cv.putText(img_2, str(dist) + "cm" , (150, 445), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()