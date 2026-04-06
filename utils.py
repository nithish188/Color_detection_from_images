import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def load_colors(csv_path="colors.csv"):
    """Load and cache the color dataset."""
    return pd.read_csv(csv_path)


def get_closest_color_name(R, G, B, colors_df):
    """
    Find the closest color name using vectorized Euclidean distance
    in RGB space for fast, perceptually better matching.
    """
    rgb_array = colors_df[["R", "G", "B"]].values.astype(np.int32)
    target = np.array([R, G, B], dtype=np.int32)

    # Euclidean distance (vectorized — no Python loop)
    distances = np.sqrt(np.sum((rgb_array - target) ** 2, axis=1))
    closest_idx = np.argmin(distances)
    return colors_df.iloc[closest_idx]["color_name"]
