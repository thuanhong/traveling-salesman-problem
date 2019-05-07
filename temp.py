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
    # fig = pyplot.figure()
    # ax = Axes3D(fig)
    vetex = len(ls_of_cities)
    cost = 0
    start = time()
    path = []
    ls_of_nodes = []
    points = []

    for idx, city in enumerate(ls_of_cities):
        each = list(map(float, city[:-1].split(', ')[1:]))
        points.append(each[::-1])
        each.append(idx)
        ls_of_nodes.append(each)
    print(ls_of_nodes)
        

    sorted_x = sorted(ls_of_nodes,key=lambda l:l[0])
    sorted_y = sorted(ls_of_nodes,key=lambda l:l[1])
    # print(sorted_x[:100])
    # print(sorted_y[:100])
    cur_city = 0
    pivot = find_start_node(cur_city, sorted_x)
    inc_x = get_inc(sorted_x)
    inc_y = get_inc(sorted_y)
    if inc_x < inc_y:
        inc = inc_x
    else:
        inc = inc_y
    print('inc:', inc)
    
    while True:
        # print(pivot, y_id)
        delta = 0.0
        ls_of_common = set()

        x_ref = sorted_x[pivot][0]
        # y_ref = sorted_y[y_id][1]
        y_ref = sorted_x[pivot][1]
        # print('x,y:', x_ref,y_ref)

        
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

            new_pivot = buffer_x[ls_x.index(min_id)]
            # new_y_id = buffer_y[ls_y.index(min_id)]

            if new_pivot > pivot:
                new_pivot -= 1

            # pivot, y_id = new_pivot, new_y_id
            pivot = new_pivot
            # print("xy_id:", pivot, y_id)
            # print(len(path))
            if len(path) == vetex-1:
                print("cost:", cost)
                break
        else:
            break
    print(path)
    print('time:', time()-start)
    # plot(points, path)
    


if __name__ == "__main__":
    with open('vietnam_cities.csv', 'r') as f:
        ls_of_cities = f.readlines()
        main(ls_of_cities)
        # for city in result:
#     print(ls_of_cities[city][:-1])