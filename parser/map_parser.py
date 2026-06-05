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


def parse_file(file_name: str) -> MapData:
    data = {
        "nb_drones": None,
        "start_hub": None,
        "end_hub": None,
        "zones": None,
        "connections": None,
    }
    # try:
    with open(file_name, "r") as f:
        lines = f.read()
        zones = {}
        connections = []
        new_lines = []
        for i, line in enumerate(lines, start=1):
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                raise ParseError(f"Line {i}: missing ':' in '{line}'")
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "nb_drones":
                try:
                    data["nb_drones"] = int(value)
                except ValueError:
                    raise ParseError("the 'nb_drones' most be integer")
            if "hub" in key:
                j = value.find("[")
                md = parse_metadata(value[j:])
                if key == "start_hub" or key == "end_hub":
                    name, x, y, _ = value.split()
                    try:
                        x, y = int(x), int(y)
                    except ValueError:
                        raise ParseError("the x and y most be interger")
                    if key == "start_hub":
                        data["start_hub"] = Zone(
                            name, x, y,
                            md["zone"] if md["zone"] else None,
                            md["color"] if md["color"] else None,
                            md["max_drones"] if md["max_drones"] else None)
                    else:
                        data["end_hub"] = Zone(
                            name, x, y,
                            md["zone"] if md["zone"] else None,
                            md["color"] if md["color"] else None,
                            md["max_drones"] if md["max_drones"] else None)
                elif key == "hub":
                    name, x, y, _ = value.split()
                    try:
                        x, y = int(x), int(y)
                    except ValueError:
                        raise ParseError("the x and y most be interger")
                    zone = Zone(name, x, y,
                                md["zone"] if md["zone"] else None,
                                md["color"] if md["color"] else None,
                                md["max_drones"] if md["max_drones"] else None)
                    zones[name] = zone
                else:
                    raise ParseError("the line {i} in invalid ")
            elif key == "connection":
                new_lines.append(line)
            else:
                raise ParseError("the line {i} in invalid syntax")
        for lin in new_lines:
            _, value = line.split(":", 1)
            value = value.strip()
            names, _ = value.split()
            if "-" not in names:
                raise ParseError("most be in btw the names of zone '-'")
            j = value.find("[")
            md = parse_metadata(value[j:])
            zone1, zone2 = names.split("-")
            connection = Connection(zones[zone1],)

    # except FileNotFoundError:
    #     raise ParseError("file not found or the path false")
    # except PermissionError:
    #     raise ParseError("can't read from the file")
