import pygame
from numpy import pi, sin, cos, square, sqrt

# Переменные для окон и точки крепления
FPS = 60
width = 600
height = 600
GUI_W = 300
offset = (int(width/2), int(height/2))

# Инициация и настройка Pygame
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((width + GUI_W, height))
pygame.display.set_caption('Маятник')
font = pygame.font.SysFont('arial', 20)
# Области отрисовки маятников и линии
screen = pygame.Surface((width, height))
trace = pygame.Surface((width, height))
GUI_screen = pygame.Surface((GUI_W, height))
# Цвета интерфейса
RED = (230, 0, 0)
T_RED = (150, 0, 0)
GREY = (230, 230, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLOR_KEY = (0, 0, 1)
BALL_COLOR = RED

trace.set_colorkey(COLOR_KEY)
trace.fill(COLOR_KEY)

# Глобальные переменные
g = 1
r1 = 100
r2 = 120
m1 = 10
m2 = 20
a1 = pi/2
a2 = pi/2
a1_v = 0
a2_v = 0
# Переменные предыдущего положения для отрисовки линии
px2 = 0
py2 = 0
# Условие для проспуска отрисовки линии на первом кадре
first_frame = True

# Переменные интерфейса
GUI_P1_TOP = [width + (GUI_W * 1 // 3), height // 5]
GUI_P2_TOP = [width + (GUI_W * 2 // 3), height // 5]
GUI_P1_BOT = [width + (GUI_W * 1 // 3), height // 5 + r1]
GUI_P2_BOT = [width + (GUI_W * 2 // 3), height // 5 + r2]
p1_clicked = False
p2_clicked = False
mx, my = 0, 0
p_mx = mx
p_my = my
p_m1 = m1
p_m2 = m2
pp1_b = 0
pp2_b = 0


# Функция отображения текста
def msg(text, color, pos):
    screen_text = font.render(text, True, color)
    window.blit(screen_text, pos)


# Функция нахождения расстояния между точками
def dist(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


# Главный цикл
run = True
while run:
    # Инициация областей отрисовки
    window.blit(screen, (0, 0))
    window.blit(trace, (0, 0))
    window.blit(GUI_screen, (width, 0))
    screen.fill(WHITE)
    GUI_screen.fill(GREY)

    # Обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Проверка нажатия
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Фиксирование предыдущих значений
            p_mx = mx
            p_my = my
            p_m1 = m1
            p_m2 = m2
            pp1_b = GUI_P1_BOT[1]
            pp2_b = GUI_P2_BOT[1]
            # Проверка положения курсора
            if dist(GUI_P1_BOT[0], GUI_P1_BOT[1], mx, my) < m1:
                p1_clicked = True
            if dist(GUI_P2_BOT[0], GUI_P2_BOT[1], mx, my) < m2:
                p2_clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            p1_clicked = False
            p2_clicked = False
            BALL_COLOR = RED

    # Вычисления при нажатии
    if p1_clicked:
        if my > GUI_P1_TOP[1]:
            GUI_P1_BOT[1] = pp1_b + my - p_my
            r1 = abs(GUI_P1_BOT[1] - GUI_P1_TOP[1])
        if p_m1 + mx - p_mx > 0:
            m1 = p_m1 + mx - p_mx
    if p2_clicked:
        if my > GUI_P2_TOP[1]:
            GUI_P2_BOT[1] = pp2_b + my - p_my
            r2 = abs(GUI_P2_BOT[1] - GUI_P2_TOP[1])
        if p_m2 + mx - p_mx > 0:
            m2 = p_m2 + mx - p_mx

    # Главные уравнения ускорения
    num1 = -g * (2 * m1 + m2) * sin(a1)
    num2 = -m2 * g * sin(a1 - 2 * a2)
    num3 = -2 * sin(a1 - a2) * m2
    num4 = square(a2_v) * r2 + square(a1_v) * r1 * cos(a1 - a2)
    den = r1 * (2 * m1 + m2 - m2 * cos(2 * a1 - 2 * a2))

    a1_a = (num1 + num2 + num3 * num4) / den

    num1 = 2 * sin(a1-a2)
    num2 = square(a1_v)*r1*(m1+m2)
    num3 = g * (m1 + m2) * cos(a1)
    num4 = square(a2_v) * r2 * m2 * cos(a1-a2)
    den = r2 * (2 * m1 + m2 - m2 * cos(2 * a1 - 2 * a2))

    a2_a = (num1 * (num2 + num3 + num4)) / den

    # Координаты маятников в зависимости от угла
    x1 = r1 * sin(a1)
    y1 = r1 * cos(a1)

    x2 = x1 + r2 * sin(a2)
    y2 = y1 + r2 * cos(a2)

    # Зависимость углов от скорости и ускорения
    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    # Коэффициент затухания
    # a1_v *= 0.999
    # a2_v *= 0.999

    # Отрисовка элементов настройки
    pygame.draw.line(window, BLACK, GUI_P1_TOP, GUI_P1_BOT, 2)
    pygame.draw.line(window, BLACK, GUI_P2_TOP, GUI_P2_BOT, 2)
    pygame.draw.circle(window, BALL_COLOR, GUI_P1_BOT, m1)
    pygame.draw.circle(window, BALL_COLOR, GUI_P2_BOT, m2)
    # Отрисовка маятников
    pygame.draw.line(screen, BLACK, (offset[0] + int(x1), offset[1] + int(y1)), offset, 2)
    pygame.draw.line(screen, BLACK, (offset[0] + int(x2), offset[1] + int(y2)), (offset[0] + int(x1), offset[1] + int(y1)), 2)
    pygame.draw.circle(screen, BALL_COLOR, (offset[0] + int(x1), offset[1] + int(y1)), m1)
    pygame.draw.circle(screen, BALL_COLOR, (offset[0] + int(x2), offset[1] + int(y2)), m2)

    # Отрисовка пути линией
    if not first_frame:
        pygame.draw.line(trace, BALL_COLOR, (offset[0] + int(x2), offset[1] + int(y2)),
                         (offset[0] + int(px2), offset[1] + int(py2)), 1)
    # Отрисовка пути точками
    # pygame.draw.line(dots, (255, 0, 0), (offset[0] + int(x2), offset[1] + int(y2)), 1)

    px2 = x2
    py2 = y2
    first_frame = False
    # Отрисовка текста
    msg(str(r1), BLACK, [width + (GUI_W * 1 // 3) - 10, height // 20 + 5])
    msg(str(m1), T_RED, [width + (GUI_W * 1 // 3) - 10, height // 10 + 5])
    msg(str(r2), BLACK, [width + (GUI_W * 2 // 3) - 8, height // 20 + 5])
    msg(str(m2), T_RED, [width + (GUI_W * 2 // 3) - 8, height // 10 + 5])

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
