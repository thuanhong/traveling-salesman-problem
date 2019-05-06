from time import time
from math import sqrt


def get_dist(pa, pb):
    return sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)


def find_start_node(start_node, sorted_x):
    for i, c in enumerate(sorted_x):
        if start_node == c[2]:
            return i
        

def get_inc(sorted_x):
    min_inc = float('inf')
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
    points = []

    for idx, city in enumerate(ls_of_cities):
        each = list(map(float, city[:-1].split(', ')[1:]))
        print(each)
        points.append(each[::-1])
        each.append(idx)
        ls_of_nodes.append(each)
        

    sorted_x = sorted(ls_of_nodes,key=lambda l:l[0])
    sorted_y = sorted(ls_of_nodes,key=lambda l:l[1])

    cur_city = 0
    pivot = find_start_node(cur_city, sorted_x)
    inc = min(get_inc(sorted_x), get_inc(sorted_y))
    
    while True:

        delta = 0.0
        ls_of_common = set()

        x_ref = sorted_x[pivot][0]

        y_ref = sorted_x[pivot][1]
        
        while not ls_of_common:
            delta += inc
            ls_x = []
            buffer_x = []

            for i in range(pivot+1, len(sorted_x)):
                if sorted_x[i][0] <= x_ref + delta:
                    if sorted_x[i][1] <= y_ref + delta and sorted_x[i][1] >= y_ref - delta:
                        ls_x.append(sorted_x[i][2])
                        buffer_x.append(i)
                else:
                    break

            for i in range(pivot-1, -1, -1):
                if sorted_x[i][0] >= x_ref - delta:
                    if sorted_x[i][1] <= y_ref + delta and sorted_x[i][1] >= y_ref - delta:
                        ls_x.append(sorted_x[i][2])
                        buffer_x.append(i)
                else:
                    break

            ls_of_common = ls_x.copy()

        min_dist = float('inf')
        min_id = None
        
        for city_id in ls_of_common:
            dist = get_dist(ls_of_nodes[city_id], ls_of_nodes[cur_city])
            if dist < min_dist:
                min_dist = dist
                min_id = city_id
        if min_id:
            cost += min_dist

            path.append(min_id)

            sorted_x.pop(pivot)

            cur_city = min_id

            new_pivot = buffer_x[ls_x.index(min_id)]

            if new_pivot > pivot:
                new_pivot -= 1

            pivot = new_pivot

            if len(path) == vetex-1:
                print("cost:", cost)
                break
        else:
            break


with open('vietnam_cities.csv', 'r') as f:
    main(f.readlines())