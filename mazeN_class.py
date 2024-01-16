from tkinter import *
import numpy as np
import random
from PIL import ImageTk, Image
# from gui_widgets import *
# from grid import Grid

CELL_SIZE = 0

class Mazen:
    def __init__(self, n, canva):
        global CELL_SIZE
        CELL_SIZE = 700 // n
        self.n = n
        self.canva = canva
        self.visited_cells = []
        self.barriers = []
        self.revisited_cells = []
        
        
        self.maze = [[0 for _ in range(n)]for _ in range(n)]

    def construct_maze(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.maze[row][col] == 1:
                    color = 'white'
                elif self.maze[row][col] == 0:
                    color = 'black'
                self.draw_maze(row, col, color)
                    

    def draw_maze(self, row, col, color):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canva.create_rectangle(x1, y1, x2, y2, fill = color)

    def check_neighbours(self, current_row, current_col):
        neighbours = [[current_row, current_col-1, current_row-1, current_col-2, current_row, current_col-2, current_row+1, current_col-2, current_row-1, current_col-1, current_row+1, current_col-1], #left
                    [current_row, current_col+1, current_row-1, current_col+2, current_row, current_col+2, current_row+1, current_col+2, current_row-1, current_col+1, current_row+1, current_col+1], #right
                    [current_row-1, current_col, current_row-2, current_col-1, current_row-2, current_col, current_row-2, current_col+1, current_row-1, current_col-1, current_row-1, current_col+1], #top
                    [current_row+1, current_col, current_row+2, current_col-1, current_row+2, current_col, current_row+2, current_col+1, current_row+1, current_col-1, current_row+1, current_col+1]] #bottom
        
        visitable_neighbours = []
        for i in neighbours:
            if i[0] > 0 and i[0] < (self.n - 1) and i[1] > 0 and i[1] < (self.n - 1):
                if self.maze[i[2]][i[3]] == 1 or self.maze[i[4]][i[5]] == 1 or self.maze[i[6]][i[7]] == 1 or self.maze[i[8]][i[9]] == 1 or self.maze[i[10]][i[11]] == 1:
                    self.barriers.append(i[0:2])
                else:
                    visitable_neighbours.append(i[0:2])
        return visitable_neighbours

    def generate_maze(self):
        start_row = random.randint(0, self.n-1)
        start_col = random.randint(0, self.n-1)
        self.start = (start_row, start_col)

        start_color = '#504CD1'

        self.maze[start_row][start_col] = 2
        finished = False
        current_row, current_col = start_row, start_col

        while not finished:
            visitable_neighbours = self.check_neighbours(current_row, current_col)
            if len(visitable_neighbours) != 0:
                random_neighbour_idx = random.randint(1, len(visitable_neighbours)) - 1
                temp_row, temp_col = visitable_neighbours[random_neighbour_idx]
                self.maze[temp_row][temp_col] = 1
                self.visited_cells.append([temp_row, temp_col])
                current_row, current_col = temp_row, temp_col
                
            if len(visitable_neighbours) == 0:
                try:
                    current_row, current_col = self.visited_cells.pop()
                    self.revisited_cells.append([current_row, current_col])
                except:
                    finished= True
                    
                    
        self.construct_maze()
        self.draw_maze(start_row, start_col, start_color)

        goal_idx = random.randint(1, len(self.revisited_cells))-1
        goal_row = self.revisited_cells[goal_idx][0]
        goal_col = self.revisited_cells[goal_idx][1]

        goal_color = '#FFCE00'
        self.maze[start_row][start_col] = 2
        self.draw_maze(goal_row, goal_col, goal_color)
        self.goal = (goal_row, goal_col)
        # print(self.revisited_cells)
        return self.maze, self.start, self.goal
    
    def visualize_policy(self, maze, policy):
        
        arrow_images = {
        'U': 'arrow_up.png',
        'D': 'arrow_down.png',
        'R': 'arrow_right.png',
        'L': 'arrow_left.png'
        }
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if policy[row][col] in arrow_images:
                    arrow_image = arrow_images[policy[row][col]]
                    arrow_image_path = f'assets/{arrow_image}' 
                    
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE
                    
                    img = Image.open(arrow_image_path)
                    resized_img = img.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)
                    arrow_photo = ImageTk.PhotoImage(resized_img)
                    
                    self.canva.create_image(x, y, anchor=NW, image=arrow_photo)
                    self.canva.image = arrow_photo  # Keep a reference to avoid garbage collection
                    
        

def main():
    n = 10
        
    root = Tk()
    root.title('Maze Generator')
    canvas_side = n * CELL_SIZE
    canva = Canvas(root, width = canvas_side, height = canvas_side, bg = 'grey')
    
    mazen = Mazen(n, canva)
    maze, start, goal = mazen.generate_maze()    
    canva.pack()
    
    print("Maze ------------")
    print(maze)
    print("start: ", start)
    print("goal: ", goal)
    root.mainloop()
    
if __name__ == "__main__":
    main()