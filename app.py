import streamlit as st
import pandas as pd
import numpy as np
import cv2
from streamlit_image_coordinates import image_coordinates
from PIL import Image
import os

# Load color names CSV
@st.cache_data
def load_colors():
    csv_path = os.path.join(os.path.dirname(__file__), "colors.csv")
    return pd.read_csv(csv_path, names=["color", "color_name", "hex", "R", "G", "B"], header=None)

colors_df = load_colors()

# Color matcher
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

# Streamlit UI
st.title("Color Detection from Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Click on the image", use_column_width=True)
    
    coords = image_coordinates("Click to detect color", image)
    
    if coords:
        x, y = int(coords["x"]), int(coords["y"])
        rgb = image.getpixel((x, y))
        color_name = get_color_name(*rgb)
        
        st.markdown(f"**Coordinates:** ({x}, {y})")
        st.markdown(f"**Detected Color:** `{color_name}`")
        st.markdown(f"**RGB:** {rgb}")
        st.color_picker("Detected Color Preview", value='#%02x%02x%02x' % rgb, label_visibility='collapsed', disabled=True)
