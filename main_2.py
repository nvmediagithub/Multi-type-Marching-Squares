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

from ms_multitype import interp, build_multitype_table_2, to_base


# === Функция рисования по triangle table ===
def draw_case(overlay, case, weights):
    # Рисуем поверхности типов 0..T-1
    for t in range(T):
        base = SURFACE_COLORS[t]
        fill = (*base, OVERLAY_ALPHA)
        for tri in MULTI_TABLE[case][t]:
            pts = []
            for kind, idx in tri:
                if kind == 'p':
                    pts.append(POINTS[idx])
                elif kind == 'e':
                    a, b = EDGES[idx]
                    pts.append(interp(POINTS[a], POINTS[b], weights[a], weights[b]))
                elif kind == 'ip':

                    # # Вариант построения номер 1
                    # R_I_P = [()]*4
                    # for i in range(4):
                    #     a, b = EDGES[i]
                    #     R_I_P[i] = interp(POINTS[a], POINTS[b], weights[a], weights[b])
                    # W_E = [0] * 4
                    # for i in range(4):
                    #     a, b = EDGES[i]
                    #     W_E[i] = weights[a] + weights[b]
                    # I_P = [()]*4
                    # center_a = ((R_I_P[0][0] + R_I_P[2][0]) / 2, (R_I_P[0][1] + R_I_P[2][1]) / 2)
                    # center_b = ((R_I_P[1][0] + R_I_P[3][0]) / 2, (R_I_P[1][1] + R_I_P[3][1]) / 2)
                    #
                    # # # Вычисление обратных весов
                    # # inv_weights = [1 / w for w in weights]
                    # # # Сумма обратных весов
                    # # total_weight = sum(inv_weights)
                    # # # Взвешенное среднее для координат
                    # # x = sum(POINTS[i][0] * inv_weights[i] for i in range(4)) / total_weight
                    # # y = sum(POINTS[i][1] * inv_weights[i] for i in range(4)) / total_weight
                    # # # INNER_POINTS[4] = (x, y)
                    # # center_a = (x, y)
                    # # center_b = (x, y)
                    #
                    # weight_a = abs(W_E[0] - W_E[2])
                    # weight_b = abs(W_E[3] - W_E[1])
                    # I_P[0] = interp(R_I_P[0], center_a, W_E[0], weight_a)
                    # I_P[1] = interp(R_I_P[1], center_b, W_E[1], weight_b)
                    # I_P[2] = interp(center_a, R_I_P[2], weight_a, W_E[2])
                    # I_P[3] = interp(center_b, R_I_P[3], weight_b, W_E[3])
                    # pts.append(I_P[idx])
                    # # Конец варианта построения номер 1

                    # Вариант построения номер 2
                    R_I_P = [()]*4
                    for i in range(4):
                        a, b = EDGES[i]
                        R_I_P[i] = interp(POINTS[a], POINTS[b], weights[a], weights[b])
                    W_E = [0] * 4
                    for i in range(4):
                        a, b = EDGES[i]
                        W_E[i] = weights[a] + weights[b]

                    x = R_I_P[idx][0] + R_I_P[(idx + 1) % 4][0] + R_I_P[(idx - 1) % 4][0]
                    y = R_I_P[idx][1] + R_I_P[(idx + 1) % 4][1] + R_I_P[(idx - 1) % 4][1]
                    p = (x / 3.0, y / 3.0)
                    pts.append(p)
                    # Конец варианта построения номер 2

            pygame.draw.polygon(overlay, fill, pts)
            pygame.draw.polygon(overlay, base, pts, width=2)

    # # Рисуем спорную область (aband) розовым
    # pink_fill = (*AMBIGUOUS_COLOR, OVERLAY_ALPHA)
    # for tri in MULTI_TABLE[case]['aband']:
    #     pts = []
    #     for kind, idx in tri:
    #         if kind == 'p':
    #             pts.append(POINTS[idx])
    #         elif kind == 'e':
    #             a, b = EDGES[idx]
    #             pts.append(interp(POINTS[a], POINTS[b], weights[a], weights[b]))
    #         elif kind == 'ip':
    #             a, b = EDGES[idx]
    #             pts.append(interp(INNER_POINTS[a], INNER_POINTS[b], weights[a], weights[b]))
    #             # pts.append(INNER_POINTS[idx])
    #     pygame.draw.polygon(overlay, pink_fill, pts)
    #     pygame.draw.polygon(overlay, AMBIGUOUS_COLOR, pts, width=2)

# === Инициализация Pygame и данные ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-type MS с розовой спорной")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
values = [3, 3, 3, 0]
weights = [0.2,0.2,0.2,0.2]
MULTI_TABLE = build_multitype_table_2()
pprint.pprint(MULTI_TABLE, width=80)

# === Основной цикл ===
running = True
case = sum(values[i]*(T**i) for i in range(4))
print(f"Текущий case: \n\t {case} (base-10) \n\t {to_base(case, 4)} (base-4)")


while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos
            for i, (px, py) in POINTS.items():
                bx, by = px+BUTTON_OFFSET, py-BUTTON_OFFSET
                if pygame.Rect(bx, by, BUTTON_SIZE, BUTTON_SIZE).collidepoint(mx, my):
                    nw = weights[i] + STEP
                    weights[i] = 0.1 if nw > 0.9 else round(nw, 1)
            for i, (px, py) in POINTS.items():
                if (mx-px)**2+(my-py)**2 <= POINT_RADIUS**2:
                    values[i] = (values[i]+1) % T
                    case = sum(values[i] * (T ** i) for i in range(4))
                    print(f"Новый case: \n\t {case} (base-10) \n\t {to_base(case, 4)} (base-4)")

    case = sum(values[i]*(T**i) for i in range(4))
    screen.fill(BG_COLOR)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_case(overlay, case, weights)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, CELL_BORDER_COLOR, (MARGIN_X, MARGIN_Y, CELL_SIZE, CELL_SIZE), 2)
    for i, (px, py) in POINTS.items():
        col = SURFACE_COLORS[values[i]]
        pygame.draw.circle(screen, col, (int(px), int(py)), POINT_RADIUS)
        bx, by = px+BUTTON_OFFSET, py-BUTTON_OFFSET
        pygame.draw.rect(screen, BUTTON_COLOR, (bx, by, BUTTON_SIZE, BUTTON_SIZE))
        txt = font.render(f"{weights[i]:.1f}|{values[i]}", True, BUTTON_TEXT_COLOR)
        screen.blit(txt, (bx+2, by+2))
    pygame.display.flip()
    clock.tick(1)
pygame.quit()
sys.exit()
