import numpy as np
from mazeN_class import *
from tkinter import *
import matplotlib.pyplot as plt
from PIL import ImageTk
import PIL.Image
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkSlider, CTkComboBox, CTkCanvas, CTkRadioButton, CTkScrollableFrame, CTkCheckBox, CTkEntry
import customtkinter as ctk
from collections import deque

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
                canvas.create_text(x, y, text=arrow_symbol, font=('Arial', 20), fill = 'red')
            else:
                canvas.create_text(x, y, text=arrow_symbol, font=('Arial', 20), fill = '#0F6CAF')
            
    canvas.pack()
    

def visualize_values(canvas, values, maze):
    n = len(maze[0])
    CELL_SIZE= 700 // n
    
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
            canvas.create_text(x, y, text="{:.2f}".format(values[i][j]), font=('Arial', font_size))
            
    canvas.pack()
            

def solution_path(policy, start, goal):
    n = len(policy[0])

    current_row, current_col = start
    path = [(current_row, current_col)]
    
    while True:
        prev_row, prev_col = current_row, current_col
        if policy[current_row][current_col] == 'U':
            current_row -= 1
        elif policy[current_row][current_col] == 'D':
            current_row += 1
        elif policy[current_row][current_col] == 'R':
            current_col += 1
        elif policy[current_row][current_col] == 'L':
            current_col -= 1
        elif policy[current_row][current_col] == 'S':
            break

        if prev_row == current_col and prev_col == current_row:
            return None
        
        path.append((current_row, current_col))
        # print("current path: ", path)
        # print("policy:", policy)
        
    # print("total path: ", path)

    return path

def find_arrow_image(policy, state, CELL_SIZE):
    current_row = state[0]
    current_col = state[1]
    if policy[current_row][current_col] == 'U':
        return ImageTk.PhotoImage(PIL.Image.open("assets/arrow_up.png").resize((CELL_SIZE, CELL_SIZE)))
    elif policy[current_row][current_col] == 'D':
        return ImageTk.PhotoImage(PIL.Image.open("assets/arrow_down.png").resize((CELL_SIZE, CELL_SIZE)))
    elif policy[current_row][current_col] == 'R':
        return ImageTk.PhotoImage(PIL.Image.open("assets/arrow_right.png").resize((CELL_SIZE, CELL_SIZE)))
    elif policy[current_row][current_col] == 'L':
        return ImageTk.PhotoImage(PIL.Image.open("assets/arrow_left.png").resize((CELL_SIZE, CELL_SIZE)))
    elif policy[current_row][current_col] == 'S':
        return ImageTk.PhotoImage(PIL.Image.open("assets/firework.png").resize((CELL_SIZE, CELL_SIZE)))
