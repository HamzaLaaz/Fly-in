import heapq

from graph.graph import Graph
from models.zone import Zone, ZoneType


class Pathfinder:
    """Find shortest path using Dijkstra."""

    def find_path(
        self,
        graph: Graph,
        start: Zone,
        end: Zone
    ) -> list[Zone]:

        distances: dict[Zone, int] = {
            zone: float("inf") for zone in graph.zones.values()
        }
        previous: dict[Zone, Zone | None] = {
            zone: None for zone in graph.zones.values()
        }
        distances[start] = 0
        counter = 0
        heap: list[tuple[int, int, Zone]] = []
        heapq.heappush(heap, (0, counter, start))

        while heap:
            current_cost, _, current_zone = heapq.heappop(heap)

            if current_zone == end:
                break
            for neighbor in graph.get_neighbors(current_zone):
                if neighbor.zone_type == ZoneType.RESTRICTED:
                    move_cost = 2
                else:
                    move_cost = 1
                new_cost = current_cost + move_cost
                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current_zone
                    counter += 1
                    heapq.heappush(heap, (new_cost, counter, neighbor))

        return self._build_path(previous, start, end)

    def _build_path(
        self,
        previous: dict[Zone, Zone | None],
        start: Zone,
        end: Zone
    ) -> list[Zone]:

        path: list[Zone] = []
        current: Zone | None = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        if path[0] != start:
            return []

        return path
