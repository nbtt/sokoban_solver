from time import time
from sokoban import Sokoban
from gui import MainApp
import tkinter as tk

def bfs_solver(filename):
    start = time()
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.BFS_search(state_board)
    end = time()
    return str(board.getDirections()), "Time: " + str(end - start) + "\nLength: " + str(len(str(board.getDirections()))) + "\nGenerated States: " + str(sok.numNodeNewState()) + "\nTraversed States: " + str(len(sok.numNodeExplored()))

def aStar_solver(filename):
    start = time()
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.aStar_search(state_board)
    end = time()
    return str(board.getDirections()), "Time: " + str(end - start) + "\nLength: " + str(len(str(board.getDirections()))) + "\nGenerated States: " + str(sok.numNodeNewState()) + "\nTraversed States: " + str(len(sok.numNodeExplored()))

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sokoban Solver")
    # Map area size
    window.columnconfigure(1, minsize=550)
    app = MainApp(window, bfs_solver, aStar_solver)
    window.resizable(False, False)
    window.mainloop()