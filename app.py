
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import pandas as pd
from utils import load_colors, get_closest_color_name

st.set_page_config(page_title="Color Detector", layout="centered")
st.title("Color Detection from Image")

colors_df = load_colors()

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.subheader("Click on the image to detect color:")
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=0,
        background_image=image,
        update_streamlit=True,
        height=image_np.shape[0],
        width=image_np.shape[1],
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
        last_obj = canvas_result.json_data["objects"][-1]
        x, y = int(last_obj["left"]), int(last_obj["top"])

        r, g, b = image_np[y, x]
        color_name = get_closest_color_name(r, g, b, colors_df)

        st.markdown(f"**Color Name:** `{color_name}`")
        st.markdown(f"**RGB:** `{r}, {g}, {b}`")
        st.markdown(
            f"<div style='width:100px; height:100px; background-color:rgb({r},{g},{b}); border:1px solid #000;'></div>",
            unsafe_allow_html=True
        )
else:
    st.info("Upload an image to get started.")
