import os
import pygame
from itertools import product
from data import (T, WIDTH, HEIGHT, CELL_SIZE,
                  POINTS, INNER_POINTS, EDGES,
                  SURFACE_COLORS, AMBIGUOUS_COLOR,
                  OVERLAY_ALPHA)
from ms_multitype import interp, build_multitype_table_2, to_base
from old.t_256_v import draw_case

# 1) Headless setup
os.environ["SDL_VIDEODRIVER"] = "dummy"  # headless mode
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 2) Подготовка таблицы и конфигураций
MULTI_TABLE = build_multitype_table_2()
configs = list(product(range(T), repeat=4))  # 256 комбинаций

# 3) Генерация и сохранение
for vals in configs:
    # Вычисляем номер case
    case = sum(vals[i] * (T**i) for i in range(4))
    # Базовые веса (можно задать любые)
    weights = [0.5]*4

    # Рисуем
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_case(overlay, case, weights)
    screen.fill((0,0,0))  # или ваш BG_COLOR
    screen.blit(overlay, (0,0))

    # Сохраняем
    fname = f"screenshots/case_{to_base(case,4)}.png"
    os.makedirs("screenshots", exist_ok=True)
    pygame.image.save(screen, fname)  # сохраняем изображение

pygame.quit()
