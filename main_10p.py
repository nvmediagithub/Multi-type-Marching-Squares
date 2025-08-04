import pprint
import pygame
import sys

from data import T, EDGES, POINTS
from data import MARGIN_X, MARGIN_Y
from data import WIDTH, HEIGHT, CELL_SIZE
from data import BUTTON_OFFSET, BUTTON_SIZE, IP_ADJ
from data import OVERLAY_ALPHA
from data import STEP
from data import SURFACE_COLORS, AMBIGUOUS_COLOR, BUTTON_TEXT_COLOR, BUTTON_COLOR, CELL_BORDER_COLOR, BG_COLOR
from data import POINT_RADIUS

from ms_multitype_10p import interp, build_multitype_table_10p, to_base


def find_position(A, B, C, w):
    """
    Нахождение позиции на полилинии ABC с использованием параметра w.

    Параметры:
    A, B, C -- точки в формате (x, y)
    w -- параметр от 0 до 1, где:
         w = 0 -> точка A
         w = 0.5 -> точка B
         w = 1 -> точка C

    Возвращает:
    Кортеж (x, y) с координатами найденной точки
    """
    if w <= 0.5:
        # Интерполяция на отрезке AB (0 <= w <= 0.5)
        t = 2 * w  # Нормализация параметра для отрезка AB
        x = A[0] + t * (B[0] - A[0])
        y = A[1] + t * (B[1] - A[1])
    else:
        # Интерполяция на отрезке BC (0.5 < w <= 1)
        t = 2 * (w - 0.5)  # Нормализация параметра для отрезка BC
        x = B[0] + t * (C[0] - B[0])
        y = B[1] + t * (C[1] - B[1])

    return (x, y)



# === Функция рисования по triangle table ===
def draw_case(overlay, case, weights):
    ep = [()] * 4
    for i in range(4):
        a, b = EDGES[i]
        ep[i] = interp(POINTS[a], POINTS[b], weights[a], weights[b])

    center = (
        (ep[0][0] + ep[1][0] + ep[2][0] + ep[3][0]) / 4.0,
        (ep[0][1] + ep[1][1] + ep[2][1] + ep[3][1]) / 4.0
    )

    w_01 = weights[0] + weights[2]
    w_23 = weights[1] + weights[3]
    w = w_01 / (w_01 + w_23)
    ip = [()] * 2
    ip[0] = find_position(POINTS[0], center, POINTS[3], w)
    ip[1] = find_position(POINTS[2], center, POINTS[1], w)

    # Рисуем поверхности типов 0..T-1
    for t in range(T):
        # if t in (1, 3):
        #     continue
        base = SURFACE_COLORS[t]
        fill = (*base, OVERLAY_ALPHA)
        for tri in MULTI_TABLE[case][t]:
            pts = []
            for kind, idx in tri:
                if kind == 'p':
                    pts.append(POINTS[idx])
                elif kind == 'e':
                    pts.append(ep[idx])
                elif kind == 'ip':
                    pts.append(ip[idx])

            pygame.draw.polygon(overlay, fill, pts)
            pygame.draw.polygon(overlay, base, pts, width=2)


    pts = []
    for kind, idx in MULTI_TABLE[case]['aband'][0]:
        if kind == 'p':
            pts.append(POINTS[idx])
        elif kind == 'e':
            pts.append(ep[idx])
        elif kind == 'ip':
            pts.append(ip[idx])


    base = SURFACE_COLORS[1]
    fill = (*base, OVERLAY_ALPHA)
    if w > 0.5:
        base = SURFACE_COLORS[0]
        fill = (*base, OVERLAY_ALPHA)

    pygame.draw.polygon(overlay, fill, pts)
    pygame.draw.polygon(overlay, base, pts, width=2)

    pts = []
    for kind, idx in MULTI_TABLE[case]['aband'][1]:
        if kind == 'p':
            pts.append(POINTS[idx])
        elif kind == 'e':
            pts.append(ep[idx])
        elif kind == 'ip':
            pts.append(ip[idx])


    base = SURFACE_COLORS[3]
    fill = (*base, OVERLAY_ALPHA)
    if w > 0.5:
        base = SURFACE_COLORS[2]
        fill = (*base, OVERLAY_ALPHA)

    pygame.draw.polygon(overlay, fill, pts)
    pygame.draw.polygon(overlay, base, pts, width=2)

    pygame.draw.circle(screen, AMBIGUOUS_COLOR, center, POINT_RADIUS / 2)

    pygame.draw.circle(screen, SURFACE_COLORS[0], ep[0], POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[1], ep[1], POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[2], ep[2], POINT_RADIUS / 2)
    pygame.draw.circle(screen, SURFACE_COLORS[3], ep[3], POINT_RADIUS / 2)

    pygame.draw.circle(screen, (255, 110, 0), ip[0], POINT_RADIUS / 2)
    pygame.draw.circle(screen, (110, 0, 255), ip[1], POINT_RADIUS / 2)


# === Инициализация Pygame и данные ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-type MS с розовой спорной")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
values = [0, 1, 2, 3]
weights = [0.2, 0.4, 0.8, 0.4]
MULTI_TABLE = build_multitype_table_10p()
pprint.pprint(MULTI_TABLE, width=80)

# === Основной цикл ===
running = True
case = sum(values[i] * (T ** i) for i in range(4))
print(f"Текущий case: \n\t {case} (base-10) \n\t {to_base(case, 4)} (base-4)")

while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos
            for i, (px, py) in POINTS.items():
                bx, by = px + BUTTON_OFFSET, py - BUTTON_OFFSET
                if pygame.Rect(bx, by, BUTTON_SIZE, BUTTON_SIZE).collidepoint(mx, my):
                    nw = weights[i] + STEP
                    weights[i] = 0.1 if nw > 0.9 else round(nw, 1)
            for i, (px, py) in POINTS.items():
                if (mx - px) ** 2 + (my - py) ** 2 <= POINT_RADIUS ** 2:
                    values[i] = (values[i] + 1) % T
                    case = sum(values[i] * (T ** i) for i in range(4))
                    print(f"Новый case: \n\t {case} (base-10) \n\t {to_base(case, 4)} (base-4)")

    case = sum(values[i] * (T ** i) for i in range(4))
    screen.fill(BG_COLOR)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_case(overlay, case, weights)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, CELL_BORDER_COLOR, (MARGIN_X, MARGIN_Y, CELL_SIZE, CELL_SIZE), 2)
    for i, (px, py) in POINTS.items():
        col = SURFACE_COLORS[values[i]]
        pygame.draw.circle(screen, col, (int(px), int(py)), POINT_RADIUS)
        bx, by = px + BUTTON_OFFSET, py - BUTTON_OFFSET
        pygame.draw.rect(screen, BUTTON_COLOR, (bx, by, BUTTON_SIZE, BUTTON_SIZE))
        txt = font.render(f"{weights[i]:.1f}|{values[i]}", True, BUTTON_TEXT_COLOR)
        screen.blit(txt, (bx + 2, by + 2))
    pygame.display.flip()
    clock.tick(1)
pygame.quit()
sys.exit()
