from PIL import Image
import numpy as np
from scipy.ndimage import sobel

def sort_rows(pixels, width):
    pixels = np.array(pixels).reshape(-1, width, 4)
    for row in pixels:
        # Sum RGB values along the color channels, ignoring the alpha channel
        pix_sum = row[:, :3].sum(axis=1)
        # Sort the row based on the summed RGB values
        sorted_indices = pix_sum.argsort()
        row[:] = row[sorted_indices]

    return pixels

def sort_edge_pixels(image, edge_mask):
    pixels = np.array(image)
    edge_pixels = pixels[edge_mask]
    
    # Sum RGB values along the color channels, ignoring the alpha channel
    pix_sum = edge_pixels[:, :3].sum(axis=1)
    # Sort edge pixels based on the summed RGB values
    sorted_indices = pix_sum.argsort()
    sorted_edge_pixels = edge_pixels[sorted_indices]
    
    # Create a copy of the original pixels and replace edge regions with sorted pixels
    sorted_pixels = pixels.copy()
    sorted_pixels[edge_mask] = sorted_edge_pixels
    
    return sorted_pixels

def detect_edges(image):
    grayscale = np.array(image.convert('L'))
    dx = sobel(grayscale, axis=0)
    dy = sobel(grayscale, axis=1)
    edge_magnitude = np.hypot(dx, dy)
    return  edge_magnitude

def create_edge_mask(edge_magnitude, threshold):
    return edge_magnitude > threshold

im = Image.open('./sonoshee_wp.png', 'r')
im = im.convert('RGBA')

edge_magnitude = detect_edges(im)
edge_mask = create_edge_mask(edge_magnitude, threshold=355)  # Adjust threshold as needed

# Display the edge mask
edge_mask_image = Image.fromarray((edge_mask * 255).astype('uint8'))
edge_mask_image.save('./edge_mask.png')

# Optional: Display edge magnitude
edge_magnitude_image = Image.fromarray(edge_magnitude.astype('uint8'))
edge_magnitude_image.save('./edge_magnitude.png')

sorted_pix_val = sort_edge_pixels(im, edge_mask)

# Step 4: Combine Edge and Non-Edge Regions and Save Image
sorted_image = Image.fromarray(sorted_pix_val.astype('uint8'), 'RGBA')
sorted_image.save('./sorted_sonoshee_wp_edge_sorted.png')
# pix_val = np.asarray(im)

# sorted_pix_val = sort_rows(pix_val, im.size[0])

# # Reshape the sorted pixel array back into the image dimensions
# sorted_pix_val_reshaped = sorted_pix_val.reshape(im.size[1], im.size[0], 4)

# # Create a new image from the sorted pixel data
# sorted_image = Image.fromarray(sorted_pix_val_reshaped.astype('uint8'), im.mode)
# sorted_image.save('./sorted_sonoshee_wp.png')