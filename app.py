import streamlit as st
import pandas as pd
import numpy as np
import cv2
from streamlit_image_coordinates import image_coordinates
from PIL import Image

# Load color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

# Find the closest color name
def get_color_name(R, G, B, colors_df):
    minimum = float('inf')
    cname = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

# Load color data
colors_df = load_colors()

# UI
st.title("🎨 Color Detection from Image")
st.markdown("Upload an image and click anywhere on it to detect the color at that pixel.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)  # Load with OpenCV
    opencv_image_rgb = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    # Convert to PIL for display
    image_pil = Image.fromarray(opencv_image_rgb)

    # Show image in Streamlit
    coords = image_coordinates("Click on the image to detect color", image_pil)

    if coords:
        x, y = int(coords["x"]), int(coords["y"])
        height, width, _ = opencv_image_rgb.shape

        if 0 <= x < width and 0 <= y < height:
            b, g, r = opencv_image[y, x]
            color_name = get_color_name(r, g, b, colors_df)

            st.markdown(f"**Coordinates:** ({x}, {y})")
            st.markdown(f"**Detected Color:** `{color_name}`")
            st.markdown(f"**RGB (R,G,B):** ({r}, {g}, {b})")
            hex_color = '#%02x%02x%02x' % (r, g, b)
            st.color_picker("Color Preview", value=hex_color, label_visibility="collapsed", disabled=True)
        else:
            st.warning("Click inside the image boundaries.")
