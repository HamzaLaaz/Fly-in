from models.zone import Zone


class VisualizerPrint:
    """Handles terminal output for the simulation."""

    def print_simulation(
        self,
        all_paths: list[list[tuple[Zone, int]]],
        total_turns: int,
    ) -> None:
        """
        Print the complete simulation turn by turn.

        Args:
            all_paths: Paths followed by all drones.
            total_turns: Total number of turns in the simulation.
        """

        movements_by_turn: dict[int, list[str]] = {}

        for drone_id, path in enumerate(all_paths, start=1):
            for i, (zone, turn) in enumerate(path):
                if i == 0:
                    continue

                prev_zone, _ = path[i - 1]

                if zone == prev_zone:
                    continue

                if zone.get_movement_cost() == 2:
                    if turn - 1 not in movements_by_turn:
                        movements_by_turn[turn - 1] = []

                    movements_by_turn[turn - 1].append(
                        f"D{drone_id}-{prev_zone.name}-{zone.name}"
                    )

                if turn not in movements_by_turn:
                    movements_by_turn[turn] = []

                movements_by_turn[turn].append(
                    f"D{drone_id}-{zone.name}"
                )

        for turn in sorted(movements_by_turn):
            self.print_turn(turn, movements_by_turn[turn])

        self.print_summary(total_turns)

    def print_turn(self, turn: int, movements: list[str],) -> None:
        """
        Print all drone movements for one simulation turn.

        Args:
            turn: Current simulation turn.
            movements: Drone movements performed during the turn.
        """
        print(f"Turn {turn}: {' '.join(movements)}")

    def print_summary(self, total_turns: int) -> None:
        """
        Print the total number of turns.

        Args:
            total_turns: Total turns required to finish the simulation.
        """
        print(f"\nTotal turns: {total_turns}")
