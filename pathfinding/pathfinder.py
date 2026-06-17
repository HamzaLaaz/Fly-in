import heapq
from models.zone import Zone, ZoneType
from graph.graph import Graph


class Pathfinder:
    """Finds shortest paths through the drone network."""

    def find_path(
        self,
        graph: Graph,
        start: Zone,
        end: Zone
    ) -> list[Zone]:
        """Find the cheapest path from start to end using Dijkstra.

        Args:
            graph: The zone network graph.
            start: Starting zone.
            end: Destination zone.

        Returns:
            List of zones from start to end (cheapest total cost).
            Empty list if no path exists.
        """
        if start == end:
            return [start]

        # distances: cost to reach each zone (start with infinity)
        distances: dict[Zone, int] = {start: 0}
        parent: dict[Zone, Zone | None] = {start: None}

        counter = 0
        heap: list[tuple[int, int, Zone]] = [(0, counter, start)]

        while heap:
            current_cost, _, current = heapq.heappop(heap)

            if current == end:
                path = []
                node: Zone | None = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return path

            for neighbor in graph.get_neighbors(current):
                if neighbor.zone_type == ZoneType.BLOCKED:
                    continue

                new_cost = current_cost + neighbor.get_movement_cost()

                # relaxation step: only update if cheaper!
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    parent[neighbor] = current
                    counter += 1
                    heapq.heappush(heap, (new_cost, counter, neighbor))

        return []
