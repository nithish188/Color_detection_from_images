# utils.py

def get_color_name(R, G, B, csv_data):
    """Finds the closest color name by comparing RGB values."""
    minimum = float('inf')
    color_name = "Unknown"
    for i in range(len(csv_data)):
        d = abs(R - int(csv_data.loc[i, "R"])) + abs(G - int(csv_data.loc[i, "G"])) + abs(B - int(csv_data.loc[i, "B"]))
        if d < minimum:
            minimum = d
            color_name = csv_data.loc[i, "color_name"]
    return color_name

