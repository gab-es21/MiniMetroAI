import pygame


class Train:
    def __init__(self, line, capacity=6):
        self.line = line  # TrainLine object
        self.capacity = capacity  # Max passengers
        self.passengers = []  # Passengers on the train
        self.current_station_index = 0  # Index in the line's stations list

    def move(self):
        """Move the train to the next station on the line."""
        if len(self.line.stations) > 1:
            self.current_station_index = (self.current_station_index + 1) % len(self.line.stations)

    def pick_up_passengers(self, station):
        """Pick up passengers from a station."""
        while len(self.passengers) < self.capacity and station.passengers:
            passenger = station.passengers.pop(0)  # Oldest passenger first
            if passenger.shape in [s.shape for s in self.line.stations]:
                self.passengers.append(passenger)
                print(f"Passenger picked up from {station.shape} at ({station.x}, {station.y})")

    def drop_off_passengers(self, station):
        """Drop off passengers at their destination."""
        remaining_passengers = []
        for passenger in self.passengers:
            if passenger.shape == station.shape:
                print(f"Passenger dropped off at {station.shape} at ({station.x}, {station.y})")
            else:
                remaining_passengers.append(passenger)
        self.passengers = remaining_passengers

    def draw(self, screen):
        """Draw the train at its current station."""
        current_station = self.line.stations[self.current_station_index]
        pygame.draw.circle(screen, self.line.color, (current_station.x, current_station.y), 10)  # Train size
