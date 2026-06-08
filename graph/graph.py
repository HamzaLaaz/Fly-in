from models.connection import Connection
from models.zone import Zone, ZoneType


class Graph:
    """
    Represents an undirected graph of zones connected by connections.

    Attributes:
        zones: Dictionary mapping zone names to Zone objects.
        connections: List of connections between zones.
    """
    def __init__(self, zones: dict[str, Zone],
                 connections: list[Connection]) -> None:
        """
        Initialize a graph with zones and their connections.

        Args:
            zones: Dictionary of zone names and corresponding Zone objects.
            connections: List of connections linking zones together.
        """
        self.zones = zones
        self.connections = connections

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        """
        Return all zones directly connected to the given zone.

        Args:
            zone: The zone whose neighbors are requested.

        Returns:
            A list of neighboring Zone objects.
        """
        neighbors: list[Zone] = []
        for connection in self.connections:
            if connection.zone_a == zone:
                if connection.zone_b.zone_type != ZoneType.BLOCKED:
                    neighbors.append(connection.zone_b)
            elif connection.zone_b == zone:
                if connection.zone_a.zone_type != ZoneType.BLOCKED:
                    neighbors.append(connection.zone_a)
        return neighbors

    def get_zone(self, name: str) -> Zone | None:
        """
        Retrieve a zone by its name.

        Args:
            name: Name of the zone.

        Returns:
            The corresponding Zone object if found, otherwise None.
        """
        return self.zones.get(name)

    def get_connection(self, zone_a: Zone, zone_b: Zone) -> Connection | None:
        """
        Find the connection between two zones.

        Since the graph is undirected, the order of the zones
        does not matter.

        Args:
            zone_a: First zone.
            zone_b: Second zone.

        Returns:
            The Connection object linking the two zones, or None
            if no connection exists.
        """
        for conct in self.connections:
            if (conct.zone_a == zone_a and conct.zone_b == zone_b) or \
               (conct.zone_a == zone_b and conct.zone_b == zone_a):
                return conct
        return None
