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
    def __init__(self, name, posx, posy):
        self.name = name
        self.posx = posx
        self.posy = posy


class Graph:
    def __init__(self, file_name):
        



if __name__ == '__main__':