import pandas as pd

# Load CSV dataset
def load_colors(csv_path="colors.csv"):
    return pd.read_csv(csv_path)

# Find closest color name from the dataset
def get_closest_color_name(R, G, B, colors_df):
    min_dist = float("inf")
    closest_name = ""
    for _, row in colors_df.iterrows():
        d = abs(R - int(row["R"])) + abs(G - int(row["G"])) + abs(B - int(row["B"]))
        if d < min_dist:
            min_dist = d
            closest_name = row["color_name"]
    return closest_name
