
import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

# Load color dataset
@st.cache_data
def load_colors():
    csv_path = 'D:\\colors.csv'
    return pd.read_csv(csv_path, names=["color", "color_name", "hex", "R", "G", "B"], header=None)

colors_df = load_colors()

# Function to get the closest color name
def get_color_name(R, G, B):
    minimum = float('inf')
    cname = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + abs(G - int(colors_df.loc[i, "G"])) + abs(B - int(colors_df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = colors_df.loc[i, "color_name"]
    return cname

st.title("🎨 Color Detection App")
st.write("Upload an image and click to get the nearest color name.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Display the image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    st.write("Click anywhere on the image to get color info (use coordinates):")
    x = st.number_input("X Coordinate", min_value=0, max_value=image_np.shape[1]-1, value=0)
    y = st.number_input("Y Coordinate", min_value=0, max_value=image_np.shape[0]-1, value=0)

    if st.button("Detect Color"):
        pixel = image_np[int(y), int(x)]
        R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2]) if image_np.shape[2] == 3 else (0, 0, 0)

        color_name = get_color_name(R, G, B)
        st.markdown(f"**Color Name**: {color_name}")
        st.markdown(f"**RGB**: ({R}, {G}, {B})")
        st.markdown(f"<div style='width:100px;height:50px;background-color:rgb({R},{G},{B});'></div>", unsafe_allow_html=True)
