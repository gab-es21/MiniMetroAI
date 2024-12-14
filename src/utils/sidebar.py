import pygame
from utils.constants import BLACK, BUTTON_BG, BUTTON_BORDER, HEIGHT, SIDEBAR_GRADIENT_END, SIDEBAR_GRADIENT_START, SIDEBAR_WIDTH, TEXT_COLOR, TITLE_FONT, WIDTH, BLUE, GREEN, GREY, ORANGE, RED, TITLE_FONT, CLOCK_FONT, TEXT_COLOR, YELLOW
def draw_gradient_rect(screen, rect, color1, color2):
    """Draw a vertical gradient in a rectangle."""
    x, y, width, height = rect
    for i in range(height):
        ratio = i / height
        color = [
            int(color1[j] * (1 - ratio) + color2[j] * ratio)
            for j in range(3)
        ]
        pygame.draw.line(screen, color, (x, y + i), (x + width, y + i))

def draw_circular_button(screen, rect, icon, is_pressed):
    """Draw a circular button with an icon."""
    center_x, center_y = rect.center
    radius = rect.width // 2

    # Background
    pygame.draw.circle(screen, BUTTON_BG, (center_x, center_y), radius)
    pygame.draw.circle(screen, BUTTON_BORDER, (center_x, center_y), radius, 2)

    # Icon
    if icon == "play":
        pygame.draw.polygon(screen, TEXT_COLOR, [
            (center_x - 5, center_y - 10),
            (center_x - 5, center_y + 10),
            (center_x + 10, center_y)
        ])
    elif icon == "pause":
        pygame.draw.rect(screen, TEXT_COLOR, (center_x - 10, center_y - 12, 6, 24))
        pygame.draw.rect(screen, TEXT_COLOR, (center_x + 4, center_y - 12, 6, 24))
    elif icon == "restart":
        # Full square icon
        square_size = 20
        pygame.draw.rect(screen, TEXT_COLOR, 
                         (center_x - square_size // 2, center_y - square_size // 2, square_size, square_size))


def draw_sidebar(screen, elapsed_time, play_button, restart_button, running, score, lines):
    """Draw the sidebar with clock, buttons, smaller circles, and scoreboard."""
    # Sidebar background
    pygame.draw.rect(screen, SIDEBAR_GRADIENT_START, (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))

    # Clock
    minutes, seconds = divmod(int(elapsed_time), 60)
    clock_text = TITLE_FONT.render(f"{minutes:02}:{seconds:02}", True, TEXT_COLOR)
    clock_rect = clock_text.get_rect(center=(WIDTH + (SIDEBAR_WIDTH // 2), 30))
    screen.blit(clock_text, clock_rect)

    # Scoreboard
    score_text = CLOCK_FONT.render(f"Score: {score}", True, TEXT_COLOR)
    score_rect = score_text.get_rect(center=(WIDTH + (SIDEBAR_WIDTH // 2), 70))
    screen.blit(score_text, score_rect)

    # Smaller Circles for Line Selection
    mouse_pos = pygame.mouse.get_pos()
    circle_positions = [
        (WIDTH + SIDEBAR_WIDTH // 2, 110),  # Green
        (WIDTH + SIDEBAR_WIDTH // 2, 150),  # Red
        (WIDTH + SIDEBAR_WIDTH // 2, 190),  # Yellow
        (WIDTH + SIDEBAR_WIDTH // 2, 230),  # Grey (1)
        (WIDTH + SIDEBAR_WIDTH // 2, 270)   # Grey (2)
    ]
    
    colors = [
        RED,  # Green
        BLUE,    # Red
        YELLOW, # Yellow
        GREY if score < 10 else GREEN,  # Grey to Blue
        GREY if score < 20 else ORANGE # Grey to Orange
    ]

    for pos, color, line in zip(circle_positions, colors, lines):
        hover = line.sidebar_rect.collidepoint(mouse_pos)  # Check for hover
        border_thickness = 5 if line.active else (3 if hover else 2)
        border_color = (255, 255, 255) if line.active else (150, 150, 150)
        
        # Draw the outer border for hover and selection
        pygame.draw.circle(screen, border_color, pos, 17, border_thickness)  # Slightly larger radius for the border
        # Draw the actual circle
        pygame.draw.circle(screen, color, pos, 15)

    # Play/Pause and Restart Buttons (Side by Side)
    play_button.center = (WIDTH + SIDEBAR_WIDTH // 4, HEIGHT - 50)
    restart_button.center = (WIDTH + (SIDEBAR_WIDTH // 4) * 3, HEIGHT - 50)

    draw_circular_button(screen, play_button, "pause" if running else "play", False)
    draw_circular_button(screen, restart_button, "restart", False)

    
def handle_sidebar_events(event, play_button, restart_button, running):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if play_button.collidepoint(event.pos):
            return not running, False
        elif restart_button.collidepoint(event.pos):
            return running, True
    return running, False

def handle_sidebar_click(lines, mouse_pos):
    """Handle user clicking on sidebar to select a line color."""
    for line in lines:
        if line.sidebar_rect.collidepoint(mouse_pos):  # Click inside circle
            for other_line in lines:
                other_line.active = False  # Deactivate all other lines
            line.active = True  # Activate the clicked line
            print(f"{line.color} line selected.")  # Debugging



def draw_temporary_line(screen, start_station, mouse_pos, active_line):
    """Draw a temporary line using the active line's color."""
    if start_station and mouse_pos and active_line:
        pygame.draw.line(screen, active_line.color, (start_station.x, start_station.y), mouse_pos, 3)

def draw_sidebar_lines(screen, lines):
    """Draw the sidebar circles for line selection."""
    for line in lines:
        color = line.color if not line.active else (255, 255, 255)  # Highlight active line
        pygame.draw.circle(screen, color, line.sidebar_center, 20)
        pygame.draw.circle(screen, BLACK, line.sidebar_center, 20, 2)  # Circle border
