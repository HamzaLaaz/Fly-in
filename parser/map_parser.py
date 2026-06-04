from models.connection import Connection
from models.zone import Zone


class ParseError(Exception):
    """Raised when the map file contains invalid syntax."""
    pass


class MapData:
    """Holds all parsed data from a map file.

    Attributes:
        nb_drones: Number of drones to simulate.
        start_zone: The starting zone.
        end_zone: The destination zone.
        zones: Dictionary of all zones by name.
        connections: List of all connections.
    """
    def __init__(
        self,
        nb_drones: int,
        start_zone: Zone,
        end_zone: Zone,
        zones: dict[str, Zone],
        connections: list[Connection]
    ) -> None:
        """Initialize MapData."""
        self.nb_drones = nb_drones
        self.start_zone = start_zone
        self.end_zone = end_zone
        self.zones = zones
        self.connections = connections


def parse_metadata(metadata_str: str) -> dict[str, str]:
    """Parse metadata block into a dictionary.

    Args:
        metadata_str: Raw metadata string like "[zone=restricted color=red]"

    Returns:
        Dictionary of key-value pairs from metadata.
    """
    if not metadata_str.strip():
        return {}
    data: dict[str, str] = {}
    cleaned = metadata_str.strip("[]")
    parts = cleaned.split(" ")

    for x in parts:
        if "=" not in x:
            raise ParseError(f"Invalid metadata format: '{x}'")
        key, value = x.split("=", 1)
        key = key.strip()
        value = value.strip()
        data[key] = value
    return data


def parse_file(name_file: str) -> MapData:
    # try:
    with open(name_file, "r") as f:
        lines = f.read()
        for i, line in enumerate(lines, start=1):
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise ParseError(f"Line {i}: missing ':' in '{line}'")
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if "hub" in key:
                j = value.find("[")
                data = parse_metadata(value[j:])
                if key == "start_hub":
                    name, x, y, _ = value.split()
                    x, y = int(x), int(y)
                    start_zone = Zone(name, x, y,
                                      data["zone"] if data["zone"] else None,
                                      data["color"] if data["color"] else None,
                                      data["max_drones"] if data["max_drones"]
                                      else None,)
                



    # except FileNotFoundError:
    #     raise ParseError("file not found or the path false")
    # except PermissionError:
    #     raise ParseError("can't read from the file")
