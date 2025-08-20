from itertools import product


def to_base(n: int, base: int) -> str:
    if n == 0:
        return '0'
    digits = []
    while n > 0:
        digits.append(str(n % base))
        n //= base
    return ''.join(reversed(digits))


# corner points -> 0, 1, 2, 3
# edge points   -> 4, 5, 6, 7
# inner points  -> 8, 9, 10, 11

# 0 - miss
# 0----4----1
# |  8    9 |
# 7         5
# | 11   10 |
# 3----6----2

# 0--1--2--3--4--5--6--7--8
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9

def build_multitype_table_10p():
    """
        Генерирует таблицу из T^4 кейсов, где каждый кейс — dict:
       {0: [...tris], 1: [...], ...}
    """
    # Рёбра: (индекс вершины a, индекс вершины b)
    EDGES = {
        0: (0, 1),  # верх
        1: (1, 2),  # право
        2: (2, 3),  # низ
        3: (3, 0),  # лево
    }
    table = [[] for _ in range(512)]
    for w in (0, 1):
        for vals in product(range(T), repeat=4):
            case_idx = sum(vals[i] * (T ** i) for i in range(4)) + w * 256
            # tables = {t: [] for t in range(T)}
            tables = [[] for _ in range(T)]

            # Для каждого типа состояния внутри клетки
            for t in range(T):
                # границы сегментов для типа t
                segs = [e for e, (a, b) in EDGES.items() if (vals[a] == t) ^ (vals[b] == t)]
                # полностью однородная клетка: два больших треугольника
                if len(set(vals)) == 1:
                    if all(v == t for v in vals):
                        tables[0] = [
                            [0, 3, 1],
                            [1, 3, 2],
                            [0, 0, 0]
                        ]
                        tables[1] = [
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]
                        ]
                        tables[2] = [
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]
                        ]
                        tables[3] = [
                            [0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]
                        ]

                elif len(set(vals)) == 2 and vals[0] != vals[2] and vals[1] != vals[3]:
                    tris = [
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                    ]
                    for c in range(4):
                        if vals[c] == t:
                            rel = [e for e in segs if c in EDGES[e]]
                            if len(rel) == 1:
                                if vals[c] == vals[(c + 1) % 4]:
                                    tris = []
                                    tris.append([c, 4 + (c - 1) % 4, 4 + (c - 3) % 4])
                                    tris.append([c, (c + 1) % 4, 4 + (c + 1) % 4])
                                    tris.append([0, 0, 0])
                    tables[t] = tris
                else:
                # elif (len(set(vals)) == 3 and vals[0] != vals[2] and vals[1] != vals[3]) \
                #         or (len(set(vals)) == 2 and vals[0] == vals[2] and vals[1] == vals[3]) \
                #         or (len(set(vals)) == 3 and (vals[0] == vals[2] or vals[1] == vals[3])) \
                #         or len(set(vals)) == 4:
                    if w == 0:
                        tables[0] = [
                            [7, 8, 0],
                            [0, 8, 4],
                            [0, 0, 0]
                        ]
                        tables[1] = [
                            [4, 8, 1],
                            [8, 10, 1],
                            [10, 5, 1]
                        ]
                        tables[2] = [
                            [5, 10, 2],
                            [2, 10, 6],
                            [0, 0, 0]
                        ]
                        tables[3] = [
                            [10, 6, 3],
                            [8, 10, 3],
                            [8, 3, 7]
                        ]
                    elif w == 1:
                        tables[0] = [
                            [9, 4, 0],
                            [11, 9, 0],
                            [7, 11, 0]
                        ]
                        tables[1] = [
                            [4, 9, 1],
                            [9, 5, 1],
                            [0, 0, 0]
                        ]
                        tables[2] = [
                            [5, 9, 2],
                            [11, 2, 9],
                            [11, 6, 2]
                        ]
                        tables[3] = [
                            [3, 6, 11],
                            [7, 3, 11],
                            [0, 0, 0]
                        ]

            table[case_idx] = tables
    return table


# === Интерполяция на ребре по весам ===
def interp(p1, p2, w1, w2):
    total = w1 + w2
    t = 0.5 if total == 0 else w1 / total
    return (
        p1[0] + t * (p2[0] - p1[0]),
        p1[1] + t * (p2[1] - p1[1]),
    )


import pprint
import pygame
import sys

from data import T
from data import MARGIN_X, MARGIN_Y
from data import WIDTH, HEIGHT, CELL_SIZE
from data import OVERLAY_ALPHA
from data import SURFACE_COLORS, AMBIGUOUS_COLOR, CELL_BORDER_COLOR, BG_COLOR
from data import POINT_RADIUS


# Дискретные точки квадрата 9*9
POINTS_2 = [[0.0] * 9 for i in range(9)]
for i in range(9):
    for j in range(9):
        POINTS_2[i][j] = (i / 8 * CELL_SIZE + MARGIN_X, j / 8 * CELL_SIZE + MARGIN_Y)
print(POINTS_2)



