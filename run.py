from time import time
from sokoban import Sokoban
from gui import MainApp
import tkinter as tk

def bfs_solver(filename):
    sok = Sokoban()
    state_board = sok.new_board(filename)
<<<<<<< HEAD
    board = sok.search(state_board)
    end = time()
    return str(board.getDirections()), "Time: " + str(end - start) + "\nLength: " + str(len(str(board.getDirections())))
=======
    board = sok.BFS_search(state_board, 10)
    return str(board.getDirections()), "Time: " + str(sok.timerun) + " seconds" \
        + "\nSolution Length: " + str(len(str(board.getDirections()))) \
        + "\nGenerated States: " + str(sok.numNodeNewState()) \
        + "\nTraversed States: " + str(len(sok.numNodeExplored())) \
        + "\nSolution: " + str(board.getDirections())
>>>>>>> 07a32ee2519cbfb8156b68a380f054fbaee68904

def aStar_solver(filename):
    sok = Sokoban()
    state_board = sok.new_board(filename)
<<<<<<< HEAD
    board = sok.aStar_search(state_board)
    end = time()
    return str(board.getDirections()), "Time: " + str(end - start) + "\nLength: " + str(len(str(board.getDirections())))
=======
    board = sok.aStar_search(state_board, 10)
    return str(board.getDirections()), "Time: " + str(sok.timerun) + " seconds" \
        + "\nSolution Length: " + str(len(str(board.getDirections()))) \
        + "\nGenerated States: " + str(sok.numNodeNewState()) \
        + "\nTraversed States: " + str(len(sok.numNodeExplored())) \
        + "\nSolution: " + str(board.getDirections())
>>>>>>> 07a32ee2519cbfb8156b68a380f054fbaee68904

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sokoban Solver")
    # Map area size
    window.columnconfigure(1, minsize=550)
    app = MainApp(window, bfs_solver, aStar_solver)
    window.resizable(False, False)
    window.mainloop()