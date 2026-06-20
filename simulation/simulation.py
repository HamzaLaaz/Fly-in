from graph.graph import Graph
from models.drone import Drone, DroneStatus


class Simulation:
    """Runs the turn-by-turn drone movement simulation."""

    MAX_TURNS = 1000  # safety limit, not a target

    def __init__(
        self,
        graph: Graph,
        drones: list[Drone]
    ) -> None:
        """Initialize the simulation.

        Args:
            graph: The zone network graph.
            drones: List of drones to simulate.
        """
        self.graph = graph
        self.drones = drones
        self.turn = 0

    def all_delivered(self) -> bool:
        """Check if every drone has reached the end zone."""
        return all(drone.status == DroneStatus.DELIVERED
                   for drone in self.drones)

    def run(self) -> list[list[str]]:
        """Run the simulation until all drones are delivered.

        Returns:
            A list of turns, where each turn is a list of movement
            strings like "D1-roof1".
        """
        all_turns: list[list[str]] = []
        while not self.all_delivered() and self.turn < self.MAX_TURNS:
            self.turn += 1
            turn_movements: list[str] = []
            for drone in self.drones:
                if drone.status == DroneStatus.DELIVERED:
                    continue
                next_index = drone.path_index + 1
                next_zone = drone.path[next_index]
                drone.path_index = next_index
                drone.current_zone = next_zone
                if drone.path_index >= len(drone.path) - 1:
                    drone.status = DroneStatus.DELIVERED
                else:
                    drone.status = DroneStatus.FLYING
                turn_movements.append(f"D{drone.drone_id}-{next_zone.name}")

            all_turns.append(turn_movements)

        return all_turns