# === Функция рисования по triangle table === #
def draw_case(overlay, val, weights):
    values = val.copy()
    # values[0] = values[0] + 1
    # values[1] = values[1] + 1
    # values[2] = values[2] + 1
    # values[3] = values[3] + 1
    #
    # max_val = max(values[0], values[1])
    # max_val = max(max_val, values[2])
    # max_val = max(max_val, values[3])
    # values[0] = values[0] % max_val + 1
    # values[1] = values[1] % max_val + 1
    # values[2] = values[2] % max_val + 1
    # values[3] = values[3] % max_val + 1
    #
    # max_val = max(values[0], values[1])
    # max_val = max(max_val, values[2])
    # max_val = max(max_val, values[3])
    # values[0] = values[0] % max_val + 1
    # values[1] = values[1] % max_val + 1
    # values[2] = values[2] % max_val + 1
    # values[3] = values[3] % max_val + 1
    #
    # max_val = max(values[0], values[1])
    # max_val = max(max_val, values[2])
    # max_val = max(max_val, values[3])
    # values[0] = values[0] % max_val + 1
    # values[1] = values[1] % max_val + 1
    # values[2] = values[2] % max_val + 1
    # values[3] = values[3] % max_val + 1
    #
    # max_val = max(values[0], values[1])
    # max_val = max(max_val, values[2])
    # max_val = max(max_val, values[3])
    # values[0] = values[0] % max_val
    # values[1] = values[1] % max_val
    # values[2] = values[2] % max_val
    # values[3] = values[3] % max_val

    w_01 = weights[0] + weights[2]
    w_23 = weights[1] + weights[3]
    w = int(w_01 / (w_01 + w_23) + 0.5)
    case = values[0] + values[1] * 4 + values[2] * 16 + values[3] * 64 + w * 256

    POINTS = [[] for _ in range(12)]
    POINTS[0] = POINTS_2[0][0]
    POINTS[1] = POINTS_2[8][0]
    POINTS[2] = POINTS_2[8][8]
    POINTS[3] = POINTS_2[0][8]

    POINTS[4] = POINTS_2[int(weights[0] / (weights[0] + weights[1]) * 8 + 0.5)][0]
    POINTS[5] = POINTS_2[8][int(weights[1] / (weights[1] + weights[2]) * 8 + 0.5)]
    POINTS[6] = POINTS_2[int(weights[3] / (weights[3] + weights[2]) * 8 + 0.5)][8]
    POINTS[7] = POINTS_2[0][int(weights[0] / (weights[0] + weights[3]) * 8 + 0.5)]

    # Усреднить
    center = (
        (POINTS[4][0] + POINTS[5][0] + POINTS[6][0] + POINTS[7][0]) / 4.0,
        (POINTS[4][1] + POINTS[5][1] + POINTS[6][1] + POINTS[7][1]) / 4.0
    )




    POINTS[8] = interp(POINTS[0], center, w_23, w_01)
    POINTS[9] = interp(POINTS[1], center, w_01, w_23)
    POINTS[10] = interp(POINTS[2], center, w_23, w_01)
    POINTS[11] = interp(POINTS[3], center, w_01, w_23)

    # Рисуем поверхности типов 0..T-1
    for t in range(T):
        type = val[t]
        base = SURFACE_COLORS[type]
        fill = (*base, OVERLAY_ALPHA)
        for tri in MULTI_TABLE[case][t]:
            pts = []
            for idx in tri:
                pts.append(POINTS[idx])
            pygame.draw.polygon(overlay, fill, pts)
            pygame.draw.polygon(overlay, base, pts, width=2)


    pygame.draw.circle(screen, AMBIGUOUS_COLOR, center, POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[0], POINTS[4], POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[1], POINTS[5], POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[2], POINTS[6], POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[3], POINTS[7], POINT_RADIUS / 2)

    pygame.draw.circle(screen, (255, 110, 0), POINTS[8], POINT_RADIUS / 2)
    pygame.draw.circle(screen, (110, 0, 255), POINTS[9], POINT_RADIUS / 2)


# === Инициализация Pygame и данные ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-type MS с розовой спорной")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
values = [3, 1, 3, 1]
weights = [0.2, 0.4, 0.2, 0.4]
MULTI_TABLE = build_multitype_table_10p()
pprint.pprint(MULTI_TABLE, width=80)

# === Основной цикл ===
running = True
case = sum(values[i] * (T ** i) for i in range(4))
print(values, f"Текущий case: \n\t {case} (base-10) \n\t {to_base(case, 4)} (base-4)")

while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        # elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
        #     mx, my = ev.pos
        #     for i, (px, py) in POINTS.items():
        #         bx, by = px + BUTTON_OFFSET, py - BUTTON_OFFSET
        #         if pygame.Rect(bx, by, BUTTON_SIZE, BUTTON_SIZE).collidepoint(mx, my):
        #             nw = weights[i] + STEP
        #             weights[i] = 0.1 if nw > 0.9 else round(nw, 1)
        #     for i, (px, py) in POINTS.items():
        #         if (mx - px) ** 2 + (my - py) ** 2 <= POINT_RADIUS ** 2:
        #             values[i] = (values[i] + 1) % T
        #             case = sum(values[i] * (T ** i) for i in range(4))
        #             print(values, f"Новый case: \n\t {case} (base-10) \n\t {to_base(case, 4)} (base-4)")

    screen.fill(BG_COLOR)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_case(overlay, values, weights)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, CELL_BORDER_COLOR, (MARGIN_X, MARGIN_Y, CELL_SIZE, CELL_SIZE), 2)

    # for i, (px, py) in POINTS.items():
    #     col = SURFACE_COLORS[values[i]]
    #     pygame.draw.circle(screen, col, (int(px), int(py)), POINT_RADIUS)
    #     bx, by = px + BUTTON_OFFSET, py - BUTTON_OFFSET
    #     pygame.draw.rect(screen, BUTTON_COLOR, (bx, by, BUTTON_SIZE, BUTTON_SIZE))
    #     txt = font.render(f"{weights[i]:.1f}|{values[i]}", True, BUTTON_TEXT_COLOR)
    #     screen.blit(txt, (bx + 2, by + 2))

    pygame.display.flip()
    clock.tick(1)
pygame.quit()
sys.exit()
