from math import inf


def minnode(n, keyval, mstset):
    mini = inf
    mini_index = ''
    for i in range(n):
        if mstset[i] is False and keyval[i] < mini:
            mini = keyval[i]
            mini_index = i
    return mini_index


def findcost(n, city):
    parent = [None]*n
    keyval = [None]*n
    mstset = [None]*n
    
    for i in range(n):
        keyval[i] = inf
        mstset[i] = False
    
    parent[0] = -1
    keyval[0] = 0

    for i in range(n-1):
        u = minnode(n, keyval, mstset)
        mstset[u] = True

        for v in range(n):
            if city[u][v] and mstset[v] is False and city[u][v] < keyval[v]:
                keyval[v] = city[u][v]
                parent[v] = u
    
    cost = 0
    for i in range(n, 1):
        cost += city[parent[i]][i]
    print(cost)

def main():
    n1 = 5
    city1 = [
        [0, 1, 2, 3, 4],
        [1, 0, 5, 0, 7], 
        [2, 5, 0, 6, 0], 
        [3, 0, 6, 0, 0], 
        [4, 7, 0, 0, 0]
    ]
    findcost(n1, city1)

main()