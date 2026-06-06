from models.connection import Connection
from models.zone import Zone, ZoneType


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
    """Parse a map file and return structured map data.

    Args:
        file_name: Path to the map file.

    Returns:
        MapData object containing all parsed zones and connections.

    Raises:
        ParseError: If file is missing, unreadable, or has invalid syntax.
    """
    nb_drones: int | None = None
    start_zone: Zone | None = None
    end_zone: Zone | None = None
    zones: dict[str, Zone] = {}
    connections: list[Connection] = []
    try:
        with open(file_name, "r") as f:
            lines = f.read().splitlines()
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
                        nb_drones = int(value)
                        if nb_drones <= 0:
                            raise ParseError("'nb_drones' must"
                                             "be greater than 0")
                    except ValueError:
                        raise ParseError("the 'nb_drones' most be integer and"
                                         "great then 0")
                elif "hub" in key:
                    j = value.find("[")
                    metadata_str = value[j:] if j != -1 else ""
                    md = parse_metadata(metadata_str)
                    parts = value.split()
                    name = parts[0]
                    if name in zones:
                        raise ParseError(f"Line {i}: duplicate "
                                         f"zone name '{name}'")
                    try:
                        x, y = int(parts[1]), int(parts[2])
                    except ValueError:
                        raise ParseError("the x and y most be interger")
                    max_drones_s = md.get("max_drones")
                    max_drones = int(max_drones_s) if max_drones_s else 1
                    zone_type_str = md.get("zone", "normal")
                    try:
                        zone_type = ZoneType(zone_type_str)
                    except ValueError:
                        raise ParseError(f"Line {i}: invalid zone"
                                         f"type '{zone_type_str}'")
                    if key == "start_hub":
                        start_zone = Zone(
                            name, x, y,
                            zone_type,
                            md.get("color"),
                            max_drones)
                        zones[name] = start_zone
                    elif key == "end_hub":
                        end_zone = Zone(
                            name, x, y,
                            zone_type,
                            md.get("color"),
                            max_drones)
                        zones[name] = end_zone
                    elif key == "hub":
                        zone = Zone(
                            name, x, y,
                            zone_type,
                            md.get("color"),
                            max_drones)
                        zones[name] = zone
                    else:
                        raise ParseError(f"the line {i} in invalid ")
                elif key == "connection":
                    new_lines.append(line)
                else:
                    raise ParseError(f"the line {i} in invalid syntax")
            for lin in new_lines:
                _, value = lin.split(":", 1)
                value = value.strip()
                parts = value.split()
                names = parts[0]
                if "-" not in names:
                    raise ParseError("most be in btw the names of zone '-'")
                j = value.find("[")
                metadata_str = value[j:] if j != -1 else ""
                md = parse_metadata(metadata_str)
                zone1, zone2 = names.split("-")
                if zone1 not in zones:
                    raise ParseError(f"{zone1} there is not name  in zones")
                if zone2 not in zones:
                    raise ParseError(f"{zone2} there is not name  in zones")
                for a in connections:
                    if (a.zone_a.name == zone1 and a.zone_b.name == zone2) or \
                       (a.zone_a.name == zone2 and a.zone_b.name == zone1):
                        raise ParseError(f"Duplicate connection: "
                                         f"'{zone1}-{zone2}'")
                capacity_str = md.get("max_link_capacity")
                m_lk_cap = int(capacity_str) if capacity_str else 1
                connection = Connection(zones[zone1], zones[zone2], m_lk_cap)
                connections.append(connection)
            if nb_drones is None:
                raise ParseError("Missing 'nb_drones' line")
            if start_zone is None:
                raise ParseError("Missing 'start_hub' line")
            if end_zone is None:
                raise ParseError("Missing 'end_hub' line")
            return MapData(
                nb_drones,
                start_zone,
                end_zone,
                zones,
                connections)

    except FileNotFoundError:
        raise ParseError("file not found or the path false")
    except PermissionError:
        raise ParseError("can't read from the file")
