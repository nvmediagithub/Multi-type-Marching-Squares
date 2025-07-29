# === Конфигурация экрана ===
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 200
MARGIN_X = (WIDTH - CELL_SIZE) // 2
MARGIN_Y = (HEIGHT - CELL_SIZE) // 2
POINT_RADIUS = 10
BUTTON_SIZE = 20
BUTTON_OFFSET = 15
STEP = 0.2
OVERLAY_ALPHA = 120  # прозрачность для заливки треугольников

# === Конфигурация многотиповой таблицы ===
T = 4  # число состояний в каждой точке

# Вершины квадрата
POINTS = {
    0: (MARGIN_X,               MARGIN_Y),
    1: (MARGIN_X + CELL_SIZE,   MARGIN_Y),
    2: (MARGIN_X + CELL_SIZE,   MARGIN_Y + CELL_SIZE),
    3: (MARGIN_X,               MARGIN_Y + CELL_SIZE),
}
# # Вершины внутреннего ромба
# INNER_POINTS = {
#     0: (MARGIN_X + CELL_SIZE / 2, MARGIN_Y),
#     1: (MARGIN_X + CELL_SIZE, MARGIN_Y + CELL_SIZE / 2),
#     2: (MARGIN_X + CELL_SIZE / 2, MARGIN_Y + CELL_SIZE),
#     3: (MARGIN_X, MARGIN_Y + CELL_SIZE / 2),
#     4: (MARGIN_X + CELL_SIZE / 2, MARGIN_Y + CELL_SIZE / 2), # Центр
# }
# Вершины внутреннего квадрата
INNER_POINTS = {
    0: (MARGIN_X + CELL_SIZE / 4, MARGIN_Y + CELL_SIZE / 4),
    1: (MARGIN_X + CELL_SIZE * 3 / 4, MARGIN_Y + CELL_SIZE / 4),
    2: (MARGIN_X + CELL_SIZE * 3 / 4, MARGIN_Y + CELL_SIZE * 3 / 4),
    3: (MARGIN_X + CELL_SIZE / 4, MARGIN_Y + CELL_SIZE * 3 / 4),
}

# Рёбра: (индекс вершины a, индекс вершины b)
EDGES = {
    0: (0, 1),  # верх
    1: (1, 2),  # право
    2: (2, 3),  # низ
    3: (3, 0),  # лево
}
# Точки между граней
IP_ADJ = {
    0: (0, 2), # Между верхней и нижней
    1: (1, 3),
    2: (2, 0),
    3: (3, 1),
}
# # Соседние внутренние точки для каждого ребра
# IP_ADJ = {
#     0: (0, 4),
#     1: (1, 4),
#     2: (2, 4),
#     3: (4, 3),
# }
# # Соседние внутренние точки для каждого ребра
# IP_ADJ = {
#     0: (0, 1),  # ребро 0 (верх) => внутренние точки 0 и 1
#     1: (1, 2),  # ребро 1 (право) => 1,2
#     2: (2, 3),  # ребро 2 (низ)  => 2,3
#     3: (3, 0),  # ребро 3 (лево) => 3,0
# }

# === Цвета для 4 состояний точек ===
SURFACE_COLORS = {
    0: (200, 0, 0),   # красный
    1: (0, 200, 0),   # зелёный
    2: (0, 0, 200),   # синий
    3: (200, 200, 0),   # жёлтый
}
# Цвет для спорной (aband) поверхности
AMBIGUOUS_COLOR = (255, 105, 180)  # розовый

BUTTON_COLOR = (50,  50,  50)
BUTTON_TEXT_COLOR = (255, 255, 255)
CELL_BORDER_COLOR = (200, 200, 200)
BG_COLOR = (30,  30,  30)