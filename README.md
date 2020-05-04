# Snakes in AI

This is part of my course project for the course of Machine Learning. In this project I decided to use my previous library for Neural Networks - Python ported version of [Toy Neural Network Librabry by Dan Shiffman](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6aCibgK1PTWWu9by6XFdCfh)
Thus, by using PyGame Library and the Neural Network Librabry the Snake AI is trained to dodge walls, avoid eating its own body and eat his snack.
The neural network architecture for the snake is (9,16,10,4)<br>
<p align="center">
  <img width="300" height="300" src="Images/Cover.png">
</p>

# Inputs
The snake requires 9 inputs for its working which are : Snake direction to X, Snake direction to Y, Wall to left, Wall infront, Wall right, Body on left, Body on right, Body front, Angle to food:
- **1** Input is Snakes current movement in X direction being -1 if to Left, 1 if to Right or 0 if no movement.
- **2** Input is Snakes current movement in Y direction being -1 if to Left, 1 if to Right or 0 if no movement.
- **3-5** Inputs are boolean inputs ie.(1/0) based on if wall is to its left,infront or right respectively.
- **6-8** Inputs are boolean inputs ie.(1/0) based on if any bodypart of snake is to its left,infront or right respectively.
- **9** Input is normalized angle between the snakes heads moving direction and snacks position, it is negative if food is to right and positive if food is to left.

# Outputs
The snake brain outputs an array of chances it should turn either left, right, up or down. By knowing which output is highest, the snake turns to that perticular direction

# Dependencies
Although majority of the library codes were written from scratch in this project, to run the program you must have:
- Python 3.6
- PyGame v1.9.6

# How To Run
To run the code, I have presented 3 versions:
- Non AI Snake game: Esentially just a snake game with keyboard Inputs, file name is snake.py
- AI for Training: It is the code to train the snake to play the game based on genetic algorithm, file name snake_AI_genetic.py
- AI Product: It is the final game based on the training which reads the saved brain from the training and uses it to determine the turns, file name is snake_AI.py
