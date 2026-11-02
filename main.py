import cv2
import numpy as np

def generate_synthetic_image(width=600, height=400, region_size=50):
    """
    Generates a synthetic image with distinct corner colors and a grey center.
    The corner regions will be `region_size` x `region_size` pixels.
    """
    img = np.ones((height, width, 3), dtype=np.uint8) * 128  # Grey background (B, G, R)

    # Define BGR colors for corners
    colors = {
        "top-left": (0, 0, 255),      # Red
        "top-right": (0, 255, 0),     # Green
        "bottom-left": (255, 0, 0),   # Blue
        "bottom-right": (0, 255, 255) # Yellow
    }

    # Draw colored rectangles in corners using array slicing
    img[0:region_size, 0:region_size] = colors["top-left"]
    img[0:region_size, width-region_size:width] = colors["top-right"]
    img[height-region_size:height, 0:region_size] = colors["bottom-left"]
    img[height-region_size:height, width-region_size:width] = colors["bottom-right"]

    return img

def calculate_corner_colors(image, region_size=50):
    """
    Calculates the average BGR color for the four specified corner regions of an image.
    """
    h, w, _ = image.shape
    
    # Ensure the image is large enough for the specified region size
    if h < region_size * 2 or w < region_size * 2:
        raise ValueError(f"Image (H:{h}, W:{w}) is too small for region size {region_size}. "
                         f"Minimum size required is {region_size*2}x{region_size*2}.")

    # Extract corner regions using numpy slicing
    corners = {
        "top-left": image[0:region_size, 0:region_size],
        "top-right": image[0:region_size, w-region_size:w],
        "bottom-left": image[h-region_size:h, 0:region_size],
        "bottom-right": image[h-region_size:h, w-region_size:w]
    }

    average_colors = {}
    for name, region in corners.items():
        # Calculate mean for each channel (B, G, R) across the region
        # .astype(int) converts float averages to integers
        avg_bgr = np.mean(region, axis=(0, 1)).astype(int)
        # Convert numpy array to a tuple of integers for consistency and easy use with cv2 functions
        average_colors[name] = tuple(avg_bgr.tolist()) 
    
    return average_colors

def create_color_swatch_image(average_colors, swatch_size=100, padding=20):
    """
    Creates a new image displaying color swatches for each average color,
    along with their labels and BGR values.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 1
    text_color = (0, 0, 0) # Black text for visibility on white background

    # Calculate maximum width needed for text labels
    # Example longest text: "Bottom-Right: (255, 255, 255)"
    test_text = "Bottom-Right: (255, 255, 255)" 
    max_text_width = cv2.getTextSize(test_text, font, font_scale, font_thickness)[0][0]

    # Calculate overall output image dimensions
    output_img_width = padding + swatch_size + padding + max_text_width + padding
    output_img_height = len(average_colors) * (swatch_size + padding) + padding

    # Create a blank white image for output
    output_img = np.ones((output_img_height, output_img_width, 3), dtype=np.uint8) * 255 

    current_y_offset = padding # Starting Y position for the first swatch

    for name, bgr_color in average_colors.items():
        # Draw the color swatch rectangle
        cv2.rectangle(output_img, 
                      (padding, current_y_offset), 
                      (padding + swatch_size, current_y_offset + swatch_size), 
                      bgr_color, 
                      -1) # -1 fills the rectangle

        # Format the text label, e.g., "Top-Left: (B, G, R)"
        display_name = name.replace('-', ' ').title()
        text_label = f"{display_name}: {bgr_color}"
        
        # Get text dimensions for vertical centering with the swatch
        text_size = cv2.getTextSize(text_label, font, font_scale, font_thickness)[0]
        
        # Calculate text position (horizontally aligned right of swatch, vertically centered)
        text_x = 2 * padding + swatch_size
        text_y = current_y_offset + swatch_size // 2 + text_size[1] // 2
        
        # Put the text label on the image
        cv2.putText(output_img, 
                    text_label, 
                    (text_x, text_y), 
                    font, 
                    font_scale, 
                    text_color, 
                    font_thickness,
                    cv2.LINE_AA) # Use LINE_AA for antialiased text

        # Move to the next Y position for the next swatch
        current_y_offset += swatch_size + padding
        
    return output_img

def main():
    # --- Configuration Parameters ---
    INPUT_IMAGE_WIDTH = 600
    INPUT_IMAGE_HEIGHT = 400
    CORNER_REGION_SIZE = 50  # Size of the square region to sample from each corner (e.g., 50x50 pixels)
    OUTPUT_SWATCH_SIZE = 100 # Size of each color swatch in the output image
    OUTPUT_PADDING = 20      # Padding around elements in the output image
    
    # Output filenames
    INPUT_IMAGE_FILENAME = "input_synthetic_image.png"
    OUTPUT_IMAGE_FILENAME = "corner_colors_output.png"

    print(f"Generating synthetic input image ({INPUT_IMAGE_WIDTH}x{INPUT_IMAGE_HEIGHT}): {INPUT_IMAGE_FILENAME}")
    synthetic_image = generate_synthetic_image(INPUT_IMAGE_WIDTH, INPUT_IMAGE_HEIGHT, CORNER_REGION_SIZE)
    cv2.imwrite(INPUT_IMAGE_FILENAME, synthetic_image)
    print(f"Synthetic input image saved to {INPUT_IMAGE_FILENAME}")

    print(f"\nCalculating average BGR for {CORNER_REGION_SIZE}x{CORNER_REGION_SIZE} corner regions...")
    try:
        average_colors = calculate_corner_colors(synthetic_image, CORNER_REGION_SIZE)
        for corner, color in average_colors.items():
            print(f"- {corner.replace('-', ' ').title()}: BGR {color}")
    except ValueError as e:
        print(f"Error: {e}")
        return # Exit if the input image is too small for the defined region size

    print(f"\nCreating output image with color swatches: {OUTPUT_IMAGE_FILENAME}")
    output_image = create_color_swatch_image(average_colors, OUTPUT_SWATCH_SIZE, OUTPUT_PADDING)
    cv2.imwrite(OUTPUT_IMAGE_FILENAME, output_image)
    print(f"Output image saved to {OUTPUT_IMAGE_FILENAME}")
    print("\nScript completed successfully.")

if __name__ == "__main__":
    main()