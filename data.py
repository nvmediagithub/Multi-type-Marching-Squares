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
# Рёбра: (индекс вершины a, индекс вершины b)
EDGES = {
    0: (0, 1),  # верх
    1: (1, 2),  # право
    2: (2, 3),  # низ
    3: (3, 0),  # лево
}

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