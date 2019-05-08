from time import time
from argparse import ArgumentParser
from math import sqrt
from sys import maxsize


class Node(object):
    def __init__(self, info, idx):
        city_params = info.strip('\n').split(', ')
        self.name = city_params[0]
        self.x = float(city_params[1])
        self.y = float(city_params[2])
        self.idx = idx


class Graph(object):
    def __init__(self, ls_of_cities):
        self.ls_of_nodes = []
        self._create_nodes(ls_of_cities)
        self.vetex = len(ls_of_cities)

    def _create_nodes(self, ls_of_cities):
        for idx, city in enumerate(ls_of_cities):
            self.ls_of_nodes.append(Node(city, idx))
        
class nearest_local(object):
    '''
    Nearest neighbor algorithm using bounding box heuristic
    '''
    def __init__(self, graph):
        # total cost
        self.cost = 0
        # final path represented by nodes's index in data file
        self.path = [0]
        # current nodes's index in data file
        self.cur_city = 0
        # graph object
        self.graph = graph
        # list of nodes sorted by x
        self.sorted_x = sorted(graph.ls_of_nodes,key=lambda l:l.x)
        # list of nodes sorted by y
        self.sorted_y = sorted(graph.ls_of_nodes,key=lambda l:l.y)
        # current nodes's index in sorted_x 
        self.pivot = self._find_start_node(self.cur_city, self.sorted_x)

    def solve(self):
        
        # find appropriate increment of bouding box
        inc = min(self._get_inc(self.sorted_x), self._get_inc(self.sorted_y))


        while True:
            x_ref = self.sorted_x[self.pivot].x
            y_ref = self.sorted_x[self.pivot].y

            ls_of_locals, buffer = self._find_local_nodes(inc, x_ref, y_ref)
            min_id = self._find_nearest(ls_of_locals)

            self._update_param(min_id, buffer, ls_of_locals)
            if len(self.path) == self.graph.vetex:
                break
        
        return self.path, self.cost
    
    def _find_start_node(self, start_node, sorted_ls):
        '''
        find start node's index in sorted list by datafile index 'start_node'
        @param:
            start_node: start node's index in data file
            sorted_ls: sorted list
        
        @return:
            index of start node in sorted list
        '''
        for i, node in enumerate(sorted_ls):
            if start_node == node.idx:
                return i

    def _get_inc(self, sorted_ls):
        '''
        find minimum increment of each pair of nodes
        @param: 
            sorted_ls: list of objects Node sorted by particular property
        @return:
            inc: minimum increment
        '''
        min_inc = maxsize
        for i in range(0, len(sorted_ls)-1):
            inc = abs(sorted_ls[i+1].x - sorted_ls[i].x)
            if min_inc > inc:
                min_inc = inc
        return inc

    def _find_local_nodes(self, inc, x_ref, y_ref):
        '''
        Find all nodes in bounding box
        @param:
            inc: bounding box's increment
            x_ref, y_ref: location of current nodes
        @return:
            ls_of_locals: list of all nodes's index in bounding box (index in dataset)
            buffer: list of all nodes's index in bounding box (index in sorted_x)
        '''
        ls_of_locals = []
        buffer = []
        delta = 0.0

        while not ls_of_locals:
            delta += inc
            ls_of_locals = []
            buffer = []

            # check nodes from current node to right side
            for i in range(self.pivot+1, len(self.sorted_x)):
                # check if node is in bounding box by x direction
                if self.sorted_x[i].x <= x_ref + delta:
                    # check if node is in bounding box by y direction
                    if self._in_vertical_bound(self.sorted_x[i], y_ref, delta):
                        ls_of_locals.append(self.sorted_x[i].idx)
                        buffer.append(i)
                else:
                    break
            # check nodes from current node to left side
            for i in range(self.pivot-1, -1, -1):
                # check if node is in bounding box by x direction
                if self.sorted_x[i].x >= x_ref - delta:
                    # check if node is in bounding box by y direction
                    if self._in_vertical_bound(self.sorted_x[i], y_ref, delta):
                        ls_of_locals.append(self.sorted_x[i].idx)
                        buffer.append(i)
                else:
                    break

        return ls_of_locals, buffer

    def _find_nearest(self, ls_of_locals):
        '''
        Find the nearest node out of the list of local nodes
        @param:
            ls_of_locals: list of local nodes
        @return:
            min_id: index of the nearest node
        '''
        min_dist = maxsize
        min_id = None
        
        for city_idx in ls_of_locals:
            dist = self._get_dist(self.graph.ls_of_nodes[city_idx], self.graph.ls_of_nodes[self.cur_city])
            if dist < min_dist:
                min_dist = dist
                min_id = city_idx

        self.cost += min_dist
        return min_id

    def _update_param(self, min_id, buffer, ls_of_locals):
        '''
        Update algorithm's parameter
        @param:
            min_id: index of the nearest node
            buffer: list of all nodes's index in bounding box (index in sorted_x)
            ls_of_locals: list of local nodes
        '''
        self.path.append(min_id)
        self.sorted_x.pop(self.pivot)
        self.cur_city = min_id

        new_pivot = buffer[ls_of_locals.index(min_id)]

        if new_pivot > self.pivot:
            # current node is in left of nearest node, then minus new_pivot by 1
            new_pivot -= 1

        self.pivot = new_pivot

    def _get_dist(self, node_a, node_b):
        '''
        Find distance from node_a to node_b
        @param:
            node_a, node_b: Node objects
        '''
        return sqrt((node_a.x-node_b.x)**2 + (node_a.y-node_b.y)**2)

    def _in_vertical_bound(self, node, y_ref, delta):
        '''
        check if node is in bounding box by y direction
        @param:
            node: particular node
            y_ref: y coordination of node
            delta: half of bounding box's edge
        @return:
            Boolean
        '''
        return node.y <= y_ref + delta and node.y >= y_ref - delta


def print_result(path, ls_of_nodes, cost, total_time):
    '''
    Print complete path by format A -> B -> C -> ...
    '''
    print('Path:')
    print(ls_of_nodes[0].name, end='')
    for idx in path[1:]:
        print(' -> ', end='')
        print(ls_of_nodes[idx].name, end='')
    print('\n\nCost:', cost)
    print('Time:', total_time, '\n')


def main(ls_of_cities):
    start = time()

    graph = Graph(ls_of_cities)
    NN_local = nearest_local(graph)

    
    path, cost = NN_local.solve()
    total_time = time() - start
    print_result(path, graph.ls_of_nodes, cost, total_time)

if __name__ == "__main__":
    with open('usa_cities.csv', 'r') as f:
        ls_of_cities = f.readlines()
        main(ls_of_cities)