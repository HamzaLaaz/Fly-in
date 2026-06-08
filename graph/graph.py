from models.connection import Connection
from models.zone import Zone


class Graph:
    def __init__(self, zones: dict[str, Zone],
                 connections: list[Zone]) -> None:
        self.zones = zones
        self.connections = connections

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        ...

    def get_zone(self, name: str) -> Zone | None:
        ...

    def get_connection(self, zone_a: Zone, zone_b: Zone) -> Connection | None:
        ...
