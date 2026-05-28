from models.zone import Zone


class Connection:
    """
    Represents a connection between two zones in the simulation.

    A connection acts like a road or tunnel linking two Zone objects.
    It has a maximum capacity that limits how many drones can use
    the connection at the same time.

    Attributes:
        zone_a (Zone):
            The first connected zone.

        zone_b (Zone):
            The second connected zone.

        max_link_capacity (int):
            Maximum number of drones allowed on the connection
            simultaneously.

        current_drones (int):
            Number of drones currently crossing the connection.
    """
    def __init__(
        self,
        zone_a: Zone,
        zone_b: Zone,
        max_link_capacity: int = 1
    ) -> None:
        """Initialize connection between two zones."""
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        self.current_drones = 0
