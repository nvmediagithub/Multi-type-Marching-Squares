from itertools import product

WIDTH, HEIGHT = 400, 400
CELL_SIZE = 200
MARGIN_X = (WIDTH - CELL_SIZE) // 2
MARGIN_Y = (HEIGHT - CELL_SIZE) // 2

POINTS_2 = [[0.0] * 9 for i in range(9)]
for i in range(9):
    for j in range(9):
        POINTS_2[i][j] = (i / 8 * CELL_SIZE + MARGIN_X, j / 8 * CELL_SIZE + MARGIN_Y)
print(POINTS_2)


for vals in product(range(4), repeat=4):
    print(vals)