# Camera Calibration

This code is relative to the second assignment on the course. It should calibrate the camera using the chessboard pictures. In summary, it should return the relationships between the actual coordinates in 3D and the picture coordinates in 2D.

The code uses OpenCV to generate the camera intrinsic parameters and  distortion coefficients, along the rotation/translation parameters for each picture.

Those parameters are used to compute the rotation matrix and projection matrix for each picture.

## Usage

Just run the code. It will print the camera parameters, and extrinsic parameters for each picture.

## Requirements

This code uses Python 3, NumPy and OpenCV (built on 4.5.1)

```
python3 calibrate.py
```