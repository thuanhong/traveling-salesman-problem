from time import time
from math import sqrt
from sys import maxsize


def get_dist(pa, pb):
    return sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)


def find_start_node(start_node, sorted_x):
    for i, c in enumerate(sorted_x):
        if start_node == c[2]:
            return i
        

def get_inc(sorted_x):
    min_inc = maxsize
    # try:
    for each in range(0, len(sorted_x)-1):
        inc = abs(sorted_x[each+1][0] - sorted_x[each][0])
        if min_inc > inc:
            min_inc = inc

    return inc


def main(ls_of_cities):
    vetex = len(ls_of_cities)
    cost = 0
    path = []
    ls_of_nodes = []

    for idx, city in enumerate(ls_of_cities):
        city = city.split(', ')
        ls_of_nodes.append([float(city[1]), float(city[2]), idx])
        

    sorted_x = sorted(ls_of_nodes,key=lambda l:l[0])
    # sorted_y = sorted(ls_of_nodes,key=lambda l:l[1])
    # print(sorted_y[:100])
    cur_city = 0
    pivot = find_start_node(cur_city, sorted_x)
    # inc = min(get_inc(sorted_x), get_inc(sorted_y))
    inc = get_inc(sorted_x)
    
    while True:
        # print(pivot, y_id)
        delta = 0.0
        ls_of_common = []

        coor = [sorted_x[pivot][0], sorted_x[pivot][1]]
        
        while not ls_of_common:
            delta += inc
            buffer_x = []

            for i in range(pivot+1, len(sorted_x)):
                if sorted_x[i][0] <= coor[0] + delta:
                    if sorted_x[i][1] <= coor[1] + delta and sorted_x[i][1] >= coor[1] - delta:
                        ls_of_common.append(sorted_x[i][2])
                        buffer_x.append(i)
                else:
                    break

            for i in range(pivot-1, -1, -1):
                if sorted_x[i][0] >= coor[0] - delta:
                    if sorted_x[i][1] <= coor[1] + delta and sorted_x[i][1] >= coor[1] - delta:
                        ls_of_common.append(sorted_x[i][2])
                        buffer_x.append(i)
                else:
                    break

        # print(ls_of_common)
        min_dist = maxsize
        min_id = None
        
        for city_id in ls_of_common:
            dist = get_dist(ls_of_nodes[city_id], ls_of_nodes[cur_city])
            if dist < min_dist:
                min_dist = dist
                min_id = city_id
        if min_id:
            cost += min_dist
            # print("min", min_dist)
            path.append(min_id)
            # print(ls_of_cities[min_id])
            # print(delta)
            sorted_x.pop(pivot)
            # sorted_y.pop(y_id)
            cur_city = min_id

            new_pivot = buffer_x[ls_of_common.index(min_id)]
            # new_y_id = buffer_y[ls_y.index(min_id)]

            if new_pivot > pivot:
                new_pivot -= 1

            # pivot, y_id = new_pivot, new_y_id
            pivot = new_pivot
            # print("xy_id:", pivot, y_id)
            # print(len(path))
            if len(path) == vetex-1:
                return path, cost
    # plot(points, path)
    


if __name__ == "__main__":
    st = time()
    with open('usa_cities.csv', 'r') as f:
        ls_of_cities = f.readlines()
        path, cost = main(ls_of_cities)
        for x in path:
            print(ls_of_cities[x], end =' -> ')
    print('Time : ',str(time()-st)+'\n')
