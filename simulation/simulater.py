from graph.graph import Graph
from models.zone import Zone


class ReservationTable:
    """
    Tracks reserved zones and connections during pathfinding.

    Reservations prevent drones from occupying the same zone or
    using the same connection beyond its capacity at a given turn.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initialize an empty reservation table.

        Args:
            graph: Graph containing all zones and connections.
        """
        self.graph = graph
        self.zone_table: dict[tuple[str, int], int] = {}
        self.connection_table: dict[tuple[str, str, int], int] = {}

    def can_enter_zone(self, zone: Zone, turn: int) -> bool:
        """
        Check whether a drone may enter a zone at a given turn.

        Start and end zones have unlimited capacity.

        Args:
            zone: Zone to check.
            turn: Simulation turn.

        Returns:
            True if the zone has available capacity, otherwise False.
        """
        if zone.is_start or zone.is_end:
            return True
        result = self.zone_table.get((zone.name, turn), 0)
        return result < zone.max_drones

    def reserve(self, zone: str, turn: int) -> None:
        """
        Reserve a zone for a specific turn.

        Args:
            zone: Name of the zone to reserve.
            turn: Simulation turn.
        """
        key = (zone, turn)
        self.zone_table[key] = (self.zone_table.get(key, 0) + 1)

    def can_use_connection(
        self,
        c_zone: Zone,
        n_zone: Zone,
        turn: int,
        capacity: int
    ) -> bool:
        """
        Check whether a connection may be used at a given turn.

        Args:
            c_zone: Current zone.
            n_zone: Destination zone.
            turn: Simulation turn.
            capacity: Maximum connection capacity.

        Returns:
            True if the connection has available capacity,
            otherwise False.
        """
        key = self._connection_key(c_zone, n_zone, turn)
        used = self.connection_table.get(key, 0)
        return used < capacity

    def reserve_connection(
        self,
        c_zone: str,
        n_zone: str,
        turn: int
    ) -> None:
        """
        Reserve a connection for a specific turn.

        Args:
            c_zone: Name of the starting zone.
            n_zone: Name of the destination zone.
            turn: Simulation turn.
        """
        obj_c_zone = self.graph.get_object_zone(c_zone)
        obj_n_zone = self.graph.get_object_zone(n_zone)
        if obj_c_zone is None or obj_n_zone is None:
            return
        key = self._connection_key(obj_c_zone, obj_n_zone, turn)
        self.connection_table[key] = (self.connection_table.get(key, 0) + 1)

    def _connection_key(
        self,
        c_zone: Zone,
        n_zone: Zone,
        turn: int
    ) -> tuple[str, str, int]:
        """
        Build a unique key for a connection reservation.

        The order of the zones does not matter because
        connections are undirected.

        Args:
            c_zone: First connected zone.
            n_zone: Second connected zone.
            turn: Simulation turn.

        Returns:
            A tuple identifying the connection and turn.
        """
        a = min(c_zone.name, n_zone.name)
        b = max(c_zone.name, n_zone.name)
        return (a, b, turn)
