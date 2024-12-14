import random
import pygame
from shapely.geometry import Point

from utils.helpers import draw_passengers
from utils.constants import BLACK, FORBIDDEN_DISTANCE, PASSENGER_SPAWN_INTERVAL, RIVER_MARGIN, STATION_SIZE, WHITE
from models.passengers import Passenger

class Station:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape  # Type of station (circle, square, triangle)
        self.radius = 20
        self.passengers = []  # List of passengers waiting at this station
        self.spawn_timer = 0  # Time tracker for spawning passengers

    def spawn_passenger(self, elapsed_time):
        """Spawn a new passenger if the timer allows."""
        if elapsed_time - self.spawn_timer >= PASSENGER_SPAWN_INTERVAL and random.random() < 0.5:
            # Exclude the station's shape from possible passenger shapes
            possible_shapes = [shape for shape in ["circle", "square", "triangle"] if shape != self.shape]

            # Randomly choose a passenger shape from the filtered list
            passenger_shape = random.choice(possible_shapes)

            # Add the passenger to the station
            self.passengers.append(Passenger((self.x, self.y), passenger_shape, len(self.passengers)))
            self.spawn_timer = elapsed_time
            print(f"Passenger added to station at ({self.x}, {self.y}) with shape: {passenger_shape}")

    def print_station_details(self):
        """Print the station details including passengers."""
        passenger_shapes = [p.shape for p in self.passengers]
        print(f"Station: ({self.x}, {self.y}), Shape: {self.shape}, Passengers: {passenger_shapes}")
    
    def draw(self, screen):
        """Draw the station and its passengers."""
        # Draw the station
        half_size = STATION_SIZE // 2
        if self.shape == "square":
            pygame.draw.rect(screen, WHITE, (self.x - half_size, self.y - half_size, STATION_SIZE, STATION_SIZE))
            pygame.draw.rect(screen, BLACK, (self.x - half_size, self.y - half_size, STATION_SIZE, STATION_SIZE), 3)
        elif self.shape == "circle":
            pygame.draw.circle(screen, WHITE, (self.x, self.y), half_size)
            pygame.draw.circle(screen, BLACK, (self.x, self.y), half_size, 3)
        elif self.shape == "triangle":
            height = (STATION_SIZE * (3 ** 0.5)) / 2
            points = [
                (self.x, self.y - height // 2),
                (self.x - half_size, self.y + height // 2),
                (self.x + half_size, self.y + height // 2)
            ]
            pygame.draw.polygon(screen, WHITE, points)
            pygame.draw.polygon(screen, BLACK, points, 3)

        # Draw the passengers
        draw_passengers(screen, self.passengers)


    @staticmethod
    def generate_new_station(river_polygon, existing_stations, grid_points):
        """
        Generate a new station using available grid points.
        """
        valid_points = [
            (x, y) for x, y in grid_points
            if river_polygon.distance(Point(x, y)) > RIVER_MARGIN
            and all(Point(x, y).distance(Point(s.x, s.y)) > FORBIDDEN_DISTANCE for s in existing_stations)
        ]

        if valid_points:
            x, y = random.choice(valid_points)
            shape = random.choice(["circle", "square", "triangle"])
            grid_points.remove((x, y))  # Remove used point
            return Station(x, y, shape)
        
        return None  # No valid points available

    
    @classmethod
    def generate_initial_stations(cls, river_polygon, width, height, grid_size=50, sidebar_width=200):
        """
        Generate the first three stations using precomputed grid points.
        """
        # Precompute all possible points
        playable_width = width - sidebar_width
        grid_points = [
            (x, y)
            for x in range(FORBIDDEN_DISTANCE, playable_width, grid_size)
            for y in range(FORBIDDEN_DISTANCE, height, grid_size)
            if river_polygon.distance(Point(x, y)) > FORBIDDEN_DISTANCE
        ]

        initial_stations = []
        shapes = ["circle", "square", "triangle"]

        for shape in shapes:
            # Randomly pick a valid point
            valid_points = [
                (x, y) for x, y in grid_points
                if all(Point(x, y).distance(Point(s.x, s.y)) > FORBIDDEN_DISTANCE for s in initial_stations)
            ]

            if valid_points:
                x, y = random.choice(valid_points)
                initial_stations.append(cls(x, y, shape))
                grid_points.remove((x, y))  # Remove used point

        return initial_stations
    
    def contains(self, pos):
        """Check if the given position (pos) is within the station area."""
        px, py = pos
        distance = ((px - self.x) ** 2 + (py - self.y) ** 2) ** 0.5

        if self.shape == "circle":
            return distance <= self.radius
        elif self.shape == "square":
            return (self.x - self.radius <= px <= self.x + self.radius) and \
                   (self.y - self.radius <= py <= self.y + self.radius)
        elif self.shape == "triangle":
            # For simplicity, use the bounding box of the triangle
            height = (self.radius * (3 ** 0.5)) / 2
            return (self.x - self.radius <= px <= self.x + self.radius) and \
                   (self.y - height / 2 <= py <= self.y + height / 2)
        return False




