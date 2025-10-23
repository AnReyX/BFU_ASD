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

def lab6(arr): # Посредством выбора
    n = len(arr)
    for i in range(n - 1):
        min = i
        for j in range(i + 1, n):
            if arr[j] < arr[min]:
                min = j
        arr[i], arr[min] = arr[min], arr[i]
    return arr # Средний результат: O(n^2)

def lab7(arr): # Шелла (Усовершенственная вставками)
    pass

def lab8(): # Поразрядная
    pass

def lab9(): # Пирамидальная (heap sort)
    pass

def lab10(): # Слиянием
    pass

def lab11(): # Быстрая (quick sort)
    pass

def lab12(): # Внешняя многофазная
    pass


arr = list(map(int, input("Введите последовательность чисел через пробел").split())) # 9 8 7 6 5 4 3 2 1 0 , 8 5 7 6 1 2 0 4 3 9
print(f"Отсортированный массив: {lab6(arr)}")