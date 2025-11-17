# ---------- ХЕШ-ФУНКЦИЯ ----------
def simple_hash(s, size):
    return sum(ord(c) for c in s) % size


# ---------- ХТ с наложением (открытая адресация) ----------
class HashTableOpen:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def resize(self):
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size

        for item in old_table:
            if item is not None:
                self.insert(item)

    def insert(self, key):
        index = simple_hash(key, self.size)
        start = index

        while self.table[index] is not None:
            if self.table[index] == key:
                return
            index = (index + 1) % self.size

            if index == start:
                self.resize()
                return self.insert(key)

        self.table[index] = key


# ---------- ХТ со списками (цепочки) ----------
class HashTableChains:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def insert(self, key):
        index = simple_hash(key, self.size)
        if key not in self.table[index]:
            self.table[index] += [key]


# ---------- ОСНОВНОЙ КОД ----------
def main():
    input_file = "inputText.txt"
    output_file = "resultText.txt"
    table_size = 10

    text = open(input_file, encoding="utf-8").read()
    words = [i.strip() for i in text.split()]

    ht_open = HashTableOpen(table_size)
    ht_chains = HashTableChains(table_size)

    for w in words:
        ht_open.insert(w)
        ht_chains.insert(w)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=== Хеш-таблица с наложением (open addressing) ===\n")
        for i, v in enumerate(ht_open.table):
            f.write(f"{i}: {v}\n")

        f.write("\n=== Хеш-таблица со списками (chaining) ===\n")
        for i, lst in enumerate(ht_chains.table):
            f.write(f"{i}: {lst}\n")


if __name__ == "__main__":
    main()