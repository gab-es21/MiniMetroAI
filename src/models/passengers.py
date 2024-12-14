import pygame
import random
from shapely.geometry import Point

from utils.constants import DARK_GREY

class Passenger:
    def __init__(self, station_position, shape, index):
        self.position = self.calculate_position(station_position, index)
        self.shape = shape  # "circle", "square", or "triangle"

    @staticmethod
    def calculate_position(station_position, index):
        """Calculate the passenger's position based on its index."""
        base_x, base_y = station_position
        row = index // 4  # 4 passengers per row
        col = index % 4   # Column within the row
        offset_x = 20 + col * 20  # Offset passengers horizontally
        offset_y = row * 20       # Offset passengers vertically
        return (base_x + offset_x, base_y + offset_y)

