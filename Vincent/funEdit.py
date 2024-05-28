# functions
import numpy as np
import cv2

def adjust_brightness_contrast(image, brightness, contrast):
    
    # Adjust brightness
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)

    # Adjust contrast
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)
    
    # Clip the values to keep them in the valid range [0, 255]
    image = np.clip(image, 0, 255)
    
    # Convert back to uint8
    return image