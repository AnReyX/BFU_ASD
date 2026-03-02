import itertools


def lab1():  # Метод Джарвиса
    def get_orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0
        if val > 0:
            return 1
        else:
            return 2


    def jarvis_algorithm(points):
        n = len(points)

        if n < 3:
            return "Невозможно построить выпуклую оболочку (нужно минимум 3 точки)"

        hull = []

        l = 0
        for i in range(1, n):
            if points[i][0] < points[l][0]:
                l = i

        p = l
        while True:
            hull.append(points[p])

            q = (p + 1) % n

            for i in range(n):
                if get_orientation(points[p], points[i], points[q]) == 2:
                    q = i

            p = q

            if p == l:
                break

        return hull


    try:
        n = int(input("Введите количество точек N: "))
        points = []
        print(f"Введите координаты {n} точек (x y через пробел):")

        for i in range(n):
            x, y = map(int, input(f"Точка {i + 1}: ").split())
            points.append((x, y))

        result = jarvis_algorithm(points)

        if isinstance(result, str):
            print(result)
        else:
            print("\nКоординаты точек выпуклой оболочки:")
            for p in result:
                print(p)
    except ValueError:
        print("Ошибка ввода. Пожалуйста, вводите целые числа.")


def lab2():
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def is_point_in_triangle(pt, v1, v2, v3):
        cp1 = cross_product(v1, v2, pt)

        cp2 = cross_product(v2, v3, pt)

        cp3 = cross_product(v3, v1, pt)


        has_neg = (cp1 < 0) or (cp2 < 0) or (cp3 < 0)
        has_pos = (cp1 > 0) or (cp2 > 0) or (cp3 > 0)

        return not (has_neg and has_pos)

    def solve_nested_triangles(points):
        n = len(points)
        if n < 6:
            pass

        tri_combinations = list(itertools.combinations(points, 3))

        print(f"Всего можно построить {len(tri_combinations)} треугольников.")

        for triangle_A in tri_combinations:
            for triangle_B in tri_combinations:

                if triangle_A == triangle_B:
                    continue

                is_nested = True
                for vertex in triangle_A:
                    if not is_point_in_triangle(vertex, triangle_B[0], triangle_B[1], triangle_B[2]):
                        is_nested = False
                        break

                if is_nested:
                    return triangle_A, triangle_B

        return None


    try:
        n = int(input("Введите количество точек N: "))
        points = []
        print(f"Введите координаты {n} точек (x y через пробел):")
        for i in range(n):
            x, y = map(int, input(f"Точка {i + 1}: ").split())
            points.append((x, y))

        result = solve_nested_triangles(points)

        if result:
            inner, outer = result
            print("\nНайдено вложение!")
            print(f"Внутренний треугольник: {inner}")
            print(f"Внешний треугольник: {outer}")
        else:
            print("\nВложенных треугольников не найдено.")

    except ValueError:
        print("Ошибка ввода чисел.")


# lab1()  # 7   0 3  2 2  1 1  2 1  3 0  0 0  3 3
lab2() # 7   0 0  10 0  0 10  2 2  3 2  2 3  20 20