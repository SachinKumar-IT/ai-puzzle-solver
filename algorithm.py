"""
A* search implementation for the 8-puzzle.
State format: a tuple of nine integers; 0 represents the blank tile.
"""
from __future__ import annotations

from heapq import heappush, heappop
from itertools import count
from typing import Dict, List, Optional, Tuple

State = Tuple[int, ...]
GOAL_STATE: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVE_ORDER = ("Up", "Down", "Left", "Right")


def validate_state(values) -> State:
    """Validate and return a 9-element permutation of 0..8."""
    try:
        state = tuple(int(v) for v in values)
    except (TypeError, ValueError):
        raise ValueError("Enter exactly nine integers from 0 to 8.")
    if len(state) != 9:
        raise ValueError("A puzzle must contain exactly nine values.")
    if set(state) != set(range(9)):
        raise ValueError("Use every digit from 0 to 8 exactly once.")
    return state


def inversion_count(state: State) -> int:
    """Count inversions after excluding the blank."""
    tiles = [x for x in state if x != 0]
    return sum(
        1 for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )


def is_solvable(state: State) -> bool:
    """For a 3x3 puzzle, an even inversion count is solvable."""
    return inversion_count(state) % 2 == 0


def manhattan_distance(state: State, goal: State = GOAL_STATE) -> int:
    """Sum each numbered tile's Manhattan distance from its goal cell."""
    goal_positions = {tile: divmod(index, 3) for index, tile in enumerate(goal)}
    total = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        row, col = divmod(index, 3)
        goal_row, goal_col = goal_positions[tile]
        total += abs(row - goal_row) + abs(col - goal_col)
    return total


def get_neighbors(state: State):
    """
    Yield (next_state, move_name) for each legal blank movement.
    Move names describe the direction in which the blank moves.
    """
    blank = state.index(0)
    row, col = divmod(blank, 3)
    swaps = []
    if row > 0:
        swaps.append((blank - 3, "Up"))
    if row < 2:
        swaps.append((blank + 3, "Down"))
    if col > 0:
        swaps.append((blank - 1, "Left"))
    if col < 2:
        swaps.append((blank + 1, "Right"))

    for target, move in swaps:
        new_state = list(state)
        new_state[blank], new_state[target] = new_state[target], new_state[blank]
        yield tuple(new_state), move


def solve_astar(start, goal: State = GOAL_STATE):
    """
    Find an optimal path using A* and Manhattan distance.

    Returns a dictionary with:
      path: list of states, including start and goal
      moves: list of blank movement names
      expanded: number of states removed from the frontier and expanded
      generated: number of successor states considered
      cost: optimal number of moves
    Returns None for an unsolvable state.
    """
    start = validate_state(start)
    goal = validate_state(goal)
    if not is_solvable(start) or not is_solvable(goal):
        return None
    if start == goal:
        return {
            "path": [start], "moves": [], "expanded": 0,
            "generated": 0, "cost": 0
        }

    serial = count()
    frontier = []
    g_score: Dict[State, int] = {start: 0}
    parent: Dict[State, Tuple[Optional[State], Optional[str]]] = {
        start: (None, None)
    }
    heappush(frontier, (manhattan_distance(start, goal), 0, next(serial), start))
    expanded = 0
    generated = 0

    while frontier:
        f, current_g, _, current = heappop(frontier)
        if current_g != g_score.get(current):
            continue  # Ignore an outdated priority-queue entry.

        if current == goal:
            states: List[State] = []
            moves: List[str] = []
            cursor = current
            while cursor is not None:
                states.append(cursor)
                previous, move = parent[cursor]
                if move is not None:
                    moves.append(move)
                cursor = previous
            states.reverse()
            moves.reverse()
            return {
                "path": states,
                "moves": moves,
                "expanded": expanded,
                "generated": generated,
                "cost": len(moves),
            }

        expanded += 1
        for neighbor, move in get_neighbors(current):
            generated += 1
            tentative_g = current_g + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = (current, move)
                h = manhattan_distance(neighbor, goal)
                heappush(
                    frontier,
                    (tentative_g + h, tentative_g, next(serial), neighbor)
                )

    return None
