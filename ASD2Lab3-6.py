#- - - Lab3 - Поиск с помощью конечного автомата - - -


def build_transition_table(pattern):
    m = len(pattern)
    alphabet = set(pattern)
    table = []

    for state in range(m + 1):
        table.append({})
        for char in alphabet:
            k = min(m, state + 1)
            while k > 0:
                if (pattern[:state] + char).endswith(pattern[:k]):
                    break
                k -= 1
            table[state][char] = k
    return table


def finite_automaton_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0: return []

    table = build_transition_table(pattern)
    occurrences = []

    state = 0  # Начальное состояние (0 символов совпало)

    for i in range(n):
        char = text[i]
        if char in table[state]:
            state = table[state][char]
        else:
            state = 0
            # Когда текущий символ мог бы начать паттерн заново
            if char in table[0]:
                state = table[0][char]

        if state == m: # Прошли паттерн
            occurrences.append(i - m + 1)

    return occurrences


# - - - Lab4 - Кнут-Моррис-Пратт - - -


def compute_prefix_function(pattern): # Префикс-функция
    m = len(pattern)
    pi = [0] * m
    k = 0  # длина предыдущего самого длинного префикса

    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi


def kmp_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0: return []

    pi = compute_prefix_function(pattern)
    occurrences = []

    q = 0

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            occurrences.append(i - m + 1)
            q = pi[q - 1]

    return occurrences


# - - - Lab5 - Бойер-Мур - - -


def build_bad_char_table(pattern):
    table = {}
    m = len(pattern)

    for i in range(m - 1):
        table[pattern[i]] = i
    return table


def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0: return []

    bad_char = build_bad_char_table(pattern)
    occurrences = []

    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            occurrences.append(s)

            if s + m < n:
                char_in_text = text[s + m]
                s += m - bad_char.get(char_in_text, -1)
            else:
                s += 1
        else:
            char_in_text = text[s + j]
            s += max(1, j - bad_char.get(char_in_text, -1))

    return occurrences


# - - - Lab6 - Рабин-Карп - - -

def rabin_karp_search(text, pattern):
    d = 256  # Количество символов в алфавите
    q = 101  # Простое число для модуля, против переполнения хэша
    m = len(pattern)
    n = len(text)
    occurrences = []

    if m == 0: return []

    p_hash = 0
    t_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i: i + m] == pattern:
                occurrences.append(i)

        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q

            if t_hash < 0:
                t_hash = t_hash + q

    return occurrences


text_input = "ABABDABACDABABCABAB"
pattern_input = "ABABCABAB"

print(f"Текст: {text_input}")
print(f"Паттерн: {pattern_input}\n")

print("3. Конечный автомат:", finite_automaton_search(text_input, pattern_input))
print("4. Кнут-Моррис-Пратт:", kmp_search(text_input, pattern_input))
print("5. Бойер-Мур:", boyer_moore_search(text_input, pattern_input))
print("6. Рабин-Карп:", rabin_karp_search(text_input, pattern_input))