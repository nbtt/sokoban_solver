from time import time
from sokoban import Sokoban
from gui import MainApp
import tkinter as tk

def bfs_solver(filename, max_time):
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.BFS_search(state_board, max_time)
    if str(board.getDirections()) == 'Not Found':
        return str(board.getDirections()), "Time: " + str(round(sok.time_newstate_explored[0], 3)) + " seconds" \
            + "\nSolution Length: " + '0' \
            + "\nGenerated States: " + str(sok.time_newstate_explored[1]) \
            + "\nTraversed States: " + str(sok.time_newstate_explored[2]) \
            + "\nSolution: " + str(board.getDirections())
    return str(board.getDirections()), "Time: " + str(round(sok.time_newstate_explored[0], 3)) + " seconds" \
        + "\nSolution Length: " + str(len(str(board.getDirections()))) \
        + "\nGenerated States: " + str(sok.time_newstate_explored[1]) \
        + "\nTraversed States: " + str(sok.time_newstate_explored[2]) \
        + "\nSolution: " + str(board.getDirections())

def aStar_solver(filename, max_time):
    sok = Sokoban()
    state_board = sok.new_board(filename)
    board = sok.aStar_search(state_board, max_time)
    if str(board.getDirections()) == 'Not Found':
        return str(board.getDirections()), "Time: " + str(round(sok.time_newstate_explored[0], 3)) + " seconds" \
            + "\nSolution Length: " + '0' \
            + "\nGenerated States: " + str(sok.time_newstate_explored[1]) \
            + "\nTraversed States: " + str(sok.time_newstate_explored[2]) \
            + "\nSolution: " + str(board.getDirections())
    return str(board.getDirections()), "Time: " + str(round(sok.time_newstate_explored[0], 3)) + " seconds" \
        + "\nSolution Length: " + str(len(str(board.getDirections()))) \
        + "\nGenerated States: " + str(sok.time_newstate_explored[1]) \
        + "\nTraversed States: " + str(sok.time_newstate_explored[2]) \
        + "\nSolution: " + str(board.getDirections())

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sokoban Solver")
    # Map area size
    window.columnconfigure(1, minsize=550)
    app = MainApp(window, bfs_solver, aStar_solver)
    window.resizable(False, False)
    window.mainloop()