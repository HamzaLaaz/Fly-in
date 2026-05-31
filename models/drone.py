from enum import Enum
from models.zone import Zone


class DroneStatus(Enum):
    """
    Represents the possible states of a drone during the simulation.
    """
    WAITING = "waiting"
    FLYING = "flying"
    DELIVERED = "delivered"


class Drone:
    """
    Represents a delivery drone in the simulation.
    A drone has a unique identifier, a current location, a planned
    path of zones to traverse, and a status indicating its current
    activity.
    Attributes:
        id (int):
            Unique identifier of the drone.
        current_zone (Zone):
            The zone where the drone is currently located.
        path (list[Zone]):
            Ordered list of zones that the drone will follow.
        status (DroneStatus):
            Current state of the drone.
    """
    def __init__(
        self,
        drone_id: int,
        current_zone: Zone,
        path: list[Zone] | None = None,
        status: DroneStatus = DroneStatus.WAITING,
    ) -> None:
        """
        Initialize a new Drone instance.
        Args:
            id (int):
                Unique identifier of the drone.
            current_zone (Zone):
                Starting zone of the drone.
            path (list[Zone] | None, optional):
                Planned route for the drone. If None, an empty path
                is created. Defaults to None.
            status (DroneStatus, optional):
                Initial status of the drone.
                Defaults to DroneStatus.WAITING.
        """
        self.drone_id = drone_id
        self.current_zone = current_zone
        self.path = path if path is not None else []
        self.status = status
