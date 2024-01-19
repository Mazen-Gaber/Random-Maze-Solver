
# Random Maze Game - Readme

This repository contains a Python implementation of a Maze Game. The game allows users to navigate through a maze and find the optimal path from the start to the goal cell using two reinforcement learning algorithms.

## Requirements

To run the game, you need to have the following libraries installed:

-   NumPy
-   Tkinter
-   PIL (Python Imaging Library)
-   Matplotlib
-   Time/Timeit 
-   Threading 

You can install these libraries using the following command:

``` shell
pip install numpy tkinter customtkinter threading pillow matplotlib time timeit 

```

## How to Run

To start the Maze Game, run the file  `maze_GUI.py`. Make sure you have all the required libraries installed before running the program.
``` shell
python maze_GUI.py

```

## Files

The repository includes the following files:

-   `mazeN_class.py`: Contains the implementation of the maze class.
-   `maze_utils.py`: Contains utility functions for the maze GUI.
-   `algorithms.py`: Contains the implementation of the algorithms used in the game.
-   `maze_GUI.py`: The main file to run the game and contains the main GUI components and functions.
-   `assets/`: A directory containing the images and the font used in the GUI.
Please try to download the font found in the ``assets/`` folder first for better visualization !

## Usage

Once you run  `maze_GUI.py`, a graphical user interface (GUI) will appear, allowing you to interact with the Maze Game. The GUI provides options to select the maze size, algorithm, and solve the maze. The solution will be visualized using animated arrows and a firework on arrival. If the animation is too rapid. please refer to the function ``visualize_solution`` in file ``maze_GUI.py`` at line ``418`` and readjust the ``time.sleep()`` as desired.

The available algorithms for finding the optimal path are:

-   Value Iteration
-   Policy Iteration

You can select the algorithm from the GUI before starting the game.
