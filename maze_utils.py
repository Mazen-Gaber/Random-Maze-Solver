import numpy as np
from mazeN_class import *
from tkinter import *
import matplotlib.pyplot as plt
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton, CTkScrollableFrame, CTkCheckBox, CTkEntry
import customtkinter as ctk

def policy_modified(policy):
    n = len(policy[0])
    x = np.zeros((n,n), dtype=str)
    for i in range(n):
        for j in range(n):
            if policy[i][j] == 0:
                x[i][j] == 'U'
            elif policy[i][j] == 1:
                x[i][j] == 'D'
            elif policy[i][j] == 2:
                x[i][j] == 'L'
            elif policy[i][j] == 3:
                x[i][j] == 'R'
            elif policy[i][j] == 4:
                x[i][j] == 'X '
    return x

def draw_maze(canvas, row, col, color):
    # print("Cell size: ", CELL_SIZE)
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill = color)
    
def draw_maze2(canvas, row, col, color, n):
    CELL_SIZE = 700 // n
    # print("Cell size: ", CELL_SIZE)
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill = color)
    
    

def visualize_policy(canvas, policy, maze, solution_path):
    
    print("IN VISUALIZE POLICY")
    print(policy)
    print("maze:")
    print(maze)
    n = len(policy[0])
    CELL_SIZE = 700 // n
    up_arrow = '\u2191'  
    down_arrow = '\u2193'  
    left_arrow = '\u2190'  
    right_arrow = '\u2192' 
    star_symbol = '\u2605'
    
    # root = Tk()
    # root.title('Policy')
    # root.geometry("800x600")
    # canvas_side = n * CELL_SIZE
    # canvas = Canvas(root, width = canvas_side, height = canvas_side)
    
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
    
    for i in range(n):
        for j in range(n):
            if policy[i][j] == 'U':
                arrow_symbol = up_arrow
            elif policy[i][j] == 'D':
                arrow_symbol = down_arrow
            elif policy[i][j] == 'L':
                arrow_symbol = left_arrow
            elif policy[i][j] == 'R':
                arrow_symbol = right_arrow
            elif policy[i][j] == 'S':
                arrow_symbol = star_symbol
            else:
                continue

            x = j * CELL_SIZE + CELL_SIZE // 2
            y = i * CELL_SIZE + CELL_SIZE // 2
            
            in_path = False
            if (i,j) in solution_path:
                canvas.create_text(x, y, text=arrow_symbol, font=('Arial', 20), fill = '#0F6CAF')
            else:
                canvas.create_text(x, y, text=arrow_symbol, font=('Arial', 20))
            
    canvas.pack()
    # root.mainloop()
    

def visualize_values(canvas, values, maze):
    n = len(maze[0])
    CELL_SIZE= 700 // n
    
    # root = Tk()
    # root.title('Value function')
    # canvas_side = n * CELL_SIZE
    # canvas = Canvas(root, width = canvas_side, height = canvas_side, bg = 'grey')
    
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
                
    for i in range(n):
        for j in range(n):
            x = j * CELL_SIZE + CELL_SIZE // 2
            y = i * CELL_SIZE + CELL_SIZE // 2
            font_size = min(CELL_SIZE // 2, 14)
            canvas.create_text(x, y, text="{:.3f}".format(values[i][j]), font=('Arial', font_size))
            # canvas.create_text(x, y, text="{:.3f}".format(values[i][j]), font=('Arial', 14))
            
    canvas.pack()
    # root.mainloop()
            

def solution_path(policy, start, goal):
    n = len(policy[0])
    
    current_row = start[0]
    current_col = start[1]
    print(current_row, current_col)
    path = []
    path.append((current_row, current_col))
    
    while True:
        if policy[current_row][current_col] == 'U':
            current_row = current_row - 1
        elif policy[current_row][current_col] == 'D':
            current_row = current_row + 1
        elif policy[current_row][current_col] == 'R':
            current_col = current_col + 1
        elif policy[current_row][current_col] == 'L':
            current_col = current_col - 1
        elif policy[current_row][current_col] == 'S':
            break
        path.append((current_row, current_col))
    print(path)
    return path
