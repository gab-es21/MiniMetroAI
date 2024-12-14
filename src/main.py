import pygame
import time
from models.stations import Station
from models.train_lines import TrainLine
from utils.constants import BORDER_MARGIN, GRID_SIZE, PASSENGER_SPAWN_INTERVAL, STATION_SPAWN_INTERVAL, WIDTH, HEIGHT, SCREEN_WIDTH, BEIGE, SIDEBAR_WIDTH
from utils.helpers import draw_passengers, load_random_map, draw_forbidden_area, draw_station, print_all_stations
from utils.game_logic import draw_grid_dots, initialize_game
from utils.sidebar import draw_sidebar, draw_temporary_line, handle_sidebar_click, handle_sidebar_events
from models.passengers import Passenger

# Initialize Pygame
pygame.init()

def main():
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
    pygame.display.set_caption("MiniMetro Simulation")

    # Initialize game state
    map_data, river_polygon = initialize_game()

    # Precompute grid points
    grid_points = [
    (x, y)
    for x in range(BORDER_MARGIN, WIDTH, GRID_SIZE)
    for y in range(BORDER_MARGIN, HEIGHT, GRID_SIZE)
]

    # Initialize stations
    stations = Station.generate_initial_stations(river_polygon, WIDTH, HEIGHT, grid_size=GRID_SIZE, sidebar_width=SIDEBAR_WIDTH)

    # Initialize train lines
    lines = [
        TrainLine((255, 0, 0)),  # Red line
        TrainLine((0, 0, 255)),  # Blue line
        TrainLine((255, 255, 0))  # Yellow line
    ]
    lines[0].set_sidebar_position((WIDTH + SIDEBAR_WIDTH // 2, 110))  # Green
    lines[1].set_sidebar_position((WIDTH + SIDEBAR_WIDTH // 2, 150))  # Red
    lines[2].set_sidebar_position((WIDTH + SIDEBAR_WIDTH // 2, 190))  # Yellow


    passengers = []  # Store passengers
    connections = []  # Store connections between stations (future implementation)

    # Clock variables
    start_time = None
    running = False
    elapsed_time = 0
    last_station_time = 0
    last_passenger_time = 0

    # Score
    score = 0  # Start score at zero

    # Sidebar buttons
    play_button = pygame.Rect(WIDTH + (SIDEBAR_WIDTH // 2) - 25, HEIGHT - 80, 50, 50)
    restart_button = pygame.Rect(WIDTH + (SIDEBAR_WIDTH // 2) - 25, HEIGHT - 150, 50, 50)

    # Temporary line drawing
    temporary_line_start = None
    temporary_mouse_pos = None

    # Main loop
    while True:
        current_time = time.time()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            running, restart_pressed = handle_sidebar_events(event, play_button, restart_button, running)
            if restart_pressed:
                main()  # Restart the game
            
                        # Handle temporary line drawing
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                handle_sidebar_click(lines, event.pos)
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                for station in stations:
                    if station.contains(event.pos):  # Start drawing line
                        temporary_line_start = station
                        break

            if event.type == pygame.MOUSEMOTION and temporary_line_start:
                temporary_mouse_pos = event.pos  # Update mouse position for temporary line

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
                if temporary_line_start:
                    for station in stations:
                        if station.contains(event.pos) and station != temporary_line_start:  # Connect stations
                            active_line = next((line for line in lines if line.active), None)
                            if active_line:
                                active_line.add_connection(temporary_line_start, station)
                            break
                    # Reset temporary line state
                    temporary_line_start = None
                    temporary_mouse_pos = None


        # Game logic: Update elapsed time
        if running:
            if start_time is None:  # Start the clock on play
                start_time = current_time
            elapsed_time = current_time - start_time

            # Add a new station every 10 seconds
            if elapsed_time - last_station_time >= STATION_SPAWN_INTERVAL:
                new_station = Station.generate_new_station(river_polygon, stations, grid_points)
                if new_station:
                    stations.append(new_station)
                    last_station_time = elapsed_time
                    print(f"New station added at ({new_station.x}, {new_station.y}) with shape: {new_station.shape}")
                    print_all_stations(stations)
                else:
                    print("No space for new station.")
            
            # Spawn new passengers every 5 seconds
            if elapsed_time - last_passenger_time >= PASSENGER_SPAWN_INTERVAL:
                # Spawn passengers for each station
                for station in stations:
                    station.draw(screen)
                    station.spawn_passenger(elapsed_time)

        # Game area
        screen.fill(BEIGE)  # Background color
        draw_forbidden_area(screen, river_polygon, stations)  # Draw forbidden areas
        for station in stations:
            draw_station(screen, station)
            draw_passengers(screen, station.passengers)

        # Draw grid dots on top of everything
        #draw_grid_dots(screen, river_polygon, stations, WIDTH, HEIGHT, grid_size=GRID_SIZE, sidebar_width=SIDEBAR_WIDTH)

        # Draw train lines
        for idx, line in enumerate(lines):
            line.draw(screen, index=idx)


        # Draw temporary line
        if temporary_line_start and temporary_mouse_pos:
            active_line = next((line for line in lines if line.active), None)
            draw_temporary_line(screen, temporary_line_start, temporary_mouse_pos, active_line)


        # Draw train lines
        for index, line in enumerate(lines):
            line.draw(screen, index=index)

        # Sidebar
        draw_sidebar(screen, elapsed_time, play_button, restart_button, running, score, lines)


        # Refresh screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
