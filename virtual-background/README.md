# Virtual Background

This application was the first assignment on the course. The goal is to implement something similar to the virtual background functionality used on videoconference softwares.

This code uses the _background subtraction_ technique, that consists in capturing a reference image of the current background (with no actors/objects on the foreground), and then replace each similar pixel on the target image with the corresponding pixel on the new background image.

## Usage

Leave the camera, and press C to capture the background image.

Two screens will open: one represents the mask used to substitute the foreground from the background, and the other is the final result. You may now appear on camera, and your background will be the "Bliss image".

You can change the "Bliss image" for any picture, as long as it's still 640x480 pixels.

## Requirements

This code uses Python 3, NumPy and OpenCV (built on 4.5.1)

```
python3 bgsub.py
```