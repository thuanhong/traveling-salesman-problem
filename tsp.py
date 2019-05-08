#!/usr/bin/env python3
from argparse import ArgumentParser
from time import time
from math import sqrt
from abc import ABC, abstractmethod


def take_argument():
    """
    take file name
    @param None
    @return file name, name of algorithm
    """
    argument = ArgumentParser()
    argument.add_argument('-a', "--algo",
                          metavar='algorithm',
                          default='nearest neghbor',
                          help='choice from [nearest neghbor, nearest insert,\
                                random insert, nearest neghbor heuristic]')
    argument.add_argument('file', help='file name contain the name of cities\
                                        and its position')
    return argument.parse_args()


def euclid_distance(city_a, city_b):
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
    distance_ik = euclid_distance(city_i.position, city_k.position)
    distance_kj = euclid_distance(city_k.position, city_j.position)
    distance_ij = euclid_distance(city_i.position, city_j.position)
    return distance_ik + distance_kj - distance_ij


def calculate_cost(path):
    """
    calculate length of cites visited
    @param path : All cities are arranged so that the roads
                  passing through the cities are the shortest possible
    @return length of roads passing through the cities
    """
    cost = 0
    for i, _ in enumerate(path[1:], 1):
        cost += euclid_distance(path[i].position, path[i-1].position)
    return cost


