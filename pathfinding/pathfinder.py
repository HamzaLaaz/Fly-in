from collections import deque
from models.zone import Zone
from graph.graph import Graph


class Pathfinder:
    """Finds shortest paths through the drone network."""

    def find_path(
        self,
        graph: Graph,
        start: Zone,
        end: Zone
    ) -> list[Zone]:
        """Find shortest path from start to end using BFS.

        Args:
            graph: The zone network graph.
            start: Starting zone.
            end: Destination zone.

        Returns:
            List of zones from start to end.
            Empty list if no path exists.
        """
        # 1. handle trivial case
        if start == end:
            return [start]

        # 2. initialize queue, visited, parent
        queue = deque([start])
        visited = {start}
        parent: dict[Zone, Zone | None] = {start: None}

        # 3. BFS loop
        while queue:
            current = queue.popleft()  # FIFO ✅

            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current

                    if neighbor == end:
                        # 4. reconstruct path
                        return ...

                    queue.append(neighbor)

        return []  # no path found
