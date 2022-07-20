from pysat.card import *
from pysat.formula import *
from pysat.solvers import Solver
import itertools
import csv

vpool = IDPool()


def var(i, j, k):
    return vpool.id(tuple([i + 1, j + 1, k + 1]))


def sudoku_solver(lnum, size):
    cnf = CNF()
    s = Solver()
    vpool = IDPool()

    count = 0
    for i in lnum:
        if (i):
            p = count // (size**2)
            q = count % (size**2)
            i = i - 1
            cnf.append([var(p, q, i)])
        count += 1

    for i in range((size**2) * 2):
        for j in range(size**2):
            l = []
            for k in range(size**2):
                l.extend([var(i, j, k)])
            cnf.append(l)

    for i in range(2 * (size**2)):
        for j in range(size**2):
            for k1, k2 in itertools.combinations(range(size**2), 2):
                cnf.append([-var(i, j, k1), -var(i, j, k2)])

    for i in range(2 * (size**2)):
        for k in range(size**2):
            for j1, j2 in itertools.combinations(range(size**2), 2):
                cnf.append([-var(i, j1, k), -var(i, j2, k)])

    for j in range(size**2):
        for k in range(size**2):
            for i1, i2 in itertools.combinations(range(size**2), 2):
                cnf.append([-var(i1, j, k), -var(i2, j, k)])

    for j in range(size**2):
        for k in range(size**2):
            for i1, i2 in itertools.combinations(range(size**2, 2 * (size**2)),
                                                 2):
                cnf.append([-var(i1, j, k), -var(i2, j, k)])

    for val in range(size**2):
        for i in range(size * 2):
            for j in range(size):
                subgrid = itertools.product(range(size * i, size * i + size),
                                            range(size * j, size * j + size))
                for c in itertools.combinations(subgrid, 2):
                    cnf.append([
                        -var(c[0][0], c[0][1], val),
                        -var(c[1][0], c[1][1], val)
                    ])

    for j in range(size**2):
        for k in range(size**2):
            for i in range(size**2):
                cnf.append([-var(i, j, k), -var(i + size**2, j, k)])

    s.append_formula(cnf.clauses)
    q = s.solve()
    if (q == True):
        a = s.get_model()
        b = []
        for i in a:
            if (i > 0):
                b.append(i)
        return b

    else:
        return None

x = []
z = []
size = int(input())

with open('testo_1.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        z.extend(row)

for i in z:
    x.append(int(i))

# for i in range(2*(size**4)) :
#   x.append(0)

for i in range((size**2) * 2):
    for j in range(size**2):
        for k in range(size**2):
            a = var(i, j, k)

y = sudoku_solver(x, size)
if (y != None):
    arr = []
    for i in y:
        a = vpool.obj(i)
        arr.append(a[2])

    for i in range((size**2) * 2):
        for j in range(size**2):
            if ((i == size**2) and (j == 0)):
                print()
            print(arr[(size**2) * i + j], end=" ")
        print()

else:
    print('None')
