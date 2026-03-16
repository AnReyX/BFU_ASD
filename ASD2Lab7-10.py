def lab7():
    def find_max_subarray(arr):
        n = len(arr)
        if n == 0: return 0, []

        max_so_far = arr[0]
        current_max = arr[0]

        # Итоговые индексы для ответа
        start_index = 0
        end_index = 0
        temp_start_index = 0

        for i in range(1, n):
            if arr[i] > current_max + arr[i]:
                current_max = arr[i]
                temp_start_index = i
            else:
                current_max += arr[i]

            if current_max > max_so_far:
                max_so_far = current_max
                start_index = temp_start_index
                end_index = i

        return max_so_far, arr[start_index: end_index + 1]


    try:
        input_str = input("Введите элементы массива через пробел: ")
        arr = list(map(int, input_str.split()))

        max_sum, subarray = find_max_subarray(arr)

        print(f"- - -\nИсходный массив: {arr}")
        print(f"Максимальная сумма: {max_sum}")
        print(f"Подмассив: {subarray}")

    except ValueError:
        print("Ошибка ввода. Введите целые числа через пробел.")


def lab8():
    def count_change_ways(coins, amount):
        dp = [0] * (amount + 1)

        dp[0] = 1 # Базовый случай для 0 (не брать монеты)

        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]

        return dp[amount]



    try:
        s = int(input("Введите сумму S: "))
        input_coins = input("Введите номиналы монет через пробел: ")
        coins = list(map(int, input_coins.split()))

        ways = count_change_ways(coins, s)

        print(f"Количество способов набрать сумму {s}: {ways}")

    except ValueError:
        print("Ошибка ввода. Используйте целые числа.")


def lab9():
    def solve_tsp(n, start_node, dist_matrix):
        VISITED_ALL = (1 << n) - 1

        dp = [[float('inf')] * n for _ in range(1 << n)]

        # Для восстановления пути запоминаем предков
        parent = [[-1] * n for _ in range(1 << n)]

        # Базовый случай: мы находимся в стартовом городе, посетили только его. Стоимость 0.
        dp[1 << start_node][start_node] = 0

        for mask in range(1, 1 << n): # Состояния посещенных городов
            for u in range(n): # Город, в который мы могли прийти последним
                if (mask & (1 << u)): # Есть ли бит города в маске
                    prev_mask = mask ^ (1 << u)

                    if prev_mask == 0:
                        continue

                    for v in range(n):
                        if (prev_mask & (1 << v)):
                            new_cost = dp[prev_mask][v] + dist_matrix[v][u]
                            if new_cost < dp[mask][u]:
                                dp[mask][u] = new_cost
                                parent[mask][u] = v

        # Посетили все города, находимся в городе i, возвращаемся в начальный город start_node
        min_path = float('inf')
        last_city_before_home = -1

        for i in range(n):
            if i != start_node:
                current_path_cost = dp[VISITED_ALL][i] + dist_matrix[i][start_node]
                if current_path_cost < min_path:
                    min_path = current_path_cost
                    last_city_before_home = i

        if min_path == float('inf'):
            return None, []  # граф несвязный

        # Восстановление пути (Backtracking)
        path = []
        curr_mask = VISITED_ALL
        curr_city = last_city_before_home

        while curr_city != -1:
            path.append(curr_city)
            new_mask = curr_mask ^ (1 << curr_city)
            curr_city = parent[curr_mask][curr_city]
            curr_mask = new_mask

        path = path[::-1]
        path.append(start_node)

        return min_path, path


    #   0  1  2  3
    # 0 0 10 15 20
    # 1 10 0 35 25
    # 2 15 35 0 30
    # 3 20 25 30 0
    inf = float('inf')
    # Матрица смежности
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    n = 4
    start = 0  # Начинаем с 0-го города
    cost, path = solve_tsp(n, start, dist_matrix)
    print(f"Минимальная стоимость: {cost}")
    print(f"Путь: {' -> '.join(map(str, path))}")



def lab10():
    def solve_egg_drop(n_eggs, n_floors):
        dp = [[0] * (n_floors + 1) for _ in range(n_eggs + 1)]


        # Если этажей 1, нужен 1 бросок. Если этажей 0, нужно 0 бросков.
        for i in range(1, n_eggs + 1):
            dp[i][1] = 1
            dp[i][0] = 0

        # Если яйцо 1, проверяем все этажи снизу вверх (худший случай j)
        for j in range(1, n_floors + 1):
            dp[1][j] = j


        for i in range(2, n_eggs + 1):
            for j in range(2, n_floors + 1):

                dp[i][j] = float('inf')

                # x - этаж, с которого мы пробуем бросить яйцо первый раз
                for x in range(1, j + 1):

                    # Исход 1: Разбилось
                    broken = dp[i - 1][x - 1]

                    # Исход 2: Не разбилось
                    not_broken = dp[i][j - x]

                    # max для гарантированного результата
                    worst_case = 1 + max(broken, not_broken)

                    # х выберем для минимального худшего результата
                    if worst_case < dp[i][j]:
                        dp[i][j] = worst_case

        return dp[n_eggs][n_floors]


    try:
        # По условию:
        eggs = 2 # int(input("Яиц: "))
        floors = 100 # int(input("Этажей: "))
        result = solve_egg_drop(eggs, floors)
        print(f"Для количества яиц {eggs} и {floors}-этажного дома минимальное количество бросков: {result}")
    except ValueError:
        print("Ошибка ввода")


# lab7() # -2 1 -3 4 -1 2 1 -5 4
# lab8() # 5  1 2 5
# lab9()
lab10()