#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time 


def take_argument():
    """
    take file name
    @param None
    @return file name
    """
    argument = ArgumentParser()
    argument.add_argument('-a', "--algorithm", type=str, help="choice algorithm to execute")
    argument.add_argument('file', help='file name contain the name of cities and its position')
    return argument.parse_args()


def euclidean_distance(city_a, city_b):
    """
    calculate distance between 2 cities
    @param city_a : coordinate of city a (list)
    @param city_b : coordinate of city b (list)
    @return distance physical between 2 cities
    """
    return abs(city_a[0] - city_b[0]) + abs(city_a[1] - city_b[1])


def swap_content(node_a, node_b):
    """
    swap name city and position of its from 2 Node
    @param node_a, node_b : node object contain name city and position of city
    @return True
    """
    node_a.name, node_b.name = node_b.name, node_a.name
    node_a.position, node_b.position = node_b.position, node_a.position
    return True


class Node:
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Graph:
    def __init__(self, file_name):
        self.file_name = file_name
        self.node_list = self.get_node_list()
    
    def get_node_list(self):
        node_list = []
        try:
            with open(self.file_name) as file_cities:
                for city in file_cities.readlines():
                    city = city.split(', ')
                    node_list.append(Node(city[0], [float(city[1]), float(city[2])]))
            return node_list
        except Exception:
            print('Invalid file')
            quit()


class nearest_n(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
    
    def find_shortest_path(self):
        print(self.node_list[0].name, end=' ')
        for index, city in enumerate(self.node_list[1:], 1):
            print('->', end=' ')
            min_distance = euclidean_distance(self.node_list[index-1].position, self.node_list[index].position)
            for temp_index, _ in enumerate(self.node_list[index+1:], index+1):
                temp_min_distance = euclidean_distance(self.node_list[index-1].position, self.node_list[temp_index].position)
                if min_distance > temp_min_distance:
                    min_distance = temp_min_distance
                    swap_content(self.node_list[index], self.node_list[temp_index])
            print(city.name, end=' ')
        print()

        
def main():
    started = time()  # start calculate time run
    file_name = take_argument().file
    nearest_n(file_name).find_shortest_path()
    print(str(time()-started)+'\n') # print time run


if __name__ == '__main__':
    main()