from PIL import Image
import numpy as np

def image_to_negative(image: np.ndarray) -> np.ndarray:
    """Transforms a classic image into its negative"""
    negative = image.copy()
    for i in range(0, image.size[0]-1):
        for j in range(0, image.size[1]-1):
            pixelColorVals = image.getpixel((i,j))
            redPixel    = 255 - pixelColorVals[0] # Negate red pixel
            greenPixel  = 255 - pixelColorVals[1] # Negate green pixel
            bluePixel   = 255 - pixelColorVals[2] # Negate blue pixel
            negative.putpixel((i,j),(redPixel, greenPixel, bluePixel))
    return negative

print("Server starting...")