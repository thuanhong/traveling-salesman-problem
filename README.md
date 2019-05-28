# door-to-door

### Core project
#### Notions: classes, objects, and graphs

## How to run
./tsp.py --algo [algorithm] file_city

## Introduction
This project will introduce you to a new data structure, graphs, as well as the object-oriented features of Python. It's important that you understand the main concepts of object-oriented programming (classes, objects and methods). So spend a good amount of time structuring properly your solution!

## Your mission
For this project, you will solve a classic problem, the travelling salesman problem. 

The problem is the following: given a list of cities to visit, the travelling salesman must optimise his journey and find the shortest path that goes through all cities, going through each city exactly once. Sounds simple and trivial if there are less than a dozen cities, in which case you can just try all possible permutations and search the the shortest one, but that approach becomes incredibly expensive really quick. You will therefore need to research more appropriate algorithms and heuristics.

For the core part of the project, any exact algorithm or simple heuristics is acceptable.

## Specifications
Your `tsp.py` program will take a filename as argument. That file will be a list of cities, with each line of the form: `city_name, latitude, longitude`

We will take the Euclidean distance as the distance between two cities.

You will compute a path going through all the cities for the travelling salesman, starting with the first city of the file, and output the resulting total length & path on stdout, in the order the cities should be visited.

If the file is improperly formatted, your program will output "Invalid file" on stderr before exiting.

:page_facing_up: [vietnam_cities](/vietnam_cities.csv)

:page_facing_up: [china_cities](/china_cities.csv)

:page_facing_up: [usa_cities](/usa_cities.csv)

## Mandatory classes
You will have to implement two classes: the Node class and the Graph class. 

The Graph class will have a `find_shortest_path` method that will return the solution to the problem as a list.

A Graph object will hold a series of Nodes, with each Node object holding each city's coordinates. It is probably useful to compute the distance between cities (that is, the graph's edges) once and for all as you generate the graph...

You may implement any other methods you need, and use any attributes you deem useful for your classes & objects.

## Evaluation
You are free in the choice of algorithms. Checking that your solution does visit each city once is trivial.

However, and as usual, you will have to demonstrate your understanding of the algorithms you implemented.

---

### BONUS: multiple algorithms
#### Notions: inheritance

## Multiple algorithms
For the bonus part, you will implement several algorithms solving the travelling salesman problem. As many as you want, each implementation will get you points... as long as you understand the algorithm!

For each algorithm, you will create a new class that inherits from the Graph class. The `find_shortest_path` method of the Graph class will become an abstract method and only the derived classes will implement that method.

You will modify your `tsp.py` program so that it accepts an option specifying the algorithm the program will run with to find the solution.
