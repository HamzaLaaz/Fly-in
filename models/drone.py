from models.zone import Zone


class Drone:
    """Represents a delivery drone in the simulation.

    Args:
        drone_id: Unique identifier of the drone.
        current_zone: Current zone occupied by the drone, or None while
            travelling on a connection.
        path: Planned route as (zone, turn) pairs.

    Attributes:
        drone_id: Unique identifier of the drone.
        current_zone: Current zone occupied by the drone.
        connection: Connection currently being traversed, if any.
        path: Planned route as (zone, turn) pairs.
    """
    def __init__(
        self,
        drone_id: int,
        current_zone: Zone | None,
        path: list[tuple[Zone, int]] | None = None
    ) -> None:
        """
        Initialize a new Drone instance.
        Args:
            drone_id (int):
                Unique identifier of the drone.
            current_zone (Zone):
                Starting zone of the drone.
            path (list[tuple[Zone, int]] | None):
                Planned route consisting of (zone, turn) pairs.
                Defaults to None.
        """
        self.drone_id = drone_id
        self.current_zone: Zone | None = current_zone
        self.connection: tuple[Zone, Zone] | None = None
        self.path = path if path is not None else []
