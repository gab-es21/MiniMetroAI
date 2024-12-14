import random
from shapely.geometry import LineString, Point
from utils.constants import BORDER_MARGIN, DOT_RADIUS, FORBIDDEN_DISTANCE, HEIGHT, RIVER_MARGIN, WIDTH
from utils.helpers import load_random_map

def initialize_game(width=WIDTH, height=HEIGHT):
    map_data = load_random_map()
    river_path = map_data["river"]["path"]
    river_polygon = LineString(river_path).buffer(25, cap_style=2)
    return map_data, river_polygon

import pygame
from shapely.geometry import Point

def draw_grid_dots(screen, river_polygon, existing_stations, width, height, grid_size=50, sidebar_width=200):
    """
    Draw dots representing possible station positions, excluding the sidebar area.
    Green = Valid placement
    Red = Forbidden zone
    """

    for x in range(BORDER_MARGIN, width-BORDER_MARGIN+1, grid_size):
        for y in range(BORDER_MARGIN, height-BORDER_MARGIN+1, grid_size):
            station_point = Point(x, y)

            # Check validity
            is_valid = (
                river_polygon.distance(station_point) > RIVER_MARGIN and
                all(station_point.distance(Point(s.x, s.y)) > FORBIDDEN_DISTANCE for s in existing_stations)
            )

            # Draw the dot
            color = (0, 255, 0) if is_valid else (255, 0, 0)  # Green for valid, red for forbidden
            pygame.draw.circle(screen, color, (x, y), DOT_RADIUS)
