import heapq
from graph.graph import Graph
from models.zone import Zone, ZoneType
from simulation.simulater import ReservationTable


class Pathfinder:
    """
    Finds paths for drones while respecting reservation rules.

    Uses a Dijkstra-based search with reservations to avoid
    conflicts between drones.
    """

    def find_path(
        self,
        graph: Graph,
        start: Zone,
        end: Zone,
        nb_drones: int,
        reservations: ReservationTable,
    ) -> list[tuple[str, int]]:
        """
        Find a valid path from the start zone to the end zone.

        The search respects zone capacities, connection capacities,
        restricted zones, and existing reservations.

        Args:
            graph: Graph containing all zones and connections.
            start: Starting zone.
            end: Destination zone.
            nb_drones: Total number of drones in the simulation.
            reservations: Reservation table used to avoid conflicts.

        Returns:
            A list of (zone_name, turn) pairs describing the path.
            Returns an empty list if no valid path is found.
        """
        heap: list[tuple[int, int, str, list[tuple[str, int]]]] = []
        path: list[tuple[str, int]] = []
        start_zone = start.name
        heapq.heappush(heap, (0, 0, start_zone, path))
        max_time = len(graph.zones) * nb_drones * 2
        visited: set[tuple[str, int]] = set()

        while heap:

            current_turn, _, current_zone, path = heapq.heappop(heap)
            if current_turn >= max_time:
                continue
            ob_current_zone = graph.get_object_zone(current_zone)
            if ob_current_zone is None:
                continue
            state = (current_zone, current_turn)
            if state in visited:
                continue
            new_path = path + [state]
            if current_zone == end.name:
                return new_path
            visited.add(state)
            # ---------- WAIT ACTION ----------
            wait_turn = current_turn + 1

            if (
                wait_turn <= max_time
                and reservations.can_enter_zone(ob_current_zone, wait_turn)
            ):
                priority = 0 if (
                    ob_current_zone.zone_type == ZoneType.PRIORITY) else 1
                heapq.heappush(heap, (wait_turn, priority,
                                      current_zone, new_path))

            # ---------- MOVE ACTIONS ----------

            for neighbor in graph.get_neighbors(ob_current_zone):
                arrival_turn = neighbor.get_movement_cost()
                new_turn = current_turn + arrival_turn
                neighbor_state = (neighbor.name, new_turn)
                if neighbor_state in visited:
                    continue
                connection = graph.get_connection(ob_current_zone, neighbor)
                if connection is None:
                    continue

                if not reservations.can_enter_zone(neighbor, new_turn):
                    continue
                connection_ok = True

                for t in range(current_turn + 1,
                               current_turn + arrival_turn + 1):
                    if not reservations.can_use_connection(
                        ob_current_zone,
                        neighbor,
                        t,
                        connection.max_link_capacity
                    ):
                        connection_ok = False
                        break

                if not connection_ok:
                    continue
                priority = 0 if neighbor.zone_type == ZoneType.PRIORITY else 1

                heapq.heappush(
                    heap,
                    (new_turn, priority, neighbor.name,  new_path))
        return []
