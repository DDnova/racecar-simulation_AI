# Racecar Simulation 

using neat-python to simulate racecars

![gif](https://user-images.githubusercontent.com/82214133/140673101-f5a3d1a7-07d0-43b3-a908-56244252ce55.gif)

## Neural Network of Program
![nn](https://user-images.githubusercontent.com/82214133/140673474-1be93655-a175-4aa6-b3ac-9cb0d12692c8.jpg)

## Methodology
The project consists of two major parts. 
The python file 
and the NEAT config file.
In the neat config file we can specify all sorts of parameters which will influence things like reproduction, mutation, the amount of species etc.

Our car has 5 sensors that look out for the borders
Those are the 5 input neurons of our neural network
This is the only thing that our AI actually sees
Also our model has 2 output neurons that represent the 2 actions it can take, those are steering to the left and steering to the right

All of the neurons are interconnected and those connections have certain weights
Depending on all those values our model will react in a certain way based on the inputs
In the beginning all those reactions will be random, there will be zero intelligence behind what our cas are doing
however for each action our car takes they will either receive a reward or a penalty
To implement this we use the so called fitness metric
In our simple simulation the fitness of our car increases depending on the distance it 
covers without crashing

After each generation we then evolve our cars
the cars with the highest fitness value will probably survive and reproduce
whereas the cars that didn't perform so well will go extinct after a while

when a car reproduces it will not just duplicate the child car will be quite similar to its parent but not the same therefore it has a chance to become better

cars that are very similar to each other form an owned species
if a species doesn't see any improvements for a fixed number of generations it goes extinct
the best cars survive and reproduce and the worst cars go extinct
