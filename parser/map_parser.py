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
        """Initialize the parsed map data."""
        self.nb_drones = nb_drones
        self.start_zone = start_zone
        self.end_zone = end_zone
        self.zones = zones
        self.connections = connections


def parse_metadata(metadata_str: str) -> dict[str, str]:
    """Parse a metadata block into a dictionary of key-value pairs."""
    if not metadata_str.strip():
        return {}
    if not metadata_str.startswith("[") or not metadata_str.endswith("]"):
        raise ParseError("Invalid metadata brackets")
    cleaned = metadata_str[1:-1].strip()
    if "[" in cleaned or "]" in cleaned:
        raise ParseError("Metadata contains unmatched or extra brackets")
    cleaned = cleaned.replace(" =", "=")
    cleaned = cleaned.replace("= ", "=")

    # Repeat until no spaces remain around '='
    while " =" in cleaned or "= " in cleaned:
        cleaned = cleaned.replace(" =", "=")
        cleaned = cleaned.replace("= ", "=")
    tokens = cleaned.split()
    data = {}
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Case: key=value
        if "=" in token:
            key, value = token.split("=", 1)
            # Case: key=
            if value == "":
                raise ParseError(f"Missing value for metadata '{key}'")
        # Case: key = value
        else:
            if i + 2 >= len(tokens):
                raise ParseError(f"Invalid metadata format: '{token}'")
            key = token
            if tokens[i + 1] != "=":
                raise ParseError(f"Invalid metadata format: '{token}'")
            value = tokens[i + 2]
            i += 2
        if key in data:
            raise ParseError(f"Duplicate metadata '{key}'")
        data[key] = value
        i += 1
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
                if "#" in line:
                    j = line.find("#")
                    line = line[:j]
                line = line.strip()
                if not line:
                    continue
                if ":" not in line:
                    raise ParseError(f"Line {i}: missing ':' in '{line}'")
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                if not key:
                    raise ParseError(f"Line {i}: missing key before ':'")
                if not value:
                    raise ParseError(f"Line {i}: missing value after ':'")
                if key == "nb_drones":
                    if nb_drones is not None:
                        raise ParseError(f"Line {i}: Multiple nb_drones "
                                         "definitions")
                    try:
                        nb_drones = int(value)
                        if nb_drones <= 0:
                            raise ParseError(f"Line {i}: 'nb_drones' must "
                                             "be greater than 0")
                    except ValueError:
                        raise ParseError(f"Line {i}: 'nb_drones' must "
                                         "be a positive integer")
                elif key in ("hub", "start_hub", "end_hub"):
                    j = value.find("[")
                    if j != -1:
                        zone_part = value[:j].strip()
                        metadata_str = value[j:]
                    else:
                        zone_part = value.strip()
                        metadata_str = ""
                    md = parse_metadata(metadata_str)
                    allowed = {"zone", "color", "max_drones"}
                    for k in md:
                        if k not in allowed:
                            raise ParseError(f"Line {i}: Invalid metadata")
                    parts = zone_part.split()
                    if len(parts) != 3:
                        raise ParseError(f"Line {i}: invalid hub definition")
                    name = parts[0]
                    if "-" in name:
                        raise ParseError(f"Line {i}: Zone names cannot "
                                         "contain '-'")
                    if name in zones:
                        raise ParseError(f"Line {i}: duplicate "
                                         f"zone name '{name}'")
                    try:
                        x, y = int(parts[1]), int(parts[2])
                    except ValueError:
                        raise ParseError(f"Line {i}: coordinates must "
                                         "be integers")
                    for zone in zones.values():
                        if zone.x == x and zone.y == y:
                            raise ParseError(
                                f"Line {i}: another zone already "
                                f"exists at coordinates ({x}, {y})")
                    zone_type_str = md.get("zone", "normal")
                    try:
                        zone_type = ZoneType(zone_type_str)
                    except ValueError:
                        raise ParseError(f"Line {i}: invalid zone "
                                         f"type '{zone_type_str}'")
                    if key == "start_hub":
                        if start_zone is not None:
                            raise ParseError(f"Line {i}: Multiple "
                                             "start_hub definitions")
                        start_zone = Zone(
                            name, x, y,
                            zone_type,
                            md.get("color"),
                            is_start=True)
                        zones[name] = start_zone
                    elif key == "end_hub":
                        if end_zone is not None:
                            raise ParseError(f"Line {i}: Multiple "
                                             "end_hub definitions")
                        end_zone = Zone(
                            name, x, y,
                            zone_type,
                            md.get("color"),
                            is_end=True)
                        zones[name] = end_zone
                    elif key == "hub":
                        max_drones_s = md.get("max_drones")
                        try:
                            max_drones = int(max_drones_s) \
                                if max_drones_s else 1
                        except ValueError:
                            raise ParseError(f"Line {i}: max_drones"
                                             " must be an integer")
                        if max_drones <= 0:
                            raise ParseError(f"Line {i}: max_drones"
                                             " must be positive")
                        zone = Zone(
                            name, x, y,
                            zone_type,
                            md.get("color"),
                            max_drones)
                        zones[name] = zone
                    else:
                        raise ParseError(f"Line {i}: invalid zone definition")
                elif key == "connection":
                    new_lines.append((i, line))
                else:
                    raise ParseError(f"Line {i}: invalid syntax")
            for i, lin in new_lines:
                _, value = lin.split(":", 1)
                value = value.strip()
                j = value.find("[")
                if j != -1:
                    connection_part = value[:j].strip()
                    metadata_str = value[j:]
                else:
                    connection_part = value
                    metadata_str = ""
                connection_part = connection_part.replace(" -", "-")
                connection_part = connection_part.replace("- ", "-")

                while " -" in connection_part or "- " in connection_part:
                    connection_part = connection_part.replace(" -", "-")
                    connection_part = connection_part.replace("- ", "-")
                md = parse_metadata(metadata_str)
                parts = connection_part.split()
                if len(parts) != 1:
                    raise ParseError(f"Line {i}: invalid connection "
                                     "definition")
                names = parts[0]
                if "-" not in names:
                    raise ParseError(f"Line {i}: connection must be in "
                                     "the form zone1-zone2")
                parts = names.split("-")
                if len(parts) != 2:
                    raise ParseError(f"Line {i}: Invalid connection syntax")
                allowed = {"max_link_capacity"}
                for k in md:
                    if k not in allowed:
                        raise ParseError(f"Line {i}: unknown metadata '{k}'")
                zone1, zone2 = names.split("-")
                if zone1 not in zones:
                    raise ParseError(f"Line {i}: unknown zone '{zone1}'")
                if zone2 not in zones:
                    raise ParseError(f"Line {i}: unknown zone '{zone2}'")
                if zone1 == zone2:
                    raise ParseError(
                        f"Line {i}: a zone cannot connect to itself")
                for a in connections:
                    if (a.zone_a.name == zone1 and a.zone_b.name == zone2) or \
                       (a.zone_a.name == zone2 and a.zone_b.name == zone1):
                        raise ParseError(f"Line {i}: Duplicate connection "
                                         f"'{zone1}-{zone2}'")
                capacity_str = md.get("max_link_capacity")
                try:
                    m_lk_cap = int(capacity_str) if capacity_str else 1
                except ValueError:
                    raise ParseError(f"Line {i}: max_link_capacity "
                                     "must be an integer")
                if m_lk_cap <= 0:
                    raise ParseError(f"Line {i}: max_link_capacity "
                                     "must be positive")
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
        raise ParseError("File not found")
    except PermissionError:
        raise ParseError("Permission denied while reading the file")
    except OSError as e:
        raise ParseError(f"Cannot read file: {e}")
