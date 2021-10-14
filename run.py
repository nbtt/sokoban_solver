from time import time
from sokoban import Sokoban
from gui import MainApp
import tkinter as tk

def bfs_solver(filename):
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.BFS_search(state_board, 10)
    return str(board.getDirections()), "Time: " + str(sok.timerun) + " seconds" \
        + "\nSolution Length: " + str(len(str(board.getDirections()))) \
        + "\nGenerated States: " + str(sok.numNodeNewState()) \
        + "\nTraversed States: " + str(len(sok.numNodeExplored())) \
        + "\nSolution: " + str(board.getDirections())

def aStar_solver(filename):
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.aStar_search(state_board, 10)
    return str(board.getDirections()), "Time: " + str(sok.timerun) + " seconds" \
        + "\nSolution Length: " + str(len(str(board.getDirections()))) \
        + "\nGenerated States: " + str(sok.numNodeNewState()) \
        + "\nTraversed States: " + str(len(sok.numNodeExplored())) \
        + "\nSolution: " + str(board.getDirections())

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sokoban Solver")
    # Map area size
    window.columnconfigure(1, minsize=550)
    app = MainApp(window, bfs_solver, aStar_solver)
    window.resizable(False, False)
    window.mainloop()