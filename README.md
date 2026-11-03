## AI-Puzzle Solver
A desktop application that solves the classic 8-puzzle using A Search* and the Manhattan Distance heuristic, with a graphical user interface built using Python and Tkinter.

# Overview
The 8-puzzle consists of a 3×3 board containing eight numbered tiles and one empty space. The goal is to move the tiles into the required order by sliding one adjacent tile into the empty space.

This project accepts an initial board configuration, checks whether it is valid and solvable, and searches for an optimal sequence of moves.

# Features
- Interactive 3×3 puzzle board using Tkinter.
- A* informed search algorithm.
- Manhattan Distance heuristic.
- Input validation for digits 0–8, each used exactly once.
- Solvability check using inversion parity.
- Load a sample puzzle or generate a solvable shuffled puzzle.
- View the solution step by step or use automatic playback.
- Display solution cost, expanded states, generated states, and execution time.
- Unit tests for core algorithm behaviour.
  
# AI Problem Formulation
Element           	Description
State              	A tuple of nine integers; 0 represents the blank
Initial state	      A valid, solvable configuration entered by the user
Goal state        	(1, 2, 3, 4, 5, 6, 7, 8, 0)
Actions           	Move the blank Up, Down, Left, or Right when legal
Transition model	  Swap the blank with the adjacent tile
Step cost	          1 per move
Search strategy	    A* Search
Heuristic         	Manhattan Distance, excluding the blank tile

# A* evaluates each state using:
f(n) = g(n) + h(n)
- g(n) is the number of moves taken from the initial state.
- h(n) is the estimated remaining cost, calculated using Manhattan Distance.
For the standard 3×3 puzzle with unit move costs, Manhattan Distance is admissible, so A* returns an optimal solution.

#Requirements
- Python 3.9 or newer
- Tkinter


# How to Run
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run: python main.py

# How to Use
1. Enter nine digits from 0 to 8, using each digit exactly once. Spaces and commas are accepted.
2. Use Load State to display the configuration.
3. Select Solve with A* to calculate the solution.
4. Use Next and Previous to navigate through the solution, or choose Auto Play.
5. Use Shuffle to generate a solvable puzzle.
   
The sample state is:
1 2 3
4 0 6
7 5 8

# ScreenShots
<img width="591" height="500" alt="Screenshot 2026-11-03 211246" src="https://github.com/user-attachments/assets/4f678ccb-fdd3-4b55-b78f-2092406365bf" />

<img width="578" height="509" alt="Screenshot 2026-11-03 211257" src="https://github.com/user-attachments/assets/0c791a1b-7da3-4742-8058-57323aaa2eb1" />


# Learning Outcomes
This project demonstrates state-space representation, legal state transitions, heuristic search, priority queues, path reconstruction, input validation, and a Python GUI.

# Limitations and Future Improvements
The current version supports the standard 3×3 8-puzzle and a fixed goal state. Possible extensions include alternative heuristics, comparisons with BFS or IDA*, configurable goal states, and support for larger sliding puzzles.

# Author
Name: Sachin Kumar

# Clone Repo
git clone https://github.com/SachinKumar-IT/ai-puzzle-solver.git
