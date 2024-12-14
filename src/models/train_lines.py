
import pygame

from utils.constants import TRAIN_LINE_THICKNESS
class TrainLine:
    def __init__(self, color):
        self.color = color  # Line color
        self.stations = []  # List of connected stations
        self.trains = []    # Trains operating on this line
        self.active = False  # Whether this line is selected
        self.blocked = False  # Blocked until unlocked
        self.sidebar_center = None  # Sidebar position (to be set later)
        self.sidebar_rect = None  # Clickable area for the line selector
    
    def set_sidebar_position(self, center):
        """Set the sidebar circle's position and bounding rectangle."""
        self.sidebar_center = center
        self.sidebar_rect = pygame.Rect(center[0] - 20, center[1] - 20, 40, 40)
    
    def toggle_active(self):
        """Toggle the active state of the line."""
        self.active = not self.active

    def add_connection(self, station1, station2):
            """Add a connection between two stations."""
            if station1 not in self.stations:
                self.stations.append(station1)
            if station2 not in self.stations:
                self.stations.append(station2)
            print(f"Connected {station1.shape} at ({station1.x}, {station1.y}) to {station2.shape} at ({station2.x}, {station2.y}).")

    def draw(self, screen, index=0):
            """Draw the train line connecting all stations."""
            if len(self.stations) > 1:
                for i in range(len(self.stations) - 1):
                    start = (self.stations[i].x, self.stations[i].y)
                    end = (self.stations[i + 1].x, self.stations[i + 1].y)
                    path = calculate_simplified_path(start, end)
                    offset_path_points = offset_path(path, index)
                    
                    # Draw the line
                    pygame.draw.lines(screen, self.color, False, offset_path_points, TRAIN_LINE_THICKNESS)

                    # Draw rounded corners
                    for j in range(1, len(offset_path_points) - 1):
                        prev_point = offset_path_points[j - 1]
                        current_point = offset_path_points[j]
                        next_point = offset_path_points[j + 1]
                        if prev_point[0] != next_point[0] and prev_point[1] != next_point[1]:
                            # A turn is detected
                            center = current_point
                            radius = TRAIN_LINE_THICKNESS  # Adjust as needed
                            pygame.draw.circle(screen, self.color, center, radius)
    
def add_connection(self, station1, station2):
    """Add a connection between two stations."""
    if station1 not in self.stations:
        self.stations.append(station1)
    if station2 not in self.stations:
        self.stations.append(station2)
    print(f"Connected {station1.shape} at ({station1.x}, {station1.y}) to {station2.shape} at ({station2.x}, {station2.y}).")
def draw_rounded_corner(screen, color, center, radius, start_angle, end_angle):
    """
    Draw a rounded corner between two segments.
    """
    pygame.draw.arc(screen, color, (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                    start_angle, end_angle, 3)
def offset_path(path, offset_index, spacing=TRAIN_LINE_THICKNESS):
    """
    Offset a path slightly to avoid overlap between lines.
    """
    if offset_index == 0:
        return path  # No offset for the first line

    # Offset direction based on perpendicular vector
    offset_path = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        # Perpendicular vector
        dx, dy = y2 - y1, x1 - x2
        length = (dx ** 2 + dy ** 2) ** 0.5
        dx, dy = dx / length, dy / length

        # Apply offset
        offset_x, offset_y = dx * spacing * offset_index, dy * spacing * offset_index
        offset_path.append((x1 + offset_x, y1 + offset_y))
        offset_path.append((x2 + offset_x, y2 + offset_y))

    return offset_path

def calculate_simplified_path(start, end):
    """
    Calculate a simplified path from start to end, following horizontal, vertical, 
    or 45-degree increments with intermediate points.
    """
    path = [start]
    x1, y1 = start
    x2, y2 = end

    while (x1, y1) != (x2, y2):
        if abs(x2 - x1) > abs(y2 - y1):  # Move horizontally
            x1 += 1 if x2 > x1 else -1
        elif abs(y2 - y1) > abs(x2 - x1):  # Move vertically
            y1 += 1 if y2 > y1 else -1
        else:  # Move diagonally
            x1 += 1 if x2 > x1 else -1
            y1 += 1 if y2 > y1 else -1
        path.append((x1, y1))

    return path
