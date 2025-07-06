import streamlit as st
import cv2
import numpy as np
from PIL import Image
from utils import load_colors, get_closest_color_name

st.set_page_config(page_title="Color Detector", layout="centered")
st.title("Color Detection from Image")

colors_df = load_colors()

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    st.image(image, caption="Click on the image to detect color", use_column_width=True)

    click = st.image(image_np, use_column_width=True)

    # Capture mouse clicks using OpenCV window (for local dev only)
    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            b, g, r = image_np[y, x]
            color_name = get_closest_color_name(r, g, b, colors_df)
            st.session_state['selected_color'] = {
                'rgb': (r, g, b),
                'name': color_name
            }

    if st.button("Activate Click Detection"):
        cv2.imshow("Image - Click to detect color", cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
        cv2.setMouseCallback("Image - Click to detect color", click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if 'selected_color' in st.session_state:
        r, g, b = st.session_state['selected_color']['rgb']
        name = st.session_state['selected_color']['name']
        st.markdown(f"**Detected Color:** `{name}`")
        st.markdown(f"**RGB:** `{r}, {g}, {b}`")
        st.markdown(
            f"<div style='width:100px; height:100px; background-color:rgb({r},{g},{b}); border:1px solid #000;'></div>",
            unsafe_allow_html=True
        )
else:
    st.info("Please upload an image to start color detection.")
