from PIL import Image
import numpy as np

# Load the PNG image
img = Image.open('colorful@4x.png').convert('RGB')

# Resize if needed (e.g., to 240x320)
img = img.resize((240, 320))

# Convert to numpy array
arr = np.array(img)

# Convert to RGB565
def rgb888_to_rgb565(arr):
    r = (arr[..., 0] >> 3).astype(np.uint16)
    g = (arr[..., 1] >> 2).astype(np.uint16)
    b = (arr[..., 2] >> 3).astype(np.uint16)
    return ((r << 11) | (g << 5) | b)

rgb565 = rgb888_to_rgb565(arr)

# Save as binary
with open('colorful.bin', 'wb') as f:
    f.write(rgb565.astype('>u2').tobytes())  # '>u2' for big-endian, '<u2' for little-endian