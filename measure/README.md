# Measure

This code is relative to the third assignment on the course. The goal is to create an application that measures distances and sizes of objects based on the internal camera parameters (K).

It should be able to measure the size of objects, knowing the distance between the camera and the object.

It should also be able to measure the distance between the camera and the object, if the program knows the size of the object.

The first step is to calibrate the camera, using the code obtained on assignment two, and using the internal camera parameters (K) calculate the angle between two (selected by the user) rays, and use this angle and trigonometry to measure the size/distance.

### 1. Object size

Firstly, the user must select two points in the image, and the program will store the X/Y coordinates.

Then, transform this "image coordinates" on "camera coordinates" multiplying the inverse of K and X/Y on homogenous coordinates, and obtaining the rays:

```
ray₀ = K⁻¹ × [x₀ y₀ 1]
ray₁ = K⁻¹ × [x₁ y₁ 1]
```

and the _cos &theta;_ will be given by the formula:

```
cos θ = (ray₀ × ray₁) / (ray₀ᵀray₀)½ × (ray₁ᵀray₁)½
```

As × meaning "matrix product"

Having the &theta; value, it simply uses the tangent formula:

```
tan θ = opposite side / adjacent side
```

And since we already know the distance between the object and the camera (that would be the adjacent side), it's easy to know the object size.

### 2. Object distance

Using the same formulas shown above, you may change the parameters in order to obtain the distance knowing the object size.

## Usage

For the object size, you must select two points on the picture, and the size will appear on the image. The distance for the sample image is 30cm.

For the object distance, you must select two points on the picture that corresponds the "OBJ_SIZE" cm. For example, it's 14.5 on the code. If you select 0 and 14.5 on the ruler, it will show ~30cm distance from the object to the desk.

## Requirements

This code uses Python 3, NumPy and OpenCV (built on 4.5.1)

```
python3 measure.py
```