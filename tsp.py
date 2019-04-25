from argparse import ArgumentParser


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
    return abs(city_a[0] - city_b[0]) + abs(city_a[1] + city_b[1])



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
                    node_list.append(Node(city[0], (city[1], city[2]))
            return node_list
        except Exception:
            print('Some thing was wrong')
            quit()
    
    def nearest_n(self):
        for index, city in enumerate(self.node_list[1:], 1):
            for pos, ele in enumerate(self.node_list[index:], index):
                
            
        

def main():
    pass


if __name__ == '__main__':
    main()