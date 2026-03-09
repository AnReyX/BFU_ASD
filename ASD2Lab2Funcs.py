import math
from itertools import combinations

EPS = 1e-9  # погрешность для сравнения float


# ============ АЛГОРИТМЫ ПЕРЕСЕЧЕНИЙ ============

def line_from_points(p1, p2):
    """
    Прямая по двум точкам в виде ax + by + c = 0
    Возвращает (a, b, c)
    """
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = -a * p1[0] - b * p1[1]
    return (a, b, c)


def lines_intersection(line1, line2):
    """
    Пересечение двух прямых
    line = (a, b, c) где ax + by + c = 0
    Возвращает точку или None если параллельны
    """
    a1, b1, c1 = line1
    a2, b2, c2 = line2

    det = a1 * b2 - a2 * b1

    if abs(det) < EPS:
        return None  # параллельны или совпадают

    x = (b1 * c2 - b2 * c1) / det
    y = (a2 * c1 - a1 * c2) / det

    return (x, y)


def point_on_segment(p, seg_start, seg_end):
    """проверка что точка лежит на отрезке"""
    # сначала проверим коллинеарность
    cross = (p[0] - seg_start[0]) * (seg_end[1] - seg_start[1]) - \
            (p[1] - seg_start[1]) * (seg_end[0] - seg_start[0])

    if abs(cross) > EPS:
        return False

    # теперь проверим что точка между концами
    min_x = min(seg_start[0], seg_end[0]) - EPS
    max_x = max(seg_start[0], seg_end[0]) + EPS
    min_y = min(seg_start[1], seg_end[1]) - EPS
    max_y = max(seg_start[1], seg_end[1]) + EPS

    return min_x <= p[0] <= max_x and min_y <= p[1] <= max_y


def line_segment_intersection(line, seg_start, seg_end):
    """
    Пересечение прямой и отрезка
    """
    seg_line = line_from_points(seg_start, seg_end)
    intersection = lines_intersection(line, seg_line)

    if intersection is None:
        return None

    if point_on_segment(intersection, seg_start, seg_end):
        return intersection

    return None


def segments_intersection(seg1_start, seg1_end, seg2_start, seg2_end):
    """
    Пересечение двух отрезков
    """
    line1 = line_from_points(seg1_start, seg1_end)
    line2 = line_from_points(seg2_start, seg2_end)

    intersection = lines_intersection(line1, line2)

    if intersection is None:
        return None

    # проверяем что точка лежит на обоих отрезках
    if point_on_segment(intersection, seg1_start, seg1_end) and \
            point_on_segment(intersection, seg2_start, seg2_end):
        return intersection

    return None


def line_circle_intersection(line, center, radius):
    """
    Пересечение прямой и окружности
    Возвращает список точек (0, 1 или 2)
    """
    a, b, c = line
    x0, y0 = center
    r = radius

    # расстояние от центра до прямой
    dist = abs(a * x0 + b * y0 + c) / math.sqrt(a * a + b * b)

    if dist > r + EPS:
        return []  # не пересекаются

    # находим проекцию центра на прямую
    # это ближайшая точка на прямой
    t = -(a * x0 + b * y0 + c) / (a * a + b * b)
    px = x0 + a * t
    py = y0 + b * t

    if abs(dist - r) < EPS:
        return [(px, py)]  # касание

    # два пересечения
    # находим смещение вдоль прямой
    d = math.sqrt(r * r - dist * dist)

    # единичный вектор вдоль прямой
    length = math.sqrt(a * a + b * b)
    dx = -b / length
    dy = a / length

    p1 = (px + dx * d, py + dy * d)
    p2 = (px - dx * d, py - dy * d)

    return [p1, p2]


def segment_circle_intersection(seg_start, seg_end, center, radius):
    """
    Пересечение отрезка и окружности
    """
    line = line_from_points(seg_start, seg_end)
    points = line_circle_intersection(line, center, radius)

    result = []
    for p in points:
        if point_on_segment(p, seg_start, seg_end):
            result.append(p)

    return result


def circles_intersection(c1, r1, c2, r2):
    """
    Пересечение двух окружностей
    c1, c2 - центры, r1, r2 - радиусы
    """
    x1, y1 = c1
    x2, y2 = c2

    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # проверки
    if d > r1 + r2 + EPS:
        return []  # слишком далеко

    if d < abs(r1 - r2) - EPS:
        return []  # одна внутри другой

    if d < EPS and abs(r1 - r2) < EPS:
        return None  # совпадают (бесконечно много точек)

    # формулы из википедии честно говоря
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)

    if r1 * r1 - a * a < 0:
        return []

    h = math.sqrt(max(0, r1 * r1 - a * a))

    # точка на линии между центрами
    px = x1 + a * (x2 - x1) / d
    py = y1 + a * (y2 - y1) / d

    if h < EPS:
        return [(px, py)]  # касание

    # две точки
    p1 = (px + h * (y2 - y1) / d, py - h * (x2 - x1) / d)
    p2 = (px - h * (y2 - y1) / d, py + h * (x2 - x1) / d)

    return [p1, p2]


