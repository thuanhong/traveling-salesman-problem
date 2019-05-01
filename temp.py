#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time
from math import sqrt


def take_argument():
    """
    take file name
    @param None
    @return file name
    """
    argument = ArgumentParser()
    argument.add_argument('file', help='file name contain the name of cities and its position')
    return argument.parse_args()


def euclidean_distance(city_a, city_b):
    """
    calculate distance between 2 cities
    @param city_a : coordinate of city a (list)
    @param city_b : coordinate of city b (list)
    @return distance physical between 2 cities
    """
    return sqrt((city_a[0] - city_b[0])**2 + (city_a[1] - city_b[1])**2)


def swap_content(node_a, node_b):
    """
    swap name city and position of its from 2 Node
    @param node_a, node_b : node object contain name city and position of city
    @return True
    """
    node_a.name, node_b.name = node_b.name, node_a.name
    node_a.position, node_b.position = node_b.position, node_a.position
    return True


def calculate_edge(city_i, city_j, city_k):
    """
    calculate Cik + Ckj - Cij
    """
    distance_ik = euclidean_distance(city_i.position, city_k.position)
    distance_kj = euclidean_distance(city_k.position, city_j.position)
    distance_ij = euclidean_distance(city_i.position, city_j.position)
    return distance_ik + distance_kj - distance_ij


def calculate_cost(path):
    """
    calculate length of cites visited
    @param path : All cities are arranged so that the roads passing through the cities are the shortest possible
    @return length of roads passing through the cities
    """
    cost = 0
    for i, _ in enumerate(path[1:], 1):
        temp_cost = euclidean_distance(path[i].position, path[i-1].position)
        cost += temp_cost
    return cost


def print_result(result):
    """
    display name of cities
    @param result : include roads passing through the cities and length of roads passing through the cities
    @return None
    """
    print(result[0][0].name, end=' ')
    for city in result[0][1:]:
        print('->', end=' ')
        print(city.name, end=' ')
    print()
    print('Cost : ', result[1])


def build_matrix(list_city):
    matrix = []
    for x in list_city:
        temp = {}
        for index, y in enumerate(list_city):
            temp[index] = [euclidean_distance(x.position, y.position), y]
        matrix.append(temp)
    return matrix


class Node:
    """
    Class contain name of cities and position of its
    """
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Graph:
    """
    
    """
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
    
    def find_shortest_path(self):
        cost = 0
        tour = [self.node_list[0]]
        node_start = 0
        while self.node_list:
            min_cost = float('inf')
            for index, x in enumerate(self.node_list):
                if x.get


def main():
    started = time()  # start calculate time run
    print_result(Graph(take_argument().file).find_shortest_path())
    print('Time : ',str(time()-started)+'\n') # print time run

if __name__ == '__main__':
    main()