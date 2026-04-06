# 🎨 Color Detection from Images

A Streamlit app that detects and names colors when you click on any part of an uploaded image.

## Features

- Upload any image (PNG, JPG, JPEG)
- Click anywhere to detect RGB, HEX, and the closest named color
- Visual color swatch with rounded styling
- Color log with deduplication — tracks all unique clicks
- Download the color log as CSV
- Clear log button to reset session

## Tech Stack

- Python 3.10
- Streamlit
- NumPy (vectorized Euclidean color matching)
- Pandas
- Pillow

## Setup Instructions

1. Clone the repo:
    ```bash
    git clone https://github.com/yourusername/color-detector.git
    cd color-detector
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:
    ```bash
    streamlit run streamlit_app.py
    ```

## Dataset

The `colors.csv` file contains 148 named colors from the CSS3/X11 color specification.
Color matching uses vectorized Euclidean distance in RGB space for fast and accurate results.

## Deployment

Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) — just connect your GitHub repo.
