import pygame
import os
import json
import random
from shapely.geometry import LineString

from utils.constants import TRAIN_LINE_THICKNESS


# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
screen = pygame.display.set_mode((WIDTH + BUTTON_WIDTH * 2, HEIGHT))  # Extra space for buttons
pygame.display.set_caption("Map Generation with Save and Next")

# Colors
BEIGE = (245, 245, 220)  # Land
LIGHT_BLUE = (173, 216, 230)  # Water
BLACK = (0, 0, 0)  # Border
WHITE = (255, 255, 255)  # Button background
GREY = (200, 200, 200)  # Button hover background

# Paths
SAVE_PATH = "maps/generated"

# Ensure the save directory exists
os.makedirs(SAVE_PATH, exist_ok=True)

# Functions for generating the river and its path (already provided)
from maps.map_utils import generate_line, generate_river


def draw_button(screen, x, y, width, height, text, font, hover=False):
    """Draw a button on the screen."""
    color = GREY if hover else WHITE
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)  # Border
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


def get_next_filename(directory):
    """Get the next available filename for map saving."""
    files = [f for f in os.listdir(directory) if f.startswith("map_") and f.endswith(".json")]
    numbers = [int(f.split("_")[1].split(".")[0]) for f in files if f.split("_")[1].split(".")[0].isdigit()]
    next_number = max(numbers, default=0) + 1
    return f"map_{next_number:03}.json"


def save_map(map_data):
    """Save the current map to a JSON file."""
    filename = get_next_filename(SAVE_PATH)
    with open(os.path.join(SAVE_PATH, filename), 'w') as f:
        json.dump(map_data, f, indent=4)
    print(f"Map saved as {filename}")


# Main function
def main():
    font = pygame.font.Font(None, 24)

    # Button positions
    next_button = pygame.Rect(WIDTH, HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
    save_button = pygame.Rect(WIDTH + BUTTON_WIDTH, HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Generate initial map
    curve_type = random.choice(["linear", "parabolic", "sine", "cosine"])
    print(f"Curve Type: {curve_type}")
    path = generate_line(WIDTH, HEIGHT, offset=50, curve_type=curve_type)
    river = generate_river(path, start_thickness=10, mid_thickness=30, end_thickness=15)

    map_data = {
        "width": WIDTH,
        "height": HEIGHT,
        "river": {
            "path": path,
            "thickness": {
                "start": 10,
                "middle": 30,
                "end": 15
            },
            "curve_type": curve_type
        }
    }

    running = True
    while running:
        screen.fill(BEIGE)  # Set background as land

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    # Generate a new map
                    curve_type = random.choice(["linear", "parabolic", "sine", "cosine"])
                    print(f"Curve Type: {curve_type}")
                    path = generate_line(WIDTH, HEIGHT, offset=50, curve_type=curve_type)
                    river = generate_river(path, start_thickness=10, mid_thickness=30, end_thickness=15)

                    map_data = {
                        "width": WIDTH,
                        "height": HEIGHT,
                        "river": {
                            "path": path,
                            "thickness": {
                                "start": 10,
                                "middle": 30,
                                "end": 15
                            },
                            "curve_type": curve_type
                        }
                    }
                elif save_button.collidepoint(event.pos):
                    # Save the current map
                    save_map(map_data)

        # Draw the river
        if not river.is_empty:
            points = [(int(x), int(y)) for x, y in river.exterior.coords]
            pygame.draw.polygon(screen, LIGHT_BLUE, points)
            pygame.draw.lines(screen, BLACK, True, points, TRAIN_LINE_THICKNESS)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, next_button.x, next_button.y, next_button.width, next_button.height,
                    "Next", font, hover=next_button.collidepoint(mouse_pos))
        draw_button(screen, save_button.x, save_button.y, save_button.width, save_button.height,
                    "Save", font, hover=save_button.collidepoint(mouse_pos))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
