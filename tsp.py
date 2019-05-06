#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time
from math import sqrt
import tsp


def take_argument():
    """
    take file name
    @param None
    @return file name
    """
    argument = ArgumentParser()
    argument.add_argument('-a', "--algo", type=str, help="choice algorithm to execute")
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
    
    def Initialization(self):
        min_distance = euclidean_distance(self.node_list[0].position, self.node_list[1].position)
        closest_city = self.node_list[1]
        for index, _ in enumerate(self.node_list[2:], 2):
            temp_min_distance = euclidean_distance(self.node_list[0].position, self.node_list[index].position)
            if min_distance > temp_min_distance:
                min_distance = temp_min_distance
                closest_city = self.node_list[index]
        self.node_list.remove(closest_city)
        return [self.node_list.pop(0), closest_city]


class nearest_n_ip(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
    
    def find_shortest_path(self):
        cost = 0
        for index, _ in enumerate(self.node_list[1:], 1):
            min_distance = euclidean_distance(self.node_list[index-1].position, self.node_list[index].position)
            min_index = index
            for temp_index, _ in enumerate(self.node_list[index+1:], index+1):
                temp_min_distance = euclidean_distance(self.node_list[index-1].position, self.node_list[temp_index].position)
                if min_distance > temp_min_distance:
                    min_distance = temp_min_distance
                    min_index = temp_index
            swap_content(self.node_list[index], self.node_list[min_index])
            cost += min_distance
        return self.node_list, cost


class nearest_n(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)

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


class nearest_i_abr(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
        self.tours = self.Initialization()

    def find_shortest_path(self):
        cost = euclidean_distance(self.tours[0].position, self.tours[1].position)
        while self.node_list:
            min_cost = calculate_edge(self.tours[0], self.tours[1], self.node_list[0])
            position_insert = 0
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
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
        self.tours = self.Initialization()

    def find_shortest_path(self):
        while self.node_list:
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
    

class heu(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
        self.tours = self.Initialization()
    
    def find_shortest_path(self):
        while self.node_list:
            for index, _ in enumerate(self.tours[1:], 1):
                temp_cost = euclidean_distance(self.tours[index-1].position, self.tours[index].position)
                if temp_cost > euclidean_distance(self.tours[index-1].position, self.node_list[0].position):
                    self.tours.insert(index, self.node_list.pop(0))
            # else:
            #     self.tours.append(self.node_list.pop(0))
        return self.tours, calculate_cost(self.tours)
        

def main():
    started = time()  # start calculate time run
    algorithm = {
        'nearest_i':nearest_i,
        'nearest_i_abr':nearest_i_abr,
        'nearest_n':nearest_n,
        'nearest_n_ip':nearest_n_ip,
        'heu':heu
    }
    args = take_argument()
    if args.algo in algorithm:
        print_result(algorithm[args.algo](args.file).find_shortest_path())
        print('Time : ',str(time()-started)+'\n') # print time run
    else:
        print('Wrong choice')


if __name__ == '__main__':
    main()