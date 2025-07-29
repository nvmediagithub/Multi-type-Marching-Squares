import pprint
import pygame
import sys

from data import T, EDGES, POINTS
from data import MARGIN_X, MARGIN_Y
from data import WIDTH, HEIGHT, CELL_SIZE
from data import BUTTON_OFFSET, BUTTON_SIZE
from data import OVERLAY_ALPHA
from data import STEP
from data import SURFACE_COLORS, AMBIGUOUS_COLOR, BUTTON_TEXT_COLOR, BUTTON_COLOR, CELL_BORDER_COLOR, BG_COLOR
from data import POINT_RADIUS

from ms_multitype import interp, build_multitype_table, to_base


# === Функция рисования по triangle table ===
def draw_case(overlay, case, weights):
    # рисуем поверхности 0..T-1
    for t in range(T):
        base = SURFACE_COLORS[t]
        fill = (*base, OVERLAY_ALPHA)
        for tri in MULTI_TABLE[case][t]:
            pts = []
            for kind, idx in tri:
                if kind == 'p': pts.append(POINTS[idx])
                else:
                    a,b = EDGES[idx]
                    pts.append(interp(POINTS[a], POINTS[b], weights[a], weights[b]))
            pygame.draw.polygon(overlay, fill, pts)
            pygame.draw.polygon(overlay, base, pts, width=2)
    # рисуем спорную поверхность в розовый
    pink_fill = (*AMBIGUOUS_COLOR, OVERLAY_ALPHA)
    for tri in MULTI_TABLE[case]['aband']:
        pts = []
        for _, idx in tri:
            a, b = EDGES[idx]
            pts.append(interp(POINTS[a], POINTS[b], weights[a], weights[b]))
        pygame.draw.polygon(overlay, pink_fill, pts)
        pygame.draw.polygon(overlay, AMBIGUOUS_COLOR, pts, width=2)

# === Инициализация Pygame и данные ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-type MS с розовой спорной")
font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
values = [0, 1, 2, 3]
weights = [0.2,0.2,0.2,0.2]
MULTI_TABLE = build_multitype_table()
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
