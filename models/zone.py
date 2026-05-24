from enum import Enum


class ZoneType(Enum):
    """Represents the type of a zone."""
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    """Represents a zone in the map.
        Args:
            name: The unique name of the zone.
            x: The x-coordinate of the zone.
            y: The y-coordinate of the zone.
            zone_type: The type of the zone.
            color: Optional display color for the zone.
            max_drones: Maximum number of drones allowed in the zone.
        Attributes:
            current_drones: Current number of drones in the zone.
    """
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1
    ) -> None:
        self.name = name
        self.x, self.y = x, y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.current_drones = 0
