def create_connection(station1, station2, connections):
    """Create a line connection between two stations."""
    if (station1, station2) not in connections and (station2, station1) not in connections:
        connections.append((station1, station2))
