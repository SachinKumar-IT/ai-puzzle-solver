import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from algorithm import (
    GOAL_STATE, get_neighbors, inversion_count, is_solvable,
    manhattan_distance, solve_astar, validate_state
)


class TestEightPuzzle(unittest.TestCase):
    def test_validation(self):
        self.assertEqual(validate_state("123456780"), GOAL_STATE)
        with self.assertRaises(ValueError):
            validate_state("12345677")
        with self.assertRaises(ValueError):
            validate_state("123456789")

    def test_goal_heuristic(self):
        self.assertEqual(manhattan_distance(GOAL_STATE), 0)

    def test_sample_solution_is_optimal(self):
        start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
        result = solve_astar(start)
        self.assertEqual(result["cost"], 2)
        self.assertEqual(result["path"][0], start)
        self.assertEqual(result["path"][-1], GOAL_STATE)

    def test_unsolvable_state(self):
        unsolvable = (1, 2, 3, 4, 5, 6, 8, 7, 0)
        self.assertFalse(is_solvable(unsolvable))
        self.assertIsNone(solve_astar(unsolvable))

    def test_neighbors_are_legal(self):
        neighbors = list(get_neighbors(GOAL_STATE))
        self.assertEqual(len(neighbors), 2)  # blank is bottom-right
        for state, _ in neighbors:
            self.assertEqual(sorted(state), list(range(9)))

    def test_inversion_count(self):
        self.assertEqual(inversion_count(GOAL_STATE), 0)


if __name__ == "__main__":
    unittest.main()
