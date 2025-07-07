import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import pandas as pd
from utils import load_colors, get_closest_color_name

# Configuration
st.set_page_config(page_title="Color Detector", layout="centered")
st.title("Color Detection from Image")

# Load color database
colors_df = load_colors()

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # Optional: Resize large images to fit screen
    MAX_WIDTH = 800
    if image.width > MAX_WIDTH:
        scale = MAX_WIDTH / image.width
        new_height = int(image.height * scale)
        image = image.resize((MAX_WIDTH, new_height))

    image_np = np.array(image)

    st.subheader("Click on the image to detect color:")
    st.caption("Click anywhere on the image to get the closest color name and RGB values.")

    # Draw canvas
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

    # Initialize color log
    if 'color_log' not in st.session_state:
        st.session_state.color_log = []

    if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
        last_obj = canvas_result.json_data["objects"][-1]
        x, y = int(last_obj["left"]), int(last_obj["top"])

        if 0 <= x < image_np.shape[1] and 0 <= y < image_np.shape[0]:
            r, g, b = image_np[y, x]
            color_name = get_closest_color_name(r, g, b, colors_df)

            st.markdown(f"**Color Name:** `{color_name}`")
            st.markdown(f"**RGB:** `{r}, {g}, {b}`")
            st.markdown(
                f"<div style='width:100px; height:100px; background-color:rgb({r},{g},{b}); border:1px solid #000;'></div>",
                unsafe_allow_html=True
            )

            # Add to log
            st.session_state.color_log.append({
                "Color Name": color_name,
                "R": r,
                "G": g,
                "B": b
            })
        else:
            st.warning("Clicked outside image bounds!")

    # Display color log
    if st.session_state.color_log:
        df_log = pd.DataFrame(st.session_state.color_log)
        st.subheader("Color Log")
        st.dataframe(df_log)

        csv = df_log.to_csv(index=False).encode('utf-8')
        st.download_button("Download Color Log", csv, "colors.csv", "text/csv")

else:
    st.info("Upload an image to get started.")
