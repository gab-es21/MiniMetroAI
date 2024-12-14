import random
import numpy as np
from shapely.geometry import LineString, Point

def generate_line(width, height, offset=50, curve_type="linear"):
    """Generate a curved river path from one border to another in different quadrants."""
    borders = ["top", "bottom", "left", "right"]
    start_border = random.choice(borders)
    borders.remove(start_border)  # Ensure the river ends on a different border
    end_border = random.choice(borders)

    # Determine start and end points based on borders with offsets
    if start_border == "top":
        start = (random.randint(-offset, width // 2), -offset)
    elif start_border == "bottom":
        start = (random.randint(-offset, width // 2), height + offset)
    elif start_border == "left":
        start = (-offset, random.randint(-offset, height // 2))
    elif start_border == "right":
        start = (width + offset, random.randint(-offset, height // 2))

    if end_border == "top":
        end = (random.randint(width // 2, width + offset), -offset)
    elif end_border == "bottom":
        end = (random.randint(width // 2, width + offset), height + offset)
    elif end_border == "left":
        end = (-offset, random.randint(height // 2, height + offset))
    elif end_border == "right":
        end = (width + offset, random.randint(height // 2, height + offset))

    num_points = 100
    if curve_type == "linear":
        x = np.linspace(start[0], end[0], num_points)
        y = np.linspace(start[1], end[1], num_points)
    elif curve_type == "parabolic":
        x = np.linspace(start[0], end[0], num_points)
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 + random.uniform(-50, 50)
        a = (start[1] - mid_y) / ((start[0] - mid_x) ** 2)
        y = a * (x - mid_x) ** 2 + mid_y
    elif curve_type in ["sine", "cosine"]:
        x = np.linspace(start[0], end[0], num_points)
        wavelength = (end[0] - start[0]) / 2
        amplitude = random.uniform(20, 50)
        phase = random.uniform(0, np.pi)
        if curve_type == "sine":
            y = amplitude * np.sin(2 * np.pi * (x - start[0]) / wavelength + phase) + np.linspace(start[1], end[1], num_points)
        else:
            y = amplitude * np.cos(2 * np.pi * (x - start[0]) / wavelength + phase) + np.linspace(start[1], end[1], num_points)
    else:
        raise ValueError(f"Unknown curve type: {curve_type}")

    return list(zip(x, y))
def generate_thickness(start_thickness, mid_thickness, end_thickness, num_segments):
    """Generate thickness values that vary along the river."""
    thickness = np.linspace(start_thickness, mid_thickness, num_segments // 2)
    thickness = np.append(thickness, np.linspace(mid_thickness, end_thickness, num_segments // 2))
    return thickness

def generate_river(path, start_thickness, mid_thickness, end_thickness):
    """Generate a smooth river polygon with varying thickness."""
    # Create the main line using the provided path
    line = LineString(path)

    # Generate thickness values for interpolation
    num_segments = len(path)
    thickness_values = np.linspace(start_thickness, mid_thickness, num_segments // 2)
    thickness_values = np.append(thickness_values, np.linspace(mid_thickness, end_thickness, num_segments // 2))

    # Create a unified buffer
    river_polygon = line.buffer(max(thickness_values), cap_style=2)
    print(f"River Polygon: {river_polygon}")  # Debug
    return river_polygon

