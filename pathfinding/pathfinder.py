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
        """Find shortest path from start to end using BFS."""

        if start == end:
            return [start]

        queue = deque([start])
        visited = {start}
        parent: dict[Zone, Zone | None] = {start: None}

        while queue:
            current = queue.popleft()

            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current

                    if neighbor == end:
                        path = []
                        node = end
                        while node is not None:
                            path.append(node)
                            node = parent[node]

                        path.reverse()
                        return path

                    queue.append(neighbor)

        return []
