import heapq
from graph.graph import Graph
from models.zone import Zone


class ReservationTable:

    def __init__(self) -> None:
        self.zone_table: dict[tuple[str, int], int] = {}
        self.connection_table: dict[tuple[str, str, int], int] = {}

    def can_enter_zone(self, zone: Zone, turn: int) -> bool:

        if zone.is_start or zone.is_end:
            return True
        result = self.zone_table.get((zone.name, turn), 0)
        return result < zone.max_drones

    def reserve(self, zone: Zone, turn: int) -> None:

        key = (zone.name, turn)
        self.zone_table[key] = (self.zone_table.get(key, 0) + 1)

    def can_use_connection(
        self,
        source: Zone,
        destination: Zone,
        turn: int,
        capacity: int
    ) -> bool:

        key = self._connection_key(source, destination, turn)
        used = self.connection_table.get(key, 0)
        return used < capacity

    def reserve_connection(
        self,
        source: Zone,
        destination: Zone,
        turn: int
    ) -> None:

        key = self._connection_key(source, destination, turn)
        self.connection_table[key] = (self.connection_table.get(key, 0) + 1)

    def _connection_key(
        self,
        source: Zone,
        destination: Zone,
        turn: int
    ) -> tuple[str, str, int]:

        a = min(source.name, destination.name)
        b = max(source.name, destination.name)
        return (a, b, turn)


class Pathfinder:
    """Find shortest path using Dijkstra."""

    def find_path(
        self,
        graph: Graph,
        start: Zone,
        end: Zone,
        reservations: ReservationTable
    ) -> list[tuple[Zone, int]]:

        start_state = (start, 0)
        distances: dict[tuple[Zone, int], int] = {start_state: 0}
        previous: dict[tuple[Zone, int], tuple[Zone, int] | None] = {
            start_state: None
        }
        counter = 0
        heap: list[tuple[int, int, int, Zone]] = []
        goal_state: tuple[Zone, int] | None = None
        heapq.heappush(heap, (0, 0, counter, start))
        MAX_TIME = len(graph.zones) * 10

        while heap:
            current_cost, current_turn, _, current_zone = heapq.heappop(heap)
            if current_turn > MAX_TIME:
                continue
            state = (current_zone, current_turn)
            if current_cost > distances[state]:
                continue
            if current_zone == end:
                goal_state = state
                break

            # ---------- WAIT ACTION ----------
            wait_turn = current_turn + 1
            new_cost = current_cost + 1
            if wait_turn <= MAX_TIME:
                if reservations.can_enter_zone(current_zone, wait_turn):
                    wait_state = (current_zone, wait_turn)
                    if (
                        wait_state not in distances or
                        new_cost < distances[wait_state]
                    ):
                        distances[wait_state] = new_cost
                        previous[wait_state] = state
                        counter += 1
                        heapq.heappush(
                            heap,
                            (new_cost, wait_turn, counter, current_zone))

            # ---------- MOVE ACTIONS ----------
            for neighbor in graph.get_neighbors(current_zone):
                connection = graph.get_connection(current_zone, neighbor)
                if connection is None:
                    continue
                move_cost = neighbor.get_movement_cost()
                arrival_turn = current_turn + move_cost
                if not reservations.can_enter_zone(neighbor, arrival_turn):
                    continue
                if not reservations.can_use_connection(
                    current_zone,
                    neighbor,
                    current_turn,
                    connection.max_link_capacity
                ):
                    continue
                next_state = (neighbor, arrival_turn)
                new_cost = current_cost + move_cost

                if (
                    next_state not in distances or
                    new_cost < distances[next_state]
                ):
                    distances[next_state] = new_cost
                    previous[next_state] = state
                    counter += 1
                    heapq.heappush(
                        heap,
                        (new_cost, arrival_turn, counter, neighbor))
        if goal_state is None:
            return []

        return self._build_path(previous, goal_state)

    def _build_path(
        self,
        previous: dict[tuple[Zone, int], tuple[Zone, int] | None],
        goal_state: tuple[Zone, int]
    ) -> list[tuple[Zone, int]]:

        path: list[tuple[Zone, int]] = []
        current: tuple[Zone, int] | None = goal_state
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path
