import os
import json
import pygame
import random
from utils.constants import BLACK, BORDER_MARGIN, DARK_GREY, FORBIDDEN_DISTANCE, HEIGHT, LIGHT_BLUE, SHADOW_COLOR, STATION_SIZE, WHITE, WIDTH 
# Colors
DARK_BEIGE = (220, 220, 200)

# Load Random Map
def load_random_map(save_path="maps/generated"):
    if not os.path.exists(save_path):
        raise FileNotFoundError(f"Map directory '{save_path}' does not exist.")
    map_files = [f for f in os.listdir(save_path) if f.endswith(".json")]
    if not map_files:
        raise FileNotFoundError(f"No map files found in '{save_path}'. Please generate maps first.")
    selected_file = random.choice(map_files)
    with open(os.path.join(save_path, selected_file), "r") as f:
        return json.load(f)

def draw_forbidden_area(screen, river_polygon, stations):
    """Visualize forbidden areas on the map."""
    # River forbidden area
    if not river_polygon.is_empty:
        points = [(int(x), int(y)) for x, y in river_polygon.exterior.coords]
        pygame.draw.polygon(screen, LIGHT_BLUE, points)  # Use LIGHT_BLUE for the river


     # Stations forbidden areas
    for station in stations:
        pygame.draw.circle(screen, (200, 200, 200), (station.x, station.y), FORBIDDEN_DISTANCE, 0)  # Grey forbidden area

    # Map border forbidden area
    pygame.draw.rect(screen, DARK_BEIGE, (0, 0, WIDTH, BORDER_MARGIN))  # Top border
    pygame.draw.rect(screen, DARK_BEIGE, (0, HEIGHT - BORDER_MARGIN, WIDTH, BORDER_MARGIN))  # Bottom border
    pygame.draw.rect(screen, DARK_BEIGE, (0, 0, BORDER_MARGIN, HEIGHT))  # Left border
    pygame.draw.rect(screen, DARK_BEIGE, (WIDTH - BORDER_MARGIN, 0, BORDER_MARGIN, HEIGHT))  # Right border

# Draw Station
def draw_station(screen, station):
    """Draw a station with a shadow for a professional look."""
    x, y, shape = station.x, station.y, station.shape  # Access station attributes
    shadow_offset = 3
    half_size = STATION_SIZE // 2

    # Shadow
    if shape == "square":
        pygame.draw.rect(
            screen, SHADOW_COLOR,
            (x - half_size + shadow_offset, y - half_size + shadow_offset, STATION_SIZE, STATION_SIZE)
        )
    elif shape == "circle":
        pygame.draw.circle(screen, SHADOW_COLOR, (int(x) + shadow_offset, int(y) + shadow_offset), half_size)
    elif shape == "triangle":
        height = (STATION_SIZE * (3**0.5)) / 2
        points = [
            (x, y - height // 2 + shadow_offset),
            (x - half_size + shadow_offset, y + height // 2 + shadow_offset),
            (x + half_size + shadow_offset, y + height // 2 + shadow_offset)
        ]
        pygame.draw.polygon(screen, SHADOW_COLOR, points)

    # Station
    if shape == "square":
        pygame.draw.rect(
            screen, WHITE,
            (x - half_size, y - half_size, STATION_SIZE, STATION_SIZE)
        )
        pygame.draw.rect(
            screen, BLACK,
            (x - half_size, y - half_size, STATION_SIZE, STATION_SIZE), 3
        )
    elif shape == "circle":
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), half_size)
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), half_size, 3)
    elif shape == "triangle":
        height = (STATION_SIZE * (3**0.5)) / 2
        points = [
            (x, y - height // 2),
            (x - half_size, y + height // 2),
            (x + half_size, y + height // 2)
        ]
        pygame.draw.polygon(screen, WHITE, points)
        pygame.draw.polygon(screen, BLACK, points, 3)

def print_all_stations(stations):
    """Print details of all stations and their passengers."""
    print("\n--- Stations and Passengers ---")
    for station in stations:
        station.print_station_details()
    print("--------------------------------")

def draw_passengers(screen, passengers):
    """Draw all passengers near their respective stations."""
    PASSENGER_RADIUS = 5  # Smaller size for passengers

    for passenger in passengers:
        x, y = passenger.position
        if passenger.shape == "circle":
            pygame.draw.circle(screen, DARK_GREY, (int(x), int(y)), PASSENGER_RADIUS)  # Dark gray circle
        elif passenger.shape == "square":
            pygame.draw.rect(screen, DARK_GREY, (x - PASSENGER_RADIUS, y - PASSENGER_RADIUS, PASSENGER_RADIUS * 2, PASSENGER_RADIUS * 2))  # Dark gray square
        elif passenger.shape == "triangle":
            points = [
                (x, y - PASSENGER_RADIUS),
                (x - PASSENGER_RADIUS, y + PASSENGER_RADIUS),
                (x + PASSENGER_RADIUS, y + PASSENGER_RADIUS),
            ]
            pygame.draw.polygon(screen, DARK_GREY, points)  # Dark gray triangle
