#!/usr/bin/env python3
"""Prep a photo for ASCII conversion: remove bg, boost contrast, composite on white."""

import sys
from pathlib import Path
import numpy as np
from PIL import Image
import cv2
from rembg import remove

def prep_photo(source_path: str, output_path: str = "source-prepped.png"):
    print(f"Loading {source_path}...")
    img = Image.open(source_path)
    
    # Step 1: Remove background
    print("Removing background...")
    no_bg = remove(img)
    
    # Step 2: Convert to grayscale numpy array
    gray = np.array(no_bg.convert('L'))
    
    # Step 3: Apply CLAHE for local contrast enhancement
    print("Boosting contrast...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Boost brightness overall
    enhanced = np.clip(enhanced * 1.3 + 30, 0, 255).astype(np.uint8)
    
    # Step 4: Composite onto white background
    # Get alpha channel from original no_bg image
    alpha = np.array(no_bg.split()[-1])
    
    # Create white background
    white_bg = np.ones_like(enhanced) * 255
    
    # Blend: fg * alpha + bg * (1 - alpha)
    alpha_norm = alpha / 255.0
    result = (enhanced * alpha_norm + white_bg * (1 - alpha_norm)).astype(np.uint8)
    
    # Save result
    print(f"Saving to {output_path}...")
    Image.fromarray(result).save(output_path)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo>")
        sys.exit(1)
    
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    prep_photo(source, output)
