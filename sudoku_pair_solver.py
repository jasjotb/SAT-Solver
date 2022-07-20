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
            cnf.extend(CardEnc.equals(lits=l, bound=1, encoding=0))


    for i in range(2 * (size**2)):
        for k in range(size**2):
            l1 = []
            for j in range(size**2):
                l1.extend([var(i, j, k)])
            cnf.extend(CardEnc.equals(lits=l1, bound=1, encoding=0))

    for j in range(size**2):
        for k in range(size**2):
            l2 = []
            for i in range(size**2):
                l2.extend([var(i, j, k)])
            cnf.extend(CardEnc.equals(lits=l2, bound=1, encoding=0))

    for j in range(size**2):
        for k in range(size**2):
            l3 = []
            for i in range(size**2, 2 * (size**2)):
                l3.extend([var(i, j, k)])
            cnf.extend(CardEnc.equals(lits=l3, bound=1, encoding=0))

    for i in range(size * 2):
        for j in range(size):
            for k in range(size**2):
                l4 = []
                for p in range(size * i, size * i + size):
                    for q in range(size * j, size * j + size):
                        l4.extend([var(p, q, k)])
                cnf.extend(CardEnc.equals(lits=l4, bound=1, encoding=0))


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

    l = []
    count = 0
    for i in range(2 * (size**2)):
        l1 = []
        for j in range(size**2):
            l1.append(arr[count])
            count += 1
        l.append(l1)

    with open('testo_2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(l)

    # for i in range((size**2) * 2):
    #     for j in range(size**2):
    #         if ((i == size**2) and (j == 0)):
    #             print()
    #         print(arr[(size**2) * i + j], end=" ")
    #     print()

else:
    print('None')
