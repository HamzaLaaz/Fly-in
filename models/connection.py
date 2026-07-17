from models.zone import Zone


class Connection:
    """Represents a bidirectional connection between two zones.

    Args:
        zone_a: First connected zone.
        zone_b: Second connected zone.
        max_link_capacity: Maximum number of drones that may use the
            connection simultaneously.

    Attributes:
        zone_a: First connected zone.
        zone_b: Second connected zone.
        max_link_capacity: Maximum number of drones allowed
            simultaneously.
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
