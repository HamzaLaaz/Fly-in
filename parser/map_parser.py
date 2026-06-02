class ParseError(Exception):
    """Raised when the map file contains invalid syntax."""
    pass


def parse_metadata(metadata_str: str) -> dict[str, str]:
    """Parse metadata block into a dictionary.

    Args:
        metadata_str: Raw metadata string like "[zone=restricted color=red]"

    Returns:
        Dictionary of key-value pairs from metadata.
    """
    data = {}
    md = metadata_str.strip("[]").split(" ")
    for x in md:
        i = x.split("=", 1)
        if i[0].lower() == "zone":
            data["zone"] = i[1]
        elif i[0].lower() == "color":
            data["color"] = i[1]
        elif i[0].lower() == "max_drones":
            data["max_drones"] = i[1]
        else:
            raise ParseError("the map file contains invalid syntax")
