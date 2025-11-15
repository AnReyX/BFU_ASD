import heapq

def lab4(arr): # Сортировка методом прочёсывания (Усовершенственная пузырьковая)
    n = len(arr)
    gap_fact = n / 1.247
    while gap_fact > 1:
        gap = round(gap_fact)
        i = 0
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
            i += 1
        gap_fact /= 1.247
    return arr # Лучший результат: O(nlog(n)), Худший: O(n^2)

def lab5(arr): # Вставками
    n = len(arr)
    for i in range(1, n):
        j = i - 1
        while j >= 0 and arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            j -= 1
    return arr # Лучший результат: O(n), Средний и худший: O(n^2)

def lab6(arr): # Посредством выбора - СДЕЛАНО
    n = len(arr)
    for i in range(n - 1):
        minimum = i
        for j in range(i + 1, n):
            if arr[j] < arr[minimum]:
                minimum = j
        arr[i], arr[minimum] = arr[minimum], arr[i]
    return arr # Средний результат: O(n^2)

def lab7(arr): # Шелла (Усовершенственная вставками)
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr # Лучший результат: O(nlog(n)), Средний - O(n^(3/2)), Худший - O(n^2)

def lab8(arr): # Поразрядная (Radix sort)
    max_len = max([len(str(x)) for x in arr])
    base = 10
    bins = [[] for _ in range(base)]
    for i in range(0, max_len):
        print('Номер разряда: ' + str(i))
        for x in arr:
            digit = (x // base ** i) % base
            bins[digit] += [x]
        arr = [x for queue in bins for x in queue]
        print(arr)
        print(bins)
        bins = [[] for _ in range(base)]
    return arr # Время: O(n * k), k - наибольшее число разрядов, Память: O(n + b), b - основание системы счисления

def lab9(arr): # Пирамидальная (heap sort)
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0)
    return arr # Время: O(n/2 * log_2(n))

def lab10(array): # Слиянием (Merge sort)
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result += [left[i]]
                i += 1
            else:
                result += [right[j]]
                j += 1
        result += left[i:]
        result += right[j:]
        return result

    return merge_sort(array) # Время всегда постоянно: O(nlog(n))

def lab11(array): # Быстрая (quick sort)
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        piv = arr[len(arr) // 2]
        lef = [x for x in arr if x < piv]
        mid = [x for x in arr if x == piv]
        rig = [x for x in arr if x > piv]
        return quick_sort(lef) + mid + quick_sort(rig)

    return quick_sort(array) # Лучший, средний: O(nlog(n)), Худший: O(n^2)

# lab 12 - Внешняя многофазная
def create_runs(input_file, chunk_size=100000):
    runs = []
    with open(input_file, "r") as f:
        chunk = []
        for line in f:
            chunk.append(int(line.strip()))
            if len(chunk) >= chunk_size:
                chunk.sort()
                run_name = f"run_{len(runs)}.txt"
                with open(run_name, "w") as r:
                    r.write("\n".join(map(str, chunk)))
                runs.append(run_name)
                chunk = []
        if chunk:
            chunk.sort()
            run_name = f"run_{len(runs)}.txt"
            with open(run_name, "w") as r:
                r.write("\n".join(map(str, chunk)))
            runs.append(run_name)
    return runs

def merge_runs(run_files, output_file="sorted.txt"):
    files = [open(r) for r in run_files]
    heap = []
    for i, f in enumerate(files):
        line = f.readline()
        if line:
            heapq.heappush(heap, (int(line), i))
    with open(output_file, "w") as out:
        while heap:
            value, idx = heapq.heappop(heap)
            out.write(str(value) + "\n")
            next_line = files[idx].readline()
            if next_line:
                heapq.heappush(heap, (int(next_line), idx))
    for f in files:
        f.close()


# 9 8 7 6 5 4 3 2 1 0 , 8 5 7 6 1 2 0 4 3 9 , 15 73 1 42 159 7623
# arr = list(map(int, input("Введите последовательность чисел через пробел").split()))
# print(f"Отсортированный массив: {lab10(arr)}")

# Пример внешней многофазной сортировки
runs = create_runs("input.txt", chunk_size=5)
print(runs)
merge_runs(runs, "sorted.txt")