def print_result(result):
    """
    display name of cities
    @param result : include roads passing through the cities
                    and length of roads passing through the cities
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
    def __init__(self, name, position, index):
        self.name = name
        self.position = position
        self.index = index


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
                for index, city in enumerate(file_cities.readlines()):
                    city = city.split(', ')
                    node_list.append(Node(city[0],
                                          [float(city[1]), float(city[2])],
                                          index))
            return node_list
        except Exception:
            print('Invalid file')
            quit()

    def Initialization(self):
        """
        Initialization a path contain the city start and the nearest its
        """
        min_distance = euclid_distance(self.node_list[0].position,
                                       self.node_list[1].position)
        closest_city = self.node_list[1]
        for index, _ in enumerate(self.node_list[2:], 2):
            temp_distance = euclid_distance(self.node_list[0].position,
                                            self.node_list[index].position)
            if min_distance > temp_distance:
                min_distance = temp_distance
                closest_city = self.node_list[index]
        self.node_list.remove(closest_city)
        return [self.node_list.pop(0), closest_city]

    # set method find shortest path
    @abstractmethod
    def find_shortest_path(self):
        pass


class Nearest_n(Graph):
    """
    class contain algorithm nearest neighbor simple and easy implement
    starts at a random city and repeatedly visits the nearest city until
    all have been visited
    class inherit attribute from class Graph
    """
    def find_shortest_path(self):
        # create a list output contain the city begin
        path = [self.node_list.pop(0)]
        # total length road pass thorght all city
        cost = 0
        while self.node_list:
            """
            declare min cost is eucli distance from last city
            in the path to the first city in node list
            """
            min_cost = euclid_distance(path[-1].position,
                                       self.node_list[0].position)
            # declare min node is the first city in node list
            min_node = self.node_list[0]
            # calculate from the last city in the path to all city in node list
            for node in self.node_list[1:]:
                distance = euclid_distance(path[-1].position, node.position)
                if min_cost > distance:
                    min_cost = distance
                    min_node = node
            cost += min_cost
            path.append(min_node)
            self.node_list.remove(min_node)
        return path, cost


class Arbitrary_i(Graph):
    """
    class contain algorithm arbitrary insert
    starts at a random city and choice arbitrary city in node list.
    Then, insert it at the path base on formula Cik + Cjk - Cij
    class inherit attribute from class Graph
    """
    def find_shortest_path(self):
        # create a path with 2 cities include the first city
        # in node list and the city nearest its
        self.tours = self.Initialization()
        # declare cost is distance from first city in self.tours with self
        cost = euclid_distance(self.tours[0].position, self.tours[1].position)
        while self.node_list:
            # calculate cost between the first city and
            # the second city in self.tours and
            min_cost = calculate_edge(self.tours[0],
                                      self.tours[1],
                                      self.node_list[0])
            position_insert = 1
            # insert city have been chosen from node list
            for index, _ in enumerate(self.tours[2:], 2):
                temp_cost = calculate_edge(self.tours[index-1],
                                           self.tours[index],
                                           self.node_list[0])
                if min_cost > temp_cost:
                    min_cost = temp_cost
                    position_insert = index
            else:
                self.tours.insert(position_insert, self.node_list.pop(0))
                cost += min_cost
        return self.tours, cost


class Nearest_i(Graph):
    """
    class contain algorithm nearest insert
    """
    def take_nearest_node(self):
        """
        take city nearest the path
        @param None
        @return index of city nearest the path
        """
        min_distance = float('inf')
        position_min = 0
        for index, _ in enumerate(self.node_list):
            temp_cost = 0
            for city in self.tours:
                temp_cost += euclid_distance(city.position,
                                             self.node_list[index].position)
            else:
                if min_distance > temp_cost:
                    min_distance = temp_cost
                    position_min = index
        return position_min

    def find_shortest_path(self):
        # create a path have 2 two cities nearest
        self.tours = self.Initialization()
        while self.node_list:
            # take city have distance min
            position_min = self.take_nearest_node()
            # insert city have at the path
            min_cost = calculate_edge(self.tours[0],
                                      self.tours[1],
                                      self.node_list[position_min])
            position_insert = 1
            for index, _ in enumerate(self.tours[2:], 2):
                temp_cost = calculate_edge(self.tours[index-1],
                                           self.tours[index],
                                           self.node_list[position_min])
                if min_cost > temp_cost:
                    min_cost = temp_cost
                    position_insert = index
            else:
                self.tours.insert(position_insert,
                                  self.node_list.pop(position_min))
        return self.tours, calculate_cost(self.tours)


class Nearest_local(Graph):
    """
    nearest neighbor with a heuristic
    the algorithm will sorted the node list and
    take min distance between x and y in the list sorted
    Then, the algorithm base on min distance to find nearest neighbor
    """
    def Init(self):
        self.sort_ls_x = sorted(self.node_list,
                                key=lambda l: l.position[0])
        # get index of the begin city in the list sorted
        self.pivot = self.find_start_node()
        self.current_x = None
        self.current_y = None

    def find_start_node(self):
        """
        take position of city begin
        @return index of city begin in list sorted_x
        """
        for index, city in enumerate(self.sort_ls_x):
            if city.index == 0:
                return index

    def sub_take_nearest_neighbor(self, list_neighbor, delta, i):
        if self.sort_ls_x[i].position[1] <= self.current_y + delta\
           and self.sort_ls_x[i].position[1] >= self.current_y - delta:
            list_neighbor.append(i)

    def take_nearest_neighbor(self, list_neighbor):
        """
        take nearest city
        the function will append cities nearest in range :
        coordinate_x - delta <= coordinate_x <= coordinate_x + delta
        """
        delta = 0.0
        while not list_neighbor:
            delta += 0.2
            for i, _ in enumerate(self.sort_ls_x[self.pivot+1:], self.pivot+1):
                if self.sort_ls_x[i].position[0] <= self.current_x + delta:
                    self.sub_take_nearest_neighbor(list_neighbor, delta, i)
                else:
                    break

            for i in range(self.pivot-1, -1, -1):
                if self.sort_ls_x[i].position[0] >= self.current_x - delta:
                    self.sub_take_nearest_neighbor(list_neighbor, delta, i)
                else:
                    break
        return

    def find_shortest_path(self):
        self.Init()
        output = []
        vetex = len(self.node_list)
        while True:
            list_nearest_neighbor = []
            self.current_x = self.sort_ls_x[self.pivot].position[0]
            self.current_y = self.sort_ls_x[self.pivot].position[1]
            self.take_nearest_neighbor(list_nearest_neighbor)

            min_distance = float('inf')
            min_index = None
            # take city nearset in list all nearest neighbor have been found
            for index in list_nearest_neighbor:
                dist = euclid_distance(self.sort_ls_x[self.pivot].position,
                                       self.sort_ls_x[index].position)
                if min_distance > dist:
                    min_distance = dist
                    min_index = index
            # append city pivot at output
            # set new pivot is index of nearest neighbor
            output.append(self.sort_ls_x[self.pivot])
            self.sort_ls_x.pop(self.pivot)
            """
            when index of nearest neighbor greater than pivot
            the new pivot decrease by 1
            Because the city in old pivot have been pop
            """
            if min_index > self.pivot:
                min_index -= 1
            self.pivot = min_index
            if len(output) == vetex-1:
                output += self.sort_ls_x
                return output, calculate_cost(output)


def main():
    started = time()  # start calculate time run
    algorithm = {
        'nearest_insert': Nearest_i,
        'arbitrary_insert': Arbitrary_i,
        'nearest_neighbor': Nearest_n,
        'nearest_local': Nearest_local
    }
    args = take_argument()
    if args.algo in algorithm:
        print_result(algorithm[args.algo](args.file).find_shortest_path())
        print('Time : ', str(time()-started)+'\n')  # print time run
    else:
        print('Wrong algorithm')


if __name__ == '__main__':
    main()
