from sokoban import Sokoban
from gui import MainApp
import tkinter as tk

def bfs_solver(filename):
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.search(state_board)
    return str(board.getDirections()), "Log BFS\nJust testing..."

def aStar_solver(filename):
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.aStar_search(state_board)
    return str(board.getDirections()), "Log BFS\nJust testing..."

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sokoban Solver")
    # Map area size
    window.columnconfigure(1, minsize=550)
    app = MainApp(window, bfs_solver, aStar_solver)
    window.resizable(False, False)
    window.mainloop()