import tkinter as tk
from tkinter.constants import DISABLED, HORIZONTAL, NORMAL, SUNKEN, VERTICAL
from tkinter.font import Font
import tkinter.ttk as ttk
from typing_extensions import IntVar
from PIL import Image, ImageTk
import os
from datetime import datetime

class MainApp:
    # @param (method) bfs_solver : (file_name : string, max_time : int) -> (solution : string, log : string)
    # @param (method) aStar_solver : (file_name : string, max_time : int) -> (solution : string, log : string)
    def __init__(self, master : tk.Tk, bfs_solver, aStar_solver):
        self.master = master
        self.solver_bfs = bfs_solver
        self.solver_aStar = aStar_solver
        ## 3 main columns:
        # Control panel
        self.frm_ctrl = ttk.Frame(master=self.master, width=250)
        self.frm_ctrl.grid(row=0, column=0, sticky="w")

        # Map area
        self.frm_map = ttk.Frame(master=self.master)
        self.frm_map.grid(row=0, column=1, sticky="nsew")

        # Log area
        self.frm_log = ttk.Frame(master=self.master)
        self.frm_log.grid(row=0, column=2, sticky="nsew")

        
        ## control panel:
        self.lbl_1 = ttk.Label(master=self.frm_ctrl, text="Choose map:")
        self.lbl_1.pack()
        # Listbox for choosing map
        self.frm_lstbox_choose = ttk.Frame(master=self.frm_ctrl)
        # Get list of file name in directory map/
        self.choices_map = [os.path.splitext(file)[0] for file in os.listdir('map') if os.path.isfile(os.path.join("map", file))]
        self.choicesvar = tk.StringVar(value=self.choices_map)
        self.lstbox_choose = tk.Listbox(master=self.frm_lstbox_choose, listvariable=self.choicesvar)
        self.scrbar_lstbox_choose_vert = ttk.Scrollbar(master=self.frm_lstbox_choose, orient=VERTICAL, command=self.lstbox_choose.yview)
        self.scrbar_lstbox_choose_horiz = ttk.Scrollbar(master=self.frm_lstbox_choose, orient=HORIZONTAL, command=self.lstbox_choose.xview)
        self.lstbox_choose.configure(yscrollcommand=self.scrbar_lstbox_choose_vert.set, xscrollcommand=self.scrbar_lstbox_choose_horiz.set)
        self.frm_lstbox_choose.pack()
        self.lstbox_choose.grid(row=0, column=0, sticky="nsew")
        self.scrbar_lstbox_choose_horiz.grid(row=1, column=0, sticky="we")
        self.scrbar_lstbox_choose_vert.grid(row=0, column=1, sticky="ns")

        # Buttons
        self.btn_show = ttk.Button(master=self.frm_ctrl, text="Show")
        self.btn_solve_BFS = ttk.Button(master=self.frm_ctrl, text="Solve BFS", state=DISABLED)
        self.btn_solve_AStar = ttk.Button(master=self.frm_ctrl, text="Solve A*", state=DISABLED)
        
        self.btn_show.pack()
        self.btn_solve_BFS.pack()
        self.btn_solve_AStar.pack()

        # Solution:
        self.lbl_2 = ttk.Label(master=self.frm_ctrl, text="Solution:")
        self.lbl_2.pack()
        self.frm_txt_solution = ttk.Frame(master=self.frm_ctrl)
        self.txt_solution = tk.Text(master=self.frm_txt_solution, width=16, height=10, state=DISABLED)
        self.scrbar_txt_solution = ttk.Scrollbar(master=self.frm_txt_solution, orient=VERTICAL, command=self.txt_solution.yview)
        self.txt_solution.configure(yscrollcommand=self.scrbar_txt_solution.set)
        self.frm_txt_solution.pack()
        self.txt_solution.pack(side=tk.LEFT)
        self.scrbar_txt_solution.pack(side=tk.LEFT, fill=tk.Y)
        self.txt_solution.tag_configure("current_move", background="#71add9") # Tag for current move's text

        # Delay time bar
        self.delay_time_var = tk.IntVar(value=500)
        self.frm_delay_label = ttk.Frame(master=self.frm_ctrl)
        self.frm_delay_label.pack()
        self.lbl_3 = ttk.Label(master=self.frm_delay_label, text="Delay: ")
        self.lbl_3.pack(side=tk.LEFT)
        self.lbl_delay_time = ttk.Label(master=self.frm_delay_label, textvariable=self.delay_time_var)
        self.lbl_delay_time.pack(side=tk.LEFT)
        self.lbl_4 = ttk.Label(master=self.frm_delay_label, text=" (ms)")
        self.lbl_4.pack(side=tk.LEFT)
        self.scl_delay = ttk.Scale(master=self.frm_ctrl, from_=100, to=3000, orient="horizontal", value=self.delay_time_var.get(), 
            command=lambda x: self.delay_time_var.set(int(float(x))))
        self.scl_delay.pack(fill=tk.X)

        # Maximum time
        self.frm_max_time = ttk.Frame(master=self.frm_ctrl)
        self.frm_max_time.pack()
        self.lbl_6 = ttk.Label(master=self.frm_max_time, text="Max time: ")
        self.lbl_6.pack(side=tk.LEFT)
        self.max_time_var = tk.IntVar(value=30)
        vcmd = (self.master.register(self.on_validate_max_time), "%P")
        self.spinbx_max_time = ttk.Spinbox(master=self.frm_max_time, from_=1, to=1800, textvariable=self.max_time_var, 
            width=5, validate="key", validatecommand=vcmd)
        self.spinbx_max_time.pack(side=tk.LEFT)
        self.lbl_7 = ttk.Label(master=self.frm_max_time, text=" secs")
        self.lbl_7.pack(side=tk.LEFT)

        ## Map area variable
        self.map_content = None # Map's file content
        self.map = [] # Map of object in symbols
        self.map_frame = [] # List of frames of map
        self.map_idx = None # Index of map name in listbox
        self.map_name = None # Name of map retrieved from choices_map
        self.player_pos = (None, None) # Player position

        # Style
        self.my_style = ttk.Style()
        self.my_style.configure("wall.TFrame", background="#50617d")

        # Image
        self.img_box_raw = Image.open("image/box.png") # Pixel perfect - flaticon.com
        self.img_player_raw = Image.open("image/man.png") # Freepik - flaticon.com
        self.img_box = None
        self.img_player = None

        ## Log area
        self.frm_clr_log = ttk.Frame(self.frm_log) # Contains label and clear button
        self.lbl_5 = ttk.Label(self.frm_clr_log, text="Log:")
        self.btn_clr_log = ttk.Button(self.frm_clr_log, text="Clear")
        self.frm_clr_log.pack(fill=tk.X)
        self.lbl_5.pack(side=tk.LEFT)
        self.btn_clr_log.pack(side=tk.RIGHT)

        self.frm_txt_log = ttk.Frame(self.frm_log) # Contains txt_log and its scrollbar
        self.txt_log = tk.Text(self.frm_txt_log, state=DISABLED, width=32, height=30)
        self.scrbar_txt_log = ttk.Scrollbar(self.frm_txt_log, orient=VERTICAL, command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=self.scrbar_txt_log.set)
        self.frm_txt_log.pack()
        self.txt_log.pack(side=tk.LEFT)
        self.scrbar_txt_log.pack(side=tk.LEFT, fill=tk.Y)

        self.btn_save_log = ttk.Button(self.frm_log, text="Save log")
        self.btn_save_log.pack()

        # Bind functions to events
        self.bind_func()

    def bind_func(self):
        self.btn_show.configure(command=self.show_map)
        self.btn_solve_BFS.configure(command=self.solve_map_bfs)
        self.btn_solve_AStar.configure(command=self.solve_map_aStar)
        self.btn_save_log.configure(command=self.save_log)
        self.btn_clr_log.configure(command=self.clear_log)

    # This function is used for disable solving function of app after a solution is made
    def disable_solving(self):
        self.btn_solve_BFS.configure(state=DISABLED)
        self.btn_solve_AStar.configure(state=DISABLED)

    # Opposite function of pause_funcs()
    def enable_solving(self):
        self.btn_solve_BFS.configure(state=NORMAL)
        self.btn_solve_AStar.configure(state=NORMAL)

    def show_map(self):
        self.map_idx = self.lstbox_choose.curselection()
        if len(self.map_idx) == 0: # not chosen yet
            self.map_idx = None
            return

        self.enable_solving() # Enable solving function

        self.add_text_widget(self.txt_solution, "1.0", "") # Clear text in txt_solution
        self.map_idx = self.map_idx[0]
        
        self.map_name = self.choices_map[self.map_idx]
        self.master.title("Sokoban Solver - " + self.map_name) # Change title of app
        # Read map file
        with open("map/" + self.map_name + ".txt", "r") as f:
            self.map_content = f.readlines()
            self.n_row = int(self.map_content[0])
            self.n_col = int(self.map_content[1])
            self.map_content.pop(0)
            self.map_content.pop(0)
            # Set size of cell
            self.cell_size = 512 // self.n_row if (self.n_row > self.n_col) else 512 // self.n_col

        # Get image
        self.img_box = self.img_box_raw.resize((self.cell_size - 12, self.cell_size - 12), Image.ANTIALIAS)
        self.img_box = ImageTk.PhotoImage(self.img_box)
        self.img_player = self.img_player_raw.resize((self.cell_size - 12, self.cell_size - 12), Image.ANTIALIAS)
        self.img_player = ImageTk.PhotoImage(self.img_player)

        # Clear old map
        if len(self.map_frame) > 0:
            for row in self.map_frame:
                for cell in row:
                    cell.grid_forget()
            self.map_frame = []

        # Draw new map
        self.map = [] # Reset

        for i in range(self.n_row):
            self.map.append([]) # append a row
            self.map_frame.append([])
            for j in range(self.n_col):

                current_sym = self.map_content[i][j]
                self.map[i].append(current_sym)

                # Draw static object: wall, goal and ground
                if (current_sym == "@"): # wall
                    current_frm = ttk.Frame(self.frm_map, width=self.cell_size, height=self.cell_size, style="wall.TFrame")
                else:
                    current_frm = tk.Canvas(master=self.frm_map, width=self.cell_size-8, height=self.cell_size-8, bd=0, borderwidth=4)
                    if (current_sym == "o" or current_sym == "*" or current_sym == "$"): # goal
                        current_frm.configure(relief=SUNKEN, bg="#94e3b5")
                current_frm.grid(row=i, column=j, sticky="nsew")

                # Draw dynamic object: box and player
                if (current_sym == "+" or current_sym == "*"):
                    self.visualize_img(current_frm, self.img_box)
                elif (current_sym == "i" or current_sym == "$"):
                    self.visualize_img(current_frm, self.img_player)
                    self.player_pos = (i, j)
                
                self.map_frame[i].append(current_frm)

    def visualize_img(self, frame : tk.Canvas, image):
        frame.delete("all") # Firstly clear the frame
        frame.create_image(8, 8, anchor="nw", image=image) # Draw new objec
    
    # @param pos: position to start inserting text. Format: "<line>.<position from start of line>"
    # @param value: text to be inserted
    # @param rewrite_or_change: rewrite if True, else only change the content and not rewrite
    def add_text_widget(self, text_widget : tk.Text, pos, value, rewrite_or_change=True):
        text_widget.configure(state=NORMAL) # Change state to enable editing
        if rewrite_or_change:
            text_widget.delete("1.0", tk.END) # Delete old text
        text_widget.insert(pos, value)
        text_widget.configure(state=DISABLED)

    def solve_map_bfs(self):
        self.solve_map(self.solver_bfs)

    def solve_map_aStar(self):
        self.solve_map(self.solver_aStar)

    def solve_map(self, solver_func):
        if self.map_idx is None:
            return
        self.btn_show.configure(state=DISABLED) # Disable show button when playing
        self.disable_solving() # Disable solving function
        solution, log = solver_func(os.path.join("map", self.map_name + ".txt"), self.max_time_var.get())
        # Change text in txt_solution
        self.txt_solution.tag_remove("current_move", "1.0", tk.END) # Remove tag
        self.add_text_widget(self.txt_solution, "1.0", solution)

        # Update log
        self.add_text_widget(self.txt_log, tk.END, "Solve " + self.map_name + " using " + 
            ("BFS\n\n" if solver_func == self.solver_bfs else "A*\n\n"), rewrite_or_change=False)
        self.add_text_widget(self.txt_log, tk.END, log, rewrite_or_change=False)
        if solution == "Not Found":
            self.add_text_widget(self.txt_log, tk.END, "\nTimeout (Exceed " + str(self.max_time_var.get()) + " seconds)",
                rewrite_or_change=False)
        self.add_text_widget(self.txt_log, tk.END, "\n==========\n\n", rewrite_or_change=False)

        if solution == "Not Found":
            self.btn_show.configure(state=NORMAL)
        else:
            self.move(list(solution), 0)

    def move(self, moves, current_idx):
        if current_idx >= len(moves):
            self.btn_show.configure(state=NORMAL)
            return

        # Remove previous tag
        if current_idx > 0:
            self.txt_solution.tag_remove("current_move", "1." + str(current_idx - 1), "1." + str(current_idx))
        # Add new tag
        self.txt_solution.tag_add("current_move", "1." + str(current_idx), "1." + str(current_idx + 1))

        move = moves[current_idx]
        self.do_move(move)

        # Next move occur after a delay
        def move_next():
            self.move(moves, current_idx + 1)
        self.master.after(self.delay_time_var.get(), move_next)

    def do_move(self, move):
        if move == "u":
            direction = (-1, 0)
        elif move == "d":
            direction = (1, 0)
        elif move == "l":
            direction = (0, -1)
        elif move == "r":
            direction = (0, 1)
        else:
            direction = (0, 0)

        new_pos_x, new_pos_y = self.player_pos[0] + direction[0], self.player_pos[1] + direction[1]
        if new_pos_x < 0 or new_pos_x >= self.n_row or new_pos_y < 0 or new_pos_y >= self.n_col:
            return

        # If there is a wall forward
        if self.map[new_pos_x][new_pos_y] == "@":
            return
        # if there is a box in front of the player
        if self.map[new_pos_x][new_pos_y] in ["+","*"]:
            new_box_pos_x, new_box_pos_y = new_pos_x + direction[0], new_pos_y + direction[1]
            if new_box_pos_x < 0 or new_box_pos_x >= self.n_row or new_box_pos_y < 0 or new_box_pos_y >= self.n_col:
                return
            # The player cannot push the box if there is an obstacle forward
            if self.map[new_box_pos_x][new_box_pos_y] not in ["_", "o"]:
                return
            # Make the move in the map
            self.map[new_box_pos_x][new_box_pos_y] = "+" if self.map[new_box_pos_x][new_box_pos_y] == "_" else "*"
            self.map[new_pos_x][new_pos_y] = "_" if self.map[new_pos_x][new_pos_y] == "+" else "o"
            # Visulize the moved box
            self.visualize_img(self.map_frame[new_box_pos_x][new_box_pos_y], self.img_box)

        # Now move the player
        self.map[new_pos_x][new_pos_y] = "i" if self.map[new_pos_x][new_pos_y] == "_" else "$"
        self.map[self.player_pos[0]][self.player_pos[1]] = "_" if self.map[self.player_pos[0]][self.player_pos[1]] == "i" else "o"
        self.map_frame[self.player_pos[0]][self.player_pos[1]].delete("all")
        self.visualize_img(self.map_frame[new_pos_x][new_pos_y], self.img_player)
        self.player_pos = (new_pos_x, new_pos_y)

    def on_validate_max_time(self, new_value):
        return new_value.isdigit() and 1 <= int(new_value) <= 1800

    def save_log(self):
        f = open(os.path.join("log", "Log_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"), "w")
        f.write(self.txt_log.get("1.0", tk.END))
        f.close()

    def clear_log(self):
        self.add_text_widget(self.txt_log, "1.0", "")

def bfs_solver_sample(filename):
    return "uddurlrl", "Log BFS\nJust testing..."

def aStar_solver_sample(filename):
    return "rrurru", "Log AStar\nSolution only contains u, d, r and l letter (not capital).\n"

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sokoban Solver")
    # Map area size
    window.columnconfigure(1, minsize=550)
    app = MainApp(window, bfs_solver_sample, aStar_solver_sample)
    window.resizable(False, False)
    window.mainloop()