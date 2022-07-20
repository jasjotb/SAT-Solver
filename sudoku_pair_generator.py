import random
from pysat.card import *
from pysat.formula import *
from pysat.solvers import Solver
import itertools
import csv
vpool = IDPool()


def var(i, j, k):
    return vpool.id(tuple([i + 1, j + 1, k + 1]))


def sudoku_solver(lid, lnum, x, size):
    cnf = CNF()
    s = Solver()

    if (x):
        cnf.append([-x])

    if (x == 0):
        p1 = random.randint(0, size**2 - 1)
        q1 = random.randint(0, size**2 - 1)
        r1 = random.randint(0, size**2 - 1)

        cnf.append([var(p1, q1, r1)])

        p2 = random.randint(size**2, (size**2) * 2 - 1)
        q2 = random.randint(0, size**2 - 1)
        r2 = random.randint(0, size**2 - 1)

        if ((q1 != q2) or (r1 != r2)):
            cnf.append([var(p2, q2, r2)])

    count = 0
    for i in lnum:
        if (i):
            if (lid[count] != x):
                cnf.append([lid[count]])
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
            for val in range(size**2):
                l = []
                for p in range(size * i, size * i + size):
                    for q in range(size * j, size * j + size):
                        l.extend([var(p, q, val)])
                cnf.extend(CardEnc.equals(lits=l, bound=1, encoding=0))

    for j in range(size**2):
        for k in range(size**2):
            for i in range(size**2):
                cnf.append([-var(i, j, k), -var(i + size**2, j, k)])

    s.append_formula(cnf.clauses)
    b = s.solve()

    if (x == 0):
        c = []
        m = s.get_model()
        for i in m:
            if (i > 0):
                c.append(i)
        return c

    if (b == True):
        return 0
    else:
        return 1


def num_sol(lid, lnum, i, size):

    count = sudoku_solver(lid, lnum, i, size)

    if (count == 1):
        return 1
    else:
        return 0


size = int(input())

lid = []
d = []
lnum = []
for i in range((size**2) * 2):
    for j in range(size**2):
        for k in range(size**2):
            lid.extend([var(i, j, k)])
            d.append(0)

lid = sudoku_solver(lid, d, 0, size)

# l2 = []
# for i in lid:
#     a = vpool.obj(i)
#     l2.append(a[2])

# for i in range((size**2) * 2):
#     for j in range(size**2):
#         if ((i == size**2) and (j == 0)):
#             print()
#         p = (size**2) * i + j
#         print(l2[p], end=" ")
#     print()

# print()

random.shuffle(lid)

for i in lid:
    a = vpool.obj(i)
    lnum.append(a[2])

cou = 0
for i in lid:
    if (cou < 2):
        lnum[cou] = 0
        cou += 1
        continue
    y = num_sol(lid, lnum, i, size)
    if (y):
        lnum[cou] = 0
    cou += 1
l1 = []
for i in range((size**4) * 2):
    l1.append(0)
count = 0
for i in lid:
    a = vpool.obj(i)
    b = (size**2) * (a[0] - 1) + a[1]
    l1[b - 1] = lnum[count]
    count += 1
# for i in range((size**2)*2) :
#   for j in range(size**2) :
#     if((i==size**2)and(j==0)) :
#       print()
#     p=(size**2)*i+j
#     print(l1[p],end=",")
#   print()

l = []
count = 0

for i in range(2 * (size**2)):
    l2 = []
    for j in range(size**2):
        l2.append(l1[count])
        count += 1
    l.append(l2)

with open('testo_2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(l)
