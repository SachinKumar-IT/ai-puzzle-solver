"""Tkinter graphical interface for the AI 8-Puzzle Solver."""
from __future__ import annotations

import random
import time
import tkinter as tk
from tkinter import messagebox, ttk

from algorithm import GOAL_STATE, is_solvable, solve_astar, validate_state

DEFAULT_STATE = (1, 2, 3, 4, 0, 6, 7, 5, 8)


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 8-Puzzle Solver | A* Search")
        self.root.geometry("780x690")
        self.root.minsize(680, 620)
        self.root.configure(bg="#f3f6fb")

        self.current_state = DEFAULT_STATE
        self.solution = None
        self.step_index = 0
        self.playing = False
        self.after_id = None
        self.tile_buttons = []

        self._build_ui()
        self._render_state(self.current_state)
        self._set_status("Ready. Enter a puzzle or use the sample state.")

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", font=("Segoe UI", 10), padding=7)
        style.configure("TLabel", background="#f3f6fb", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 21, "bold"),
                        foreground="#17365d")
        style.configure("Sub.TLabel", font=("Segoe UI", 10),
                        foreground="#53657d")

        outer = tk.Frame(self.root, bg="#f3f6fb", padx=24, pady=18)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="AI 8-Puzzle Solver", style="Header.TLabel").pack()
        ttk.Label(
            outer,
            text="Solve the sliding-tile puzzle with A* search and Manhattan distance",
            style="Sub.TLabel"
        ).pack(pady=(4, 15))

        input_frame = tk.LabelFrame(
            outer, text=" Initial State (use digits 0–8; 0 is the blank) ",
            bg="#f3f6fb", fg="#17365d", font=("Segoe UI", 10, "bold"),
            padx=12, pady=10
        )
        input_frame.pack(fill="x", pady=5)
        self.input_var = tk.StringVar(value="123406758")
        entry = ttk.Entry(input_frame, textvariable=self.input_var,
                          font=("Consolas", 15), justify="center", width=18)
        entry.pack(side="left", padx=(4, 12))
        ttk.Button(input_frame, text="Load State", command=self.load_state).pack(side="left", padx=3)
        ttk.Button(input_frame, text="Sample", command=self.load_sample).pack(side="left", padx=3)
        ttk.Button(input_frame, text="Shuffle", command=self.shuffle_state).pack(side="left", padx=3)

        board_wrap = tk.Frame(outer, bg="#f3f6fb")
        board_wrap.pack(pady=15)
        self.board = tk.Frame(board_wrap, bg="#d9e2ef", padx=7, pady=7)
        self.board.pack()
        for i in range(9):
            button = tk.Label(
                self.board, text="", width=5, height=2,
                font=("Segoe UI", 25, "bold"),
                bg="#ffffff", fg="#17365d",
                relief="flat", bd=0
            )
            button.grid(row=i // 3, column=i % 3, padx=4, pady=4, ipadx=7, ipady=4)
            self.tile_buttons.append(button)

        controls = tk.Frame(outer, bg="#f3f6fb")
        controls.pack(pady=5)
        ttk.Button(controls, text="Solve with A*", command=self.solve).grid(row=0, column=0, padx=4)
        ttk.Button(controls, text="Previous", command=self.previous_step).grid(row=0, column=1, padx=4)
        ttk.Button(controls, text="Next", command=self.next_step).grid(row=0, column=2, padx=4)
        ttk.Button(controls, text="Auto Play", command=self.auto_play).grid(row=0, column=3, padx=4)
        ttk.Button(controls, text="Reset", command=self.reset).grid(row=0, column=4, padx=4)

        self.step_var = tk.StringVar(value="Step: 0 / 0")
        ttk.Label(outer, textvariable=self.step_var).pack(pady=(8, 2))
        self.status_var = tk.StringVar()
        status = tk.Label(
            outer, textvariable=self.status_var, bg="#e7eef8",
            fg="#17365d", font=("Segoe UI", 10), padx=10, pady=9,
            wraplength=680, justify="left"
        )
        status.pack(fill="x", pady=7)

        metrics = tk.LabelFrame(
            outer, text=" Search Performance ", bg="#f3f6fb",
            fg="#17365d", font=("Segoe UI", 10, "bold"), padx=10, pady=8
        )
        metrics.pack(fill="x", pady=5)
        self.metrics_var = tk.StringVar(
            value="Moves: —     Expanded states: —     Generated states: —     Time: —"
        )
        tk.Label(metrics, textvariable=self.metrics_var, bg="#f3f6fb",
                 fg="#26384d", font=("Segoe UI", 10)).pack()

        ttk.Label(
            outer,
            text="AI method: A* Search     Heuristic: Manhattan Distance     Cost per move: 1",
            style="Sub.TLabel"
        ).pack(pady=(9, 0))

    def _render_state(self, state):
        for i, value in enumerate(state):
            button = self.tile_buttons[i]
            if value == 0:
                button.configure(text="", bg="#cbd5e1", relief="sunken")
            else:
                button.configure(text=str(value), bg="#ffffff", relief="flat")
        self.step_var.set(
            f"Step: {self.step_index} / {len(self.solution['path']) - 1}"
            if self.solution else "Step: 0 / 0"
        )

    def _set_status(self, message):
        self.status_var.set(message)

    def _stop_auto(self):
        self.playing = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def load_state(self):
        self._stop_auto()
        raw = self.input_var.get().replace(",", "").replace(" ", "")
        try:
            state = validate_state(raw)
        except ValueError as exc:
            messagebox.showerror("Invalid puzzle", str(exc))
            return
        self.current_state = state
        self.solution = None
        self.step_index = 0
        self._render_state(state)
        self.metrics_var.set("Moves: —     Expanded states: —     Generated states: —     Time: —")
        if is_solvable(state):
            self._set_status("Valid and solvable initial state loaded.")
        else:
            self._set_status("This configuration is not solvable for the standard 8-puzzle goal.")

    def load_sample(self):
        self.input_var.set("123406758")
        self.load_state()

    def shuffle_state(self):
        self._stop_auto()
        state = GOAL_STATE
        previous = None
        for _ in range(24):
            choices = [(s, m) for s, m in __import__("algorithm").get_neighbors(state)
                       if s != previous]
            next_state, _ = random.choice(choices)
            previous, state = state, next_state
        self.input_var.set("".join(map(str, state)))
        self.load_state()

    def solve(self):
        self._stop_auto()
        try:
            state = validate_state(self.input_var.get().replace(",", "").replace(" ", ""))
        except ValueError as exc:
            messagebox.showerror("Invalid puzzle", str(exc))
            return
        if not is_solvable(state):
            self.solution = None
            self._set_status("No solution exists: inversion count is odd.")
            messagebox.showwarning("Unsolvable puzzle", "This state cannot reach the standard goal state.")
            return

        self.current_state = state
        start_time = time.perf_counter()
        result = solve_astar(state)
        elapsed = time.perf_counter() - start_time
        if result is None:
            self._set_status("No solution was found.")
            return
        self.solution = result
        self.step_index = 0
        self.current_state = result["path"][0]
        self._render_state(self.current_state)
        self.metrics_var.set(
            f"Moves: {result['cost']}     Expanded states: {result['expanded']}     "
            f"Generated states: {result['generated']}     Time: {elapsed:.6f} s"
        )
        if result["cost"] == 0:
            self._set_status("The initial state is already the goal state.")
        else:
            self._set_status(
                f"Solution found! First move: {result['moves'][0]}. "
                f"Optimal path contains {result['cost']} moves."
            )

    def next_step(self):
        self._stop_auto()
        if not self.solution:
            self._set_status("Click 'Solve with A*' before stepping through a solution.")
            return
        if self.step_index < len(self.solution["path"]) - 1:
            self.step_index += 1
            self.current_state = self.solution["path"][self.step_index]
            self._render_state(self.current_state)
            move = self.solution["moves"][self.step_index - 1]
            self._set_status(f"Move {self.step_index}: blank moved {move}.")
        if self.step_index == len(self.solution["path"]) - 1:
            self._set_status("Goal reached. Puzzle solved successfully!")

    def previous_step(self):
        self._stop_auto()
        if self.solution and self.step_index > 0:
            self.step_index -= 1
            self.current_state = self.solution["path"][self.step_index]
            self._render_state(self.current_state)
            self._set_status("Moved one step backward in the solution path.")

    def auto_play(self):
        if not self.solution:
            self.solve()
        if not self.solution or self.step_index >= len(self.solution["path"]) - 1:
            return
        self._stop_auto()
        self.playing = True

        def advance():
            if not self.playing:
                return
            if self.step_index < len(self.solution["path"]) - 1:
                self.step_index += 1
                self.current_state = self.solution["path"][self.step_index]
                self._render_state(self.current_state)
                self._set_status(
                    f"Auto play: step {self.step_index} of {len(self.solution['moves'])}."
                )
                self.after_id = self.root.after(550, advance)
            else:
                self.playing = False
                self.after_id = None
                self._set_status("Goal reached. Puzzle solved successfully!")
        advance()

    def reset(self):
        self._stop_auto()
        self.load_sample()
        self._set_status("Puzzle reset to the sample initial state.")


def main():
    root = tk.Tk()
    PuzzleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
