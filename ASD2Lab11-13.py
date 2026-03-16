def lab11(): # Алгоритм Уэлша-Пауэлла
    def solve_graph_coloring(num_vertices, edges):
        # Пример: adjacency[0] = {1, 2} означает, что вершина 0 соединена с 1 и 2
        adjacency = {i: set() for i in range(num_vertices)}
        for u, v in edges:
            adjacency[u].add(v)
            adjacency[v].add(u)

        # Подсчёт степеней вершин, сортировка по кол-ву вершин по убыванию
        sorted_nodes = sorted(range(num_vertices),
                              key=lambda x: len(adjacency[x]),
                              reverse=True)

        # {номер_вершины: цвет}
        result_colors = {}

        for node in sorted_nodes:
            # Смотрим, какие цвета уже заняты соседями этой вершины
            neighbor_colors = set()
            for neighbor in adjacency[node]:
                if neighbor in result_colors:
                    neighbor_colors.add(result_colors[neighbor])

            # Ищем первый доступный цвет с 1, которого нет у соседей
            color = 1
            while color in neighbor_colors:
                color += 1

            result_colors[node] = color

        return result_colors


    try:
        n = int(input("Введите количество вершин: "))
        m = int(input("Введите количество ребер: "))
        edges = []
        print(f"Введите {m} ребер (u v через пробел):")

        for _ in range(m):
            u, v = map(int, input().split())
            edges.append((u, v))

        colors = solve_graph_coloring(n, edges)
        max_color = max(colors.values())
        print(f"Минимальное количество цветов: {max_color}")

        for i in range(n):
            print(f"Вершина {i} -> Цвет {colors[i]}")

    except ValueError:
        print("Ошибка ввода чисел.")


def lab12():
    def solve_knapsack(capacity, weights, values, n):
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(1, capacity + 1):

                current_weight = weights[i - 1]
                current_value = values[i - 1]

                if current_weight <= w:
                    # Если предмет влезает, выбираем лучшее:
                    # Не брать (значение сверху)
                    # Взять (цена + значение для оставшегося веса из пред. строки)
                    dp[i][w] = max(dp[i - 1][w],
                                   current_value + dp[i - 1][w - current_weight])
                else:
                    # Если не влезает - копируем значение сверху
                    dp[i][w] = dp[i - 1][w]

        max_value = dp[n][capacity]


        selected_items = []
        w = capacity

        for i in range(n, 0, -1):
            # Если значение отличается от того, что было строкой выше, значит, мы добавили этот предмет
            if dp[i][w] != dp[i - 1][w]:
                item_index = i - 1
                selected_items.append(item_index + 1)
                w -= weights[item_index]

        selected_items.reverse()

        return max_value, selected_items


    try:
        # Веса: [10, 20, 30]
        # Цены: [60, 100, 120]
        # Рюкзак: 50

        W = int(input("Введите вместимость рюкзака W: "))
        n = int(input("Введите количество предметов N: "))
        weights = []
        values = []
        print(f"Введите вес и стоимость {n} предметов (w v):")

        for i in range(n):
            w, v = map(int, input(f"Предмет {i + 1}: ").split())
            weights.append(w)
            values.append(v)

        max_val, items = solve_knapsack(W, weights, values, n)
        print(f"Максимальная стоимость: {max_val}")
        print(f"Номера взятых предметы: {items}")

    except ValueError:
        print("Ошибка ввода чисел.")


def lab13(): # Алгоритм First Fit Decreasing
    def solve_bin_packing(capacity, items):
        sorted_items = sorted(items, reverse=True)

        bins = [] # Вложенный список ящиков, ящики - списки предметов в них

        bin_rem_space = [] # Сколько места в каждом ящике есть

        for item in sorted_items:
            if item > capacity:
                print(f"Предмет размера {item} не влезает в ящик {capacity} и будет пропущен!")
                continue

            placed = False

            # Пробуем положить в уже в открытые ящики
            for i in range(len(bins)):
                if bin_rem_space[i] >= item:
                    bins[i].append(item)
                    bin_rem_space[i] -= item
                    placed = True
                    break

            # Иначе открываем новый ящик
            if not placed:
                bins.append([item])
                bin_rem_space.append(capacity - item)

        return bins


    try:
        C = int(input("Введите вместимость одного ящика (C): "))
        input_str = input("Введите размеры предметов через пробел: ")
        items = list(map(int, input_str.split()))

        result_bins = solve_bin_packing(C, items)
        print(f"\nВсего использовано ящиков: {len(result_bins)}")
        for i, b in enumerate(result_bins):
            filled = sum(b)
            print(f"Ящик {i + 1}: {b} (Занято: {filled}/{C}, Свободно: {C - filled})")
    except ValueError:
        print("Ошибка ввода чисел.")



# lab11() # 5   5   0 1  0 2  1 2  1 3  2 4
# lab12() # 49  3   10 60  20 100  30 120
lab13() # 10  2 5 4 7 1 3 8