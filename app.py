import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# Load color dataset (name, R, G, B)
@st.cache_data
def load_colors():
    url = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
    color_data = pd.read_csv(url)
    return color_data[['name', 'red', 'green', 'blue']]

# Function to find the closest color name
def get_closest_color_name(r, g, b, color_data):
    distances = np.sqrt((color_data['red'] - r)**2 + (color_data['green'] - g)**2 + (color_data['blue'] - b)**2)
    closest_index = distances.idxmin()
    return color_data.loc[closest_index, 'name']

# Load image using OpenCV from uploaded file
def load_image(image_file):
    image = Image.open(image_file)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Streamlit UI
st.title("🎨 Color Detection from Image")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    color_data = load_colors()
    image_bgr = load_image(uploaded_file)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    st.image(image_rgb, caption="Click on the image to detect color", use_column_width=True)

    # Get click coordinates
    click = st.image(image_rgb, channels="RGB")

    if 'clicked_point' not in st.session_state:
        st.session_state.clicked_point = None

    def handle_click(event):
        st.session_state.clicked_point = (int(event.x), int(event.y))

    st.markdown("**Click anywhere on the image above to detect a color.**")

    coords = st.experimental_data_editor(
        {"X": [""], "Y": [""]},
        disabled=["X", "Y"],
        key="coords",
        num_rows="fixed",
    )

    x = st.number_input("X coordinate", min_value=0, max_value=image_rgb.shape[1]-1, step=1)
    y = st.number_input("Y coordinate", min_value=0, max_value=image_rgb.shape[0]-1, step=1)

    if st.button("Detect Color"):
        r, g, b = image_rgb[y, x]
        color_name = get_closest_color_name(r, g, b, color_data)

        st.markdown(f"**Detected Color:** `{color_name}`")
        st.markdown(f"**RGB:** ({r}, {g}, {b})")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});border:1px solid #000'></div>",
            unsafe_allow_html=True,
        )
