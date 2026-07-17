from enum import Enum


class ZoneType(Enum):
    """Represents the type of a zone."""
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Zone:
    """Represents a zone in the map.

    Args:
        name: The unique name of the zone.
        x: The x-coordinate of the zone.
        y: The y-coordinate of the zone.
        zone_type: The type of the zone, controls movement cost.
        color: Optional display color for the zone.
        max_drones: Maximum number of drones allowed simultaneously.
        is_start: True if this is the starting zone.
        is_end: True if this is the destination zone.

    Attributes:
        name: Zone name.
        x: X coordinate.
        y: Y coordinate.
        zone_type: Type of the zone.
        color: Display color.
        max_drones: Maximum allowed drones.
        is_start: Whether this is the start zone.
        is_end: Whether this is the end zone.
    """
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False
    ) -> None:
        self.name = name
        self.x, self.y = x, y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end

    def get_movement_cost(self) -> int:
        """Return the turn cost to enter this zone."""
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        return 1
