import cv2
import numpy as np

def preprocess_image(img: np.ndarray) -> np.ndarray:
    """
    Normalize image for downstream row detection and OCR.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    return gray
