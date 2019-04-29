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


def print_result(result):
    print(result[0][0].name, end=' ')
    for city in result[0][1:]:
        print('->', end=' ')
        print(city.name, end=' ')
    print()
    print('Cost : ', result[1])


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


class nearest_n_ip(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
    
    def find_shortest_path(self):
        cost = 0
        for index, _ in enumerate(self.node_list[1:], 1):
            min_distance = euclidean_distance(self.node_list[index-1].position, self.node_list[index].position)
            for temp_index, _ in enumerate(self.node_list[index+1:], index+1):
                temp_min_distance = euclidean_distance(self.node_list[index-1].position, self.node_list[temp_index].position)
                if min_distance > temp_min_distance:
                    min_distance = temp_min_distance
                    swap_content(self.node_list[index], self.node_list[temp_index])
            cost += min_distance
        return self.node_list, cost


class nearest_n(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)

    def find_shortest_path(self):
        min_node = self.node_list.pop(0)
        path = [min_node]
        cost = 0

        while self.node_list:
            temp = []

            for node in self.node_list:
                distance = euclidean_distance(min_node.position, node.position)
                temp.append((node, distance))

            min_node, min_cost = min(temp, key=lambda i: i[1])
            cost += min_cost
            path.append(min_node)
            self.node_list.remove(min_node)

        return path, cost


class nearest_i(Graph):
    def __init__(self, file_name):
        Graph.__init__(self, file_name)
        self.tours = self.Initialization()
    
    def calculate_edge(self, city_i, city_j, city_k):
        distance_ik = euclidean_distance(city_i.position, city_k.position)
        distance_kj = euclidean_distance(city_k.position, city_j.position)
        distance_ij = euclidean_distance(city_i.position, city_j.position)
        return distance_ik + distance_kj - distance_ij
    
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
    
    def calculate_cost(self):
        cost = 0
        for i, _ in enumerate(self.tours[1:], 1):
            temp_cost = euclidean_distance(self.tours[i].position, self.tours[i-1].position)
            cost += temp_cost
        return cost

    def find_shortest_path(self):
        while self.node_list:
            min_cost = self.calculate_edge(self.tours[0], self.tours[1], self.node_list[0])
            position_insert = 1
            for x, _ in enumerate(self.tours[2:], 2):
                temp_cost = self.calculate_edge(self.tours[x-1], self.tours[x], self.node_list[0])
                if min_cost > temp_cost:
                    min_cost = temp_cost
                    position_insert = x
            else:
                self.tours.insert(position_insert, self.node_list.pop(0))
            
        return self.tours, self.calculate_cost()

        
def main():
    started = time()  # start calculate time run
    algorithm = {
        'nearest_i':nearest_i,
        'nearest_n':nearest_n,
        'nearest_n_ip':nearest_n_ip
    }
    args = take_argument()
    if args.algo in algorithm:
        print_result(algorithm[args.algo](args.file).find_shortest_path())
        print('Time : ',str(time()-started)+'\n') # print time run
    else:
        print('Wrong choice')


if __name__ == '__main__':
    main()