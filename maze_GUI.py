import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Label
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton, CTkScrollableFrame, CTkCheckBox, CTkEntry
import customtkinter as ctk
from PIL import ImageTk
import PIL.Image
import timeit, time
from algorithms import *
from mazeN_class import *
from maze_utils import *
import threading

import warnings
warnings.filterwarnings("ignore")

class MazeGameGUI:
    def __init__(self):
        
        self.technique = "Value Iteration"
        self.n = 8
        self.maze = None
        self.start = None
        self.goal = None
        self.value_pov = True
                
        self.root = CTk()
        self.root.title("Maze Game")
        self.root.geometry('1400x700')
        self.root.resizable(False, False)
        background = ImageTk.PhotoImage(PIL.Image.open("assets/purple space2.jpg").resize((2000, 1200)))
        background_label = CTkLabel(self.root, image=background, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        #### START PAGE FRAME ####
        
        self.start_frame = CTkFrame(self.root)
        self.start_frame.pack()
        
        self.title_label = CTkLabel(self.start_frame, text=" Maze Solver Game", font=("joystix monospace", 40))
        self.title_label.pack(anchor = 'c', pady=20, padx=60)
        
        self.radio_frame = CTkFrame(self.start_frame, width=90)
        self.radio_frame.pack()
        
        self.theme_label = CTkLabel(self.radio_frame, text="Theme:", font=("joystix monospace", 20) )
        self.theme_label.pack(padx=10, pady=8)
        
        self.theme_var = tk.StringVar(value="Dark")
        self.light_theme = CTkRadioButton(self.radio_frame, value="Light", text="Light", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.theme_var, command=self.game_theme)
        self.light_theme.pack(anchor='e' ,padx=80, pady=2)
        self.dark_theme = CTkRadioButton(self.radio_frame, value="Dark", text="Dark", font=("joystix monospace", 16), fg_color=("#3A7EBF","#504CD1"), variable=self.theme_var, command=self.game_theme)
        self.dark_theme.pack(anchor='e',padx=80, pady=10)

        def button_click_event():
            dialog = ctk.CTkInputDialog(text="Enter the size(N):", title="Maze Size", font=("joystix monospace", 12))
            self.n = int(dialog.get_input())
            print("Number:", self.n)

        self.input_button = ctk.CTkButton(self.start_frame, text="Input Size", font=("joystix monospace", 12), command=button_click_event, fg_color=("#3A7EBF","#504CD1"))
        self.input_button.pack(pady=10, padx=20)
        
        self.start_button = CTkButton(self.start_frame, text="Start Game", font=("joystix monospace", 20), command=self.start_game, width=70, height=40, fg_color=("#3A7EBF","#504CD1"))
        self.start_button.pack(pady=20)
        
        #### PUZZLE FRAME ####

        self.puzzle_frame = CTkFrame(self.root, width=90)
        self.puzzle_frame.pack()
        
        buttons1_frame = CTkFrame(self.puzzle_frame)
        buttons1_frame.pack(pady=(5,5), padx=5)
        
        self.back_button = CTkButton(buttons1_frame, text="Back", command=self.return_to_start_page, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.back_button.pack(pady=10, padx=20, side = 'left')
        
        self.technique_label = CTkLabel(self.puzzle_frame, text="Technique", font=("joystix monospace", 12))
        self.technique_label.pack()
        
        self.technique_combobox = CTkComboBox(self.puzzle_frame, values=["Value Iteration", "Policy Iteration"], width = 200, font=("joystix monospace", 12), dropdown_font=("joystix monospace", 12),
                                                button_color=("#3A7EBF","#504CD1"), border_color=("#3A7EBF","#504CD1"), justify="center")
        self.technique_combobox.pack()
        
        # self.n_label = CTkLabel(self.puzzle_frame, text="Size (N)", font=("joystix monospace", 12))
        # self.n_label.pack()
        
        def button1_click_event():
            dialog = ctk.CTkInputDialog(text="Enter the size(N):", title="Maze Size", font=("joystix monospace", 12))
            self.n = int(dialog.get_input())
            print("Number:", self.n)
            self.change_maze()

        self.change_input_button = ctk.CTkButton(self.puzzle_frame, text="Input Size", font=("joystix monospace", 12), command=button1_click_event, fg_color=("#3A7EBF","#504CD1"))
        self.change_input_button.pack(pady=10, padx=20)
        
        self.info_frame = CTkFrame(self.puzzle_frame)
        self.info_frame.pack(pady=10)
        
        self.start_label = CTkLabel(self.info_frame, text="START -> VIOLET", font=("joystix monospace", 12), text_color = "#504CD1")
        self.start_label.pack(padx = 3)
        self.goal_label = CTkLabel(self.info_frame, text="GOAL -> GOLD", font=("joystix monospace", 12), text_color = "#FFCE00")
        self.goal_label.pack()
        
        button_frame = CTkFrame(self.puzzle_frame)
        button_frame.pack(pady=10)
        
        self.start_button2 = CTkButton(button_frame, text="Solve", font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command = self.solve_maze)
        self.start_button2.pack(side='left', pady=10, padx=10)
        
        self.change_puzzle_button = CTkButton(button_frame, text="Change Maze", font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command = self.change_maze)
        self.change_puzzle_button.pack(side='left', padx=10)
        
        self.change_input_button = ctk.CTkButton(self.puzzle_frame, text="Show Policy and Value function", font=("joystix monospace", 12), command=self.display_policy_value, fg_color=("#3A7EBF","#504CD1"))
        self.change_input_button.pack(pady=10, padx=20)
        
        self.analysis_frame = CTkScrollableFrame(self.root, width = 350, height=250)
        self.analysis_frame.pack()
        
        #### POLICY FRAME ####
        
        self.policy_frame = CTkFrame(self.root)
        self.policy_frame.pack()
        
        buttons3_frame = CTkFrame(self.policy_frame)
        buttons3_frame.pack(pady=(5,5), padx=5)
        
        self.back_button3 = CTkButton(buttons3_frame, text="Back", command=self.return_to_puzzle_page, width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"))
        self.back_button3.pack(pady=10, padx=20, side = 'left') #me7taga te3adel !!
        
        self.labels_frame = CTkFrame(self.policy_frame)
        self.labels_frame.pack(pady=(5,5), padx=5)
        
        self.policy_frame_title = CTkLabel(self.labels_frame, text ="Optimal Policy", font=("joystix monospace", 16))
        self.policy_frame_title.pack(side = 'left', padx=(20,300))
        self.policy_canvas = CTkCanvas(self.policy_frame, width=700, height=700)
        self.policy_canvas.pack(side='left', padx=(40,20), pady=(20,40))
        
        self.value_frame_title = CTkLabel(self.labels_frame, text ="Optimal Value Function", font=("joystix monospace", 16))
        self.value_frame_title.pack(side = 'right', padx=(300,20))
        self.value_canvas = CTkCanvas(self.policy_frame, width=700, height=700)
        self.value_canvas.pack(side='left', padx=(20,40), pady=(20,40))
        
        self.show_start_page()      
        
    def show_start_page(self):
        self.puzzle_frame.pack_forget()
        self.analysis_frame.pack_forget()
        self.policy_frame.pack_forget()
        self.start_frame.pack(pady=50)
        
    def return_to_start_page(self):
        self.clear_puzzle()
        self.puzzle_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.analysis_frame.pack_forget()
        self.start_frame.pack(pady=50)
        self.canvas.pack_forget()
        
    def return_to_puzzle_page(self):
        self.start_frame.pack_forget()
        self.policy_frame.pack_forget()
        self.puzzle_frame.pack_forget()
        self.puzzle_frame.pack(side='left', pady=10, padx=(40,40))
        self.canvas = CTkCanvas(self.root, width=700, height=700)
        self.canvas.pack(side='left')
        
        self.draw_defined_maze()
        
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
        time_taken = self.end_time - self.start_time
        self.analyze_algorithm(self.technique, time_taken, self.cost)
        
    def show_puzzle_page(self):
        self.start_frame.pack_forget()
        self.policy_frame.pack_forget()
        self.puzzle_frame.pack(side='left', pady=10, padx=(40,40))
        self.canvas = CTkCanvas(self.root, width=700, height=700)
        self.canvas.pack(side='left')
        
        self.draw_random_maze()
        
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
        
    def change_puzzle(self):
        self.start_frame.pack_forget()
        self.policy_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.clear_puzzle()
        self.canvas.pack_forget()
        self.puzzle_frame.pack_forget()
        self.canvas = CTkCanvas(self.root, width=700, height=700)
        self.canvas.pack(side='left', padx=(20,20))
        
    def clear_analysis_frame(self):
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.analysis_frame.pack_forget()
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
        
    def clear_puzzle(self):
        self.canvas.delete("all")
        
    def start_game(self):
        self.show_puzzle_page()
        
    def game_theme(self):
        theme = self.theme_var.get()
        # ctk.set_smooth_theme_transition(True)
        if theme == "Dark":
            ctk.set_appearance_mode("Dark")
            
        elif theme == "Light":
            ctk.set_appearance_mode("Light") 
        
    def draw_defined_maze(self):
        n = self.n
        maze = self.maze
        canvas = self.canvas
        for i in range(n):
            for j in range(n):
                if maze[i][j] == 0:
                    draw_maze2(canvas, i, j, 'black', n)
                if maze[i][j] == 1:
                    draw_maze2(canvas, i, j, 'white', n)
                if maze[i][j] == 2:
                    draw_maze2(canvas, i, j, '#504CD1', n)
                elif maze[i][j] == 3:
                    draw_maze2(canvas, i, j, '#FFCE00', n)
        
    def draw_random_maze(self):
        n = self.n
        CELL_SIZE = (700) // n
        canvas_side = n * CELL_SIZE
        self.canva = CTkCanvas(self.canvas, width = canvas_side, height = canvas_side, bg = 'grey')

        mazen = Mazen(n, self.canva)
        self.maze, self.start, self.goal = mazen.generate_maze()    
        self.canva.pack()
        self.maze[self.start[0]][self.start[1]] = 2
        self.maze[self.goal[0]][self.goal[1]] = 3
        
        print("Maze ------------")
        for i in range(n):
            print(self.maze[i])
        print("start: ", self.start)
        print("goal: ", self.goal)
        
    def change_maze(self):
        self.start_frame.pack_forget()
        self.analysis_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.clear_puzzle()
        self.canvas.pack_forget()
        self.puzzle_frame.pack_forget()

        self.show_puzzle_page()
        
    def solve_maze(self):
        
        self.technique = self.technique_combobox.get()
        print(self.technique)
        
        self.start_frame.pack_forget()
        self.analysis_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.clear_puzzle()
        self.canvas.pack_forget()
        self.puzzle_frame.pack_forget()
        
        n = self.n
        CELL_SIZE = (700) // n
        canvas_side = n * CELL_SIZE
        self.canva = CTkCanvas(self.canvas, width = canvas_side, height = canvas_side, bg = 'grey')
        
        if self.maze == None or self.start == None or self.goal == None:
            print("NO MAZE, START OR GOAL FOUND")
            analysis_label = CTkLabel(self.analysis_frame, text = "NO MAZE, START OR GOAL FOUND", text_color = 'red', font=("joystix monospace", 12), width = 280)   
            analysis_label.pack(anchor="w", pady=3)
            return
        
        analysis_label = CTkLabel(self.analysis_frame, text = "THE MAZE IS SOLVABLE", text_color = 'red', font=("joystix monospace", 12), width = 280)   
        analysis_label.pack(anchor="w", pady=3)
        
        self.optimal_value_functions = None
        
        if self.technique == 'Value Iteration':
            self.value_pov = True
            self.start_time = timeit.default_timer()
            self.optimal_value_functions, self.optimal_policy = value_iteration(self.maze)
            self.end_time = timeit.default_timer()
        else:
            self.value_pov = False
            self.start_time = timeit.default_timer()
            self.optimal_policy, self.optimal_value_functions, iterations = policy_iteration(self.maze)
            print("Iterations: ", iterations)
            self.end_time = timeit.default_timer()
        
        time_taken = self.end_time - self.start_time
        
        self.path = solution_path(self.optimal_policy, self.start, self.goal)
        
        self.cost = len(self.path) - 1
        
        self.analyze_algorithm(self.technique, time_taken, self.cost)
        print(f"-----> {self.technique} time taken: {time_taken} ms, cost = {self.cost} ")
        self.start_frame.pack_forget()
        self.policy_frame.pack_forget()
        self.puzzle_frame.pack(side='left', pady=10, padx=(40,40))
        self.canvas = CTkCanvas(self.root, width=700, height=700)
        self.canvas.pack(side='left')
        
        self.visualize_solution(self.canvas, self.path)
        
        print("Optimal Value Function:")
        print(self.optimal_value_functions)
        print("\nOptimal Policy:")
        print(self.optimal_policy)
        
        print(f"-----------------------------END OF {self.technique}-----------------------------")
        
    def analyze_algorithm (self, algorithm, time_taken, cost):
        steps_text = f"--> {algorithm}\n Time taken: {time_taken*1000:.4f} ms\n Cost: {cost}"
        analysis_label = CTkLabel(self.analysis_frame, text = steps_text, font=("joystix monospace", 12), width = 280)   
        analysis_label.pack(anchor="w", pady=3, padx = 3)
        
    def display_policy_value(self):
        self.start_frame.pack_forget()
        self.analysis_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.clear_puzzle()
        self.canvas.pack_forget()
        self.puzzle_frame.pack_forget()

        self.policy_frame.pack_forget()
        self.policy_frame.pack()
        visualize_policy(self.policy_canvas, self.optimal_policy, self.maze, self.path)  
        visualize_values(self.value_canvas, self.optimal_value_functions, self.maze) 
        self.policy_frame.pack()
        
    def visualize_solution(self, canvas, solution_path):
        maze = self.maze
        n = self.n
        CELL_SIZE = 700 // n
        canvas = Canvas(canvas, width=CELL_SIZE * n, height=CELL_SIZE * n)
        
        self.analysis_frame.pack_forget()
        widgets = self.analysis_frame.winfo_children()
        for widget in widgets:
            widget.destroy()
        self.analysis_frame2 = CTkFrame(self.analysis_frame)
        self.analysis_frame2.pack()
        self.analysis_frame.pack(side = 'left', padx=(40,40))
        self.analysis_frame_title = CTkLabel(self.analysis_frame2, text ="Analysis History", font=("joystix monospace", 16))
        self.analysis_frame_title.pack(side = 'left', padx=(40,0))
        
        self.analysis_frame_clear_button = CTkButton(self.analysis_frame2, text ="Clear", width=50, font=("joystix monospace", 12), fg_color=("#3A7EBF","#504CD1"), command=self.clear_analysis_frame)
        self.analysis_frame_clear_button.pack(side = 'left', padx=(30,0))
        analysis_label = CTkLabel(self.analysis_frame, text = "THE MAZE IS SOLVABLE", text_color = 'red', font=("joystix monospace", 12), width = 280)   
        analysis_label.pack(anchor="w", pady=3)
        self.analyze_algorithm(self.technique, self.end_time - self.start_time, self.cost)
        
        for i in range(n):
            for j in range(n):
                if maze[i][j] == 0:
                    draw_maze2(canvas, i, j, 'black', n)
                if maze[i][j] == 1:
                    draw_maze2(canvas, i, j, 'white', n)
                if maze[i][j] == 2:
                    draw_maze2(canvas, i, j, '#504CD1', n)
                elif maze[i][j] == 3:
                    draw_maze2(canvas, i, j, '#FFCE00', n)
                    
        canvas.pack()

        for row, col in solution_path:
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            movement_image = find_arrow_image(self.optimal_policy, (row, col), CELL_SIZE)
            canvas.create_image(x, y, anchor=NW, image=movement_image)
            canvas.update()  
            canvas.pack()
            time.sleep(0.5) # Adjustable to the desired lag animation !! 
        
    def run(self):
        self.root.mainloop()

app = MazeGameGUI()
app_thread = threading.Thread(app.run())
app_thread.start()
