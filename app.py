import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_image_coordinates import image_coordinates

# Load the colors CSV
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

colors_df = load_colors()

# Find closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = None
    for _, row in colors_df.iterrows():
        d = abs(R - row.R) + abs(G - row.G) + abs(B - row.B)
        if d < minimum:
            minimum = d
            cname = row.color_name
    return cname

st.title("Color Detection from Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    coords = image_coordinates(img)

    if coords is not None:
        x, y = coords["x"], coords["y"]
        rgb = img.convert('RGB').getpixel((x, y))
        color_name = get_color_name(*rgb)

        st.write(f"**Position:** ({x}, {y})")
        st.write(f"**Detected Color:** {color_name}")
        st.color_picker("Color Preview", value='#%02x%02x%02x' % rgb, disabled=True)