# ============ РАБОТА С ТРЕУГОЛЬНИКАМИ ============

def sign(x):
    if x > EPS:
        return 1
    elif x < -EPS:
        return -1
    return 0


def point_in_triangle(p, t1, t2, t3):
    """
    Проверка что точка внутри треугольника (не на границе!)
    Используем знаки векторных произведений
    """

    def area_sign(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    s1 = sign(area_sign(p, t1, t2))
    s2 = sign(area_sign(p, t2, t3))
    s3 = sign(area_sign(p, t3, t1))

    # если все знаки одинаковые и не ноль - точка строго внутри
    if s1 == s2 == s3 and s1 != 0:
        return True

    return False


def triangle_inside_triangle(inner, outer):
    """
    Проверка что треугольник inner полностью внутри outer
    """
    # все вершины inner должны быть внутри outer
    for p in inner:
        if not point_in_triangle(p, outer[0], outer[1], outer[2]):
            return False

    # проверяем что стороны не пересекаются
    inner_edges = [(inner[0], inner[1]), (inner[1], inner[2]), (inner[2], inner[0])]
    outer_edges = [(outer[0], outer[1]), (outer[1], outer[2]), (outer[2], outer[0])]

    for ie in inner_edges:
        for oe in outer_edges:
            if segments_intersection(ie[0], ie[1], oe[0], oe[1]) is not None:
                return False

    return True


def find_nested_triangles(points):
    """
    Ищем пары вложенных треугольников среди точек
    """
    if len(points) < 6:
        return None

    # генерируем все возможные треугольники
    triangles = []
    for combo in combinations(range(len(points)), 3):
        t = (points[combo[0]], points[combo[1]], points[combo[2]])
        # проверяем что это не вырожденный треугольник
        area = abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[2][0] - t[0][0]) * (t[1][1] - t[0][1]))
        if area > EPS:
            triangles.append(t)

    # ищем вложенные пары
    for i, t1 in enumerate(triangles):
        for j, t2 in enumerate(triangles):
            if i == j:
                continue

            # проверяем что у них нет общих вершин
            common = set(t1) & set(t2)
            if len(common) > 0:
                continue

            if triangle_inside_triangle(t1, t2):
                return (t2, t1)  # внешний, внутренний

    return None


def main():
    print("=" * 50)
    print("ПОИСК ВЛОЖЕННЫХ ТРЕУГОЛЬНИКОВ")
    print("=" * 50)

    test = input("Использовать тестовые данные? (y/n): ")

    if test.lower() == 'y':
        # точки для теста - должны образовывать вложенные треугольники
        points = [
            (0, 0), (10, 0), (5, 10),  # внешний большой
            (4, 2), (6, 2), (5, 5),  # внутренний маленький
            (20, 20)  # лишняя точка
        ]
        print("Тестовые точки:", points)
    else:
        n = int(input("Количество точек: "))
        points = []
        for i in range(n):
            x, y = map(float, input(f"Точка {i + 1} (x y): ").split())
            points.append((x, y))

    print(f"\nВсего точек: {len(points)}")

    result = find_nested_triangles(points)

    if result is None:
        print("\nВложенных треугольников НЕ НАЙДЕНО")
    else:
        outer, inner = result
        print("\nНАЙДЕНЫ вложенные треугольники!")
        print(f"Внешний: {outer}")
        print(f"Внутренний: {inner}")

    # демо алгоритмов пересечений
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМОВ ПЕРЕСЕЧЕНИЙ")
    print("=" * 50)

    # прямые
    l1 = (1, -1, 0)  # y = x
    l2 = (1, 1, -2)  # x + y = 2
    print(f"\nПересечение прямых y=x и x+y=2: {lines_intersection(l1, l2)}")

    # отрезки
    print(
        f"Пересечение отрезков [(0,0)-(2,2)] и [(0,2)-(2,0)]: {segments_intersection((0, 0), (2, 2), (0, 2), (2, 0))}")

    # окружности
    print(f"Пересечение окружностей (0,0)r=2 и (3,0)r=2: {circles_intersection((0, 0), 2, (3, 0), 2)}")


if __name__ == "__main__":
    main()
