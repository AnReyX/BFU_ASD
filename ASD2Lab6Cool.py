import random


class CyclicRabinKarp:
    def __init__(self):
        # Эмуляция 64-битного числа для Python (чтобы работали сдвиги как в C++)
        self.MASK = 0xFFFFFFFFFFFFFFFF
        self.BIT_WIDTH = 64

        # Генерация таблицы случайных чисел для каждого символа (ASCII 0-255)
        # Это "соль" нашего алгоритма, защищающая от коллизий
        random.seed(42)  # Фиксируем сид для воспроизводимости
        self.char_table = [random.getrandbits(64) for _ in range(256)]

    def _rol(self, val, shift):
        """Циклический сдвиг влево (Rotate Left)"""
        shift %= self.BIT_WIDTH
        return ((val << shift) & self.MASK) | (val >> (self.BIT_WIDTH - shift))

    def get_hash(self, string):
        """Вычисляет хэш для полной строки (или подстроки)"""
        h = 0
        l = len(string)
        for i, char in enumerate(string):
            # Формула: XOR ( rol(val, L - 1 - i) )
            # Это аналог полиномиального хэша, где степень заменена сдвигом
            char_val = self.char_table[ord(char)]
            rotated_val = self._rol(char_val, l - 1 - i)
            h ^= rotated_val
        return h

    def search(self, text, pattern):
        """
        Поиск всех вхождений pattern в text.
        Возвращает список индексов.
        """
        n = len(text)
        m = len(pattern)

        if m > n or m == 0:
            return []

        result_indices = []

        # 1. Вычисляем хэш паттерна
        pattern_hash = self.get_hash(pattern)

        # 2. Вычисляем хэш первого окна текста
        window_hash = self.get_hash(text[:m])

        # Предварительно вычисляем значение сдвига для выходящего символа
        # Чтобы не пересчитывать это внутри цикла
        # Нам нужно будет сдвигать выходящий символ ровно на M (длина паттерна)

        for i in range(n - m + 1):
            # Если хэши совпали, проверяем символьно (на случай коллизии)
            if pattern_hash == window_hash:
                if text[i: i + m] == pattern:
                    result_indices.append(i)

            # Если мы не в конце текста, сдвигаем окно (Rolling Hash)
            if i < n - m:
                old_char = text[i]
                new_char = text[i + m]

                # ШАГ 1: Сдвигаем текущий хэш влево на 1
                # Это поднимает "степень" всех текущих символов
                window_hash = self._rol(window_hash, 1)

                # ШАГ 2: Убираем старый символ.
                # Старый символ внутри хэша уже был бы сдвинут на M позиций после шага 1.
                # Поэтому мы берем его табличное значение, сдвигаем на M и делаем XOR.
                old_val_rotated = self._rol(self.char_table[ord(old_char)], m)
                window_hash ^= old_val_rotated

                # ШАГ 3: Добавляем новый символ (он просто заходит с позиции 0, сдвиг не нужен)
                window_hash ^= self.char_table[ord(new_char)]

        return result_indices


# --- Тестирование ---
if __name__ == "__main__":
    rk = CyclicRabinKarp()

    text_sample = "ABRACADABRA_TESTING_ALGORITHM_ABRA"
    pattern_sample = "ABRA"

    matches = rk.search(text_sample, pattern_sample)

    print(f"Текст: {text_sample}")
    print(f"Паттерн: {pattern_sample}")
    print(f"Найдены вхождения на индексах: {matches}")

    # Проверка корректности
    for idx in matches:
        assert text_sample[idx: idx + len(pattern_sample)] == pattern_sample
    print("Проверка пройдена успешно!")