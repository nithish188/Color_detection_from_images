import streamlit as st
import cv2
import numpy as np
import pandas as pd
from utils import get_closest_color_name

# Load color dataset
colors_df = pd.read_csv("colors.csv")

st.title("🎨 Color Detection from Images")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    st.image(image, caption="Click on the image to detect colors", use_column_width=True)

    clicked = st.image(image, use_column_width=True)

    # Coordinate state
    if "coords" not in st.session_state:
        st.session_state.coords = None

    def handle_click(x, y):
        st.session_state.coords = (x, y)

    # Handle mouse click on image
    from streamlit_image_coordinates import image_coordinates
    coords = image_coordinates(image)

    if coords:
        x, y = int(coords['x']), int(coords['y'])
        b, g, r = image[y, x]
        color_name = get_closest_color_name(r, g, b, colors_df)

        st.markdown(f"### 📌 Detected Color: `{color_name}`")
        st.write(f"RGB: ({r}, {g}, {b})")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});'></div>",
            unsafe_allow_html=True
        )
