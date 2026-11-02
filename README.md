# quad-corner-color

Calculates and displays average BGR color for four image corner regions.

This project generates a synthetic test image, samples the average BGR color from the top-left, top-right, bottom-left, and bottom-right corner regions (e.g., 50x50 pixels), and then creates a new image displaying these four average colors as distinct color swatches with their corresponding BGR values.

The script is designed to run on headless servers, meaning it will not open any GUI windows but instead saves all visual output to image files.

## How to Run

1.  **Clone the repository (or save `main.py` and `requirements.txt`):**
    ```bash
    git clone https://github.com/your-repo-link/quad-corner-color.git
    cd quad-corner-color
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## Output

Upon successful execution, the script will generate two image files in the same directory:

*   `input_synthetic_image.png`: The internally generated image used for analysis, showcasing distinct colors in its corners.
*   `corner_colors_output.png`: The output image displaying the calculated average BGR color swatches for each corner region, along with their names and BGR values.

Example `corner_colors_output.png`:
(An image with four vertical swatches, each labeled "Top-Left: (B, G, R)", "Top-Right: (B, G, R)", etc.)