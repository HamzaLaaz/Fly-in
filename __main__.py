import sys

from parser.map_parser import parse_file, ParseError
from graph.graph import Graph
from models.zone import Zone
from models.drone import Drone
from pathfinding.pathfinder import Pathfinder
from simulation.simulater import ReservationTable
from visualization.visualizer import VisualizerPrint
from visualization.pg_visualizer import Visualizer


def convert_name_zone_to_obj(
    path: list[tuple[str, int]],
    graph: Graph
) -> list[tuple[Zone, int]]:
    """
    Convert a path of zone names into Zone objects.

    Args:
        path: Path represented as (zone_name, turn) pairs.
        graph: Graph containing all zones.

    Returns:
        A path represented as (Zone, turn) pairs.
    """
    new_path = []
    for zone_name, turn in path:
        obj_zone = graph.get_object_zone(zone_name)
        if obj_zone is None:
            continue
        new_path.append((obj_zone, turn))
    return new_path


def main() -> None:
    """
    Run the Fly-in simulation.

    Parses the input map, computes reservation-aware paths for all
    drones, prints the simulation in the terminal, and launches the
    pygame visualizer.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 __main__.py <map_file>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        data = parse_file(filename)
    except ParseError as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)

    graph = Graph(data.zones, data.connections)
    reservations = ReservationTable(graph)
    pathfinder = Pathfinder()
    visualizer = VisualizerPrint()

    total_turns = 0
    all_paths: list[list[tuple[Zone, int]]] = []

    for drone_id in range(1, data.nb_drones + 1):
        path = pathfinder.find_path(
            graph,
            data.start_zone,
            data.end_zone,
            data.nb_drones,
            reservations
        )
        obj_path = convert_name_zone_to_obj(path, graph)

        if not path:
            print(f"Drone {drone_id}: No path found")
            continue

        all_paths.append(obj_path)

        finish_turn = path[-1][1]
        total_turns = max(total_turns, finish_turn)
        for i, (zone, turn) in enumerate(path):
            reservations.reserve(zone, turn)
            if i == 0:
                continue
            prev_zone, _ = path[i - 1]
            if zone == prev_zone:
                continue
            obj_zone = graph.get_object_zone(zone)
            if obj_zone is None:
                continue
            movement_cost = obj_zone.get_movement_cost()
            for t in range(turn - movement_cost + 1, turn + 1):
                reservations.reserve_connection(
                    prev_zone,
                    zone,
                    t
                )

    visualizer.print_simulation(all_paths, total_turns)

    # Create Drone objects for the pygame visualizer
    drones: list[Drone] = []

    for drone_id, drone_path in enumerate(all_paths, start=1):

        drone = Drone(
            drone_id=drone_id,
            current_zone=data.start_zone,
            path=drone_path,
        )
        drones.append(drone)

    # Launch pygame visualizer
    pg_visualizer = Visualizer(graph, drones, total_turns)

    pg_visualizer.run()


if __name__ == "__main__":
    main()
