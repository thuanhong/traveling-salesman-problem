from math import inf


def minnode(n, keyval, mstset):
    mini = inf
    mini_index = ''
    for i, _ in enumerate(n):
        if mstset[i] is False and keyval[i] < mini:
            mini = keyval[i]
            mini_index = i
    return mini_index


def findcost(n, city):
    parent = []
    keyval = []
    mstset = []
    
    for i, _ in enumerate(n):
        keyval[i] = inf
        mstset[i] = False
    
    