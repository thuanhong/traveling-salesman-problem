#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time
from math import sqrt
from abc import ABC, abstractmethod
import tsp


def take_argument():
    """
    take file name
    @param None
    @return file name
    """
    argument = ArgumentParser()
    argument.add_argument('-a', "--algo", metavar='algorithm',
                          help='choice from [nearest neghbor, nearest insert, random insert, nearest neghbor heuristic]')
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
        cost += euclidean_distance(path[i].position, path[i-1].position)
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
    print('city : ', len(result[0]))
    print('Cost : ', result[1])


class Node:
    """
    Class contain name of cities and position of its
    """
    def __init__(self, name, position):
        self.name = name
        self.position = position


class Graph(ABC):
    """
    Class contain list Node
    each None contain a city and postion its
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.node_list = self.get_node_list()
    
    def get_node_list(self):
        """
        read data from file csv and create a list contain Nodes
        """
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
           
    def Initialization(self):
        """
        Initialization a path contain the city start and the nearest its
        """
        min_distance = euclidean_distance(self.node_list[0].position, self.node_list[1].position)
        closest_city = self.node_list[1]
        for index, _ in enumerate(self.node_list[2:], 2):
            temp_min_distance = euclidean_distance(self.node_list[0].position, self.node_list[index].position)
            if min_distance > temp_min_distance:
                min_distance = temp_min_distance
                closest_city = self.node_list[index]
        self.node_list.remove(closest_city)
        return [self.node_list.pop(0), closest_city]

    # set method find shortest path
    @abstractmethod
    def find_shortest_path(self):
        pass


class nearest_n(Graph):
    """
    class contain algorithm nearest neighbor simple and easy implement-
    """
    def find_shortest_path(self):
        path = [self.node_list.pop(0)]
        cost = 0

        while self.node_list:
            min_cost = euclidean_distance(path[-1].position, self.node_list[0].position)
            min_node = self.node_list[0]
            for node in self.node_list[1:]:
                distance = euclidean_distance(path[-1].position, node.position)
                if min_cost > distance:
                    min_cost = distance
                    min_node = node
            cost += min_cost
            path.append(min_node)
            self.node_list.remove(min_node)

        return path, cost


class random_i(Graph):
    def find_shortest_path(self):
        self.tours = self.Initialization()
        cost = euclidean_distance(self.tours[0].position, self.tours[1].position)
        while self.node_list:
            min_cost = calculate_edge(self.tours[0], self.tours[1], self.node_list[0])
            position_insert = 1
            for index, _ in enumerate(self.tours[2:], 2):
                temp_cost = calculate_edge(self.tours[index-1], self.tours[index], self.node_list[0])
                if min_cost > temp_cost:
                    min_cost = temp_cost
                    position_insert = index
            else:
                self.tours.insert(position_insert, self.node_list.pop(0))
                cost += min_cost
        return self.tours, cost


class nearest_i(Graph):
    def take_nearest_node(self):
        min_distance = float('inf')
        position_min = 0
        for index, _ in enumerate(self.node_list):
            temp_cost = 0
            for city in self.tours:
                temp_cost += euclidean_distance(city.position, self.node_list[index].position)
            else:
                if min_distance > temp_cost:
                    min_distance = temp_cost
                    position_min = index
        return position_min
    
    def find_shortest_path(self):
        self.tours = self.Initialization()
        while self.node_list:
            position_min = self.take_nearest_node()
            
            min_cost = calculate_edge(self.tours[0], self.tours[1], self.node_list[position_min])
            position_insert = 1
            for index, _ in enumerate(self.tours[2:], 2):
                temp_cost = calculate_edge(self.tours[index-1], self.tours[index], self.node_list[position_min])
                if min_cost > temp_cost:
                    min_cost = temp_cost
                    position_insert = index
            else:
                self.tours.insert(position_insert, self.node_list.pop(position_min))
        return self.tours, calculate_cost(self.tours)


class nearest_local(Graph):
    def get_list_cities(self):
        """
        create a list contain all city
        each city is [coordinate x, coordinate y, numerical order in file csv]
        """
        with open(self.file_name, 'r') as file_csv:
            output = []
            for index, city in enumerate(file_csv.readlines()):
                city = city.split(', ')
                output.append([float(city[1]), float(city[2]), int(index)])
            return output

    def find_start_node(self, start_node, sorted_x):
        """
        take position of city begin
        @param start_node : numerical order in file csv
        @param sorted_x : a list sorted have been created by function get_list_cities
        @return index of city begin in list sorted_x
        """
        for index, city in enumerate(sorted_x):
            if start_node == city[2]:
                return index

    def get_inc(self, sorted_x):
        min_inc = float('inf')
        for each in range(0, len(sorted_x)-1):
            inc = abs(sorted_x[each+1][0] - sorted_x[each][0])
            if inc != 0 and min_inc > inc:
                min_inc = inc
        return inc
    
    def take_nearest_neighbor(self, list_neighbor, pivot, sorted_list_x, coordinate, min_distance):
        delta = 0.0
        buffer_x = []
        while not list_neighbor:
            delta += min_distance
            for i, _ in enumerate(sorted_list_x[pivot+1:], pivot+1):
                if sorted_list_x[i][0] <= coordinate[0] + delta:
                    if sorted_list_x[i][1] <= coordinate[1] + delta and sorted_list_x[i][1] >= coordinate[1] - delta:
                        list_neighbor.append(sorted_list_x[i][2])
                        buffer_x.append(i)
                else:
                    break

            for i in range(pivot-1, -1, -1):
                if sorted_list_x[i][0] >= coordinate[0] - delta:
                    if sorted_list_x[i][1] <= coordinate[1] + delta and sorted_list_x[i][1] >= coordinate[1] - delta:
                        list_neighbor.append(sorted_list_x[i][2])
                        buffer_x.append(i)
                else:
                    break
        return buffer_x
    
    def find_shortest_path(self):
        self.list_cities = self.get_list_cities()
        sorted_list_x = sorted(self.list_cities,key=lambda l:l[0])
        sorted_list_y = sorted(self.list_cities,key=lambda l:l[1])
        current_city = 0
        pivot = self.find_start_node(current_city, sorted_list_x)
        min_distance_cities = min(self.get_inc(sorted_list_x), self.get_inc(sorted_list_y))
        cost = 0
        path = [self.node_list[pivot]]
        vetex = len(self.node_list)
        while True:
            list_nearest_neighbor = []
            coordinate = [sorted_list_x[pivot][0], sorted_list_x[pivot][1]]
            buffer_x = self.take_nearest_neighbor(list_nearest_neighbor, pivot, sorted_list_x, coordinate, min_distance_cities)

            min_distance = float('inf')
            min_index = None

            for index in list_nearest_neighbor:
                dist = euclidean_distance(self.list_cities[index], self.list_cities[current_city])
                if dist < min_distance:
                    min_distance = dist
                    min_index = index
            if min_index:
                cost += min_distance
                path.append(self.node_list[min_index])
                sorted_list_x.pop(pivot)
                current_city = min_index
                new_pivot = buffer_x[list_nearest_neighbor.index(min_index)]
                if new_pivot > pivot:
                    new_pivot -= 1
                pivot = new_pivot
                if len(path) == vetex-1:
                    return path, cost
            

def main():
    started = time()  # start calculate time run
    algorithm = {
        'nearest insert':nearest_i,
        'random insert':random_i,
        'nearest neighbor':nearest_n,
        'nearest neighbor heuristic':nearest_local

    }
    args = take_argument()
    if args.algo in algorithm:
        print_result(algorithm[args.algo](args.file).find_shortest_path())
        print('Time : ',str(time()-started)+'\n') # print time run
    else:
        print('Wrong algorithm')


if __name__ == '__main__':
    main()