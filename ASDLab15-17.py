class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def parse_tree(s):
    s = s.strip()  # Убираем лишние пробелы по краям

    # Базовый случай: пустая строка означает отсутствие узла (NULL)
    if not s:
        return None

    # 1. Ищем первую скобку, чтобы отделить значение корня от потомков
    first_par = s.find('(')

    # Если скобок нет, значит это лист (например, просто "1")
    if first_par == -1:
        return Node(int(s))

    # 2. Извлекаем значение корня (все, что до первой скобки)
    root_value = int(s[:first_par])
    node = Node(root_value)

    # 3. Работаем с содержимым внутри скобок: (ЛЕВОЕ, ПРАВОЕ)
    # Берем срез без первой '(' и последней ')'
    inner = s[first_par + 1: -1]

    # Нам нужно найти ЗАПЯТУЮ, которая разделяет левое и правое поддерево.
    # Важно: это должна быть запятая "верхнего уровня", не вложенная в другие скобки.
    par = 0
    comma_index = -1

    for i in range(len(inner)):
        if inner[i] == '(':
            par += 1
        elif inner[i] == ')':
            par -= 1
        elif inner[i] == ',' and par == 0:
            comma_index = i
            break

    # Запятая есть - рекурсивно парсим левую и правую части
    if comma_index != -1:
        left_str = inner[:comma_index]
        right_str = inner[comma_index + 1:]

        node.left = parse_tree(left_str)
        node.right = parse_tree(right_str)
    else:
        # Запятой нет - передаём всю строку, как левого потомка (проверка на дурака)
        node.left = parse_tree(inner)

    return node


# - - - Lab 15 - - -


def pre_order(node):
    # Прямой обход: Корень -> Левое -> Правое
    if node:
        print(node.value, end=" ")
        pre_order(node.left)
        pre_order(node.right)


def in_order(node):
    # Центральный (симметричный) обход: Левое -> Корень -> Правое
    if node:
        in_order(node.left)
        print(node.value, end=" ")
        in_order(node.right)


def post_order(node):
    # Концевой (обратный) обход: Левое -> Правое -> Корень
    if node:
        post_order(node.left)
        post_order(node.right)
        print(node.value, end=" ")

'''
if __name__ == "__main__":
    input_str = "1 (2 ( , 4 (7, 8)), 3 (5 ( , 9 (11, )), 6 (10, )))" # 8 (3 (1, 6 (4,7)), 10 ( , 14(13,)))
    print(f"Входная строка: {input_str}")

    root = parse_tree(input_str)

    print("\nПрямой обход:")
    pre_order(root)
    print()

    print("\nЦентральный обход:")
    in_order(root)
    print()

    print("\nКонцевой обход:")
    post_order(root)
    print()
'''


# - - - Lab 16 - - -

def iterative_pre_order(root):
    if root is None:
        return ""

    result_list = []

    # В Python обычный список (list) отлично работает как стек
    # методы: append() - положить, pop() - достать последний
    stack = []

    # 1. Кладем корень в стек
    stack.append(root)

    while len(stack) > 0:
        # 2. Достаем узел с вершины
        node = stack.pop()

        # 3. Обрабатываем узел (добавляем в результат)
        result_list.append(str(node.value))

        # 4. Кладем детей в стек.
        # ВАЖНО: Порядок обратный. Сначала Right, потом Left.
        # Тогда Left окажется на вершине стека и будет обработан следующим.

        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    # Формируем итоговую строку
    return " ".join(result_list)

'''
if __name__ == "__main__":
    input_str = "1 (2 ( , 4 (7, 8)), 3 (5 ( , 9 (11, )), 6 (10, )))" # 8 (3 (1, 6 (4,7)), 10 ( , 14(13,)))
    print(f"Входная строка: {input_str}")

    root = parse_tree(input_str)

    print("\nПрямой не рекурсивный обход:")
    print(iterative_pre_order(root))
'''


# - - - Lab 17 - - -

# --- Вывод дерева обратно в строку ---
def tree_to_str(node):
    """Преобразует дерево обратно в линейно-скобочную запись"""
    if not node:
        return ""

    # Если лист
    if not node.left and not node.right:
        return str(node.value)

    left_s = tree_to_str(node.left)
    right_s = tree_to_str(node.right)

    # Форматирование: Вал (Лев, Прав)
    # Если какой-то ветки нет, оставляем пустоту
    return f"{node.value} ({left_s}, {right_s})"


def search_bst(node, key):
    if node is None:
        return None  # Не нашли
    if key == node.value:
        return node  # Нашли

    if key < node.value:
        return search_bst(node.left, key)
    else:
        return search_bst(node.right, key)


def insert_bst(node, key):
    if node is None:
        return Node(key)

    if key < node.value:
        node.left = insert_bst(node.left, key)
    elif key > node.value:
        node.right = insert_bst(node.right, key)
    else:
        print("  [!] Элемент уже существует в дереве.")

    return node


def get_min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current


def delete_bst(node, key):
    if node is None:
        return None

    # 1. Ищем узел для удаления
    if key < node.value:
        node.left = delete_bst(node.left, key)
    elif key > node.value:
        node.right = delete_bst(node.right, key)
    else:
        # Узел найден.

        # Случай 1 и 2: У узла один ребенок или нет детей
        if node.left is None:
            temp = node.right
            node = None
            return temp
        elif node.right is None:
            temp = node.left
            node = None
            return temp

        # Случай 3: У узла два ребенка.
        # Находим минимальный элемент в правом поддереве (наследник)
        temp = get_min_value_node(node.right)

        # Копируем значение наследника в текущий узел
        node.value = temp.value

        # Удаляем наследника из правого поддерева
        node.right = delete_bst(node.right, temp.value)

    return node


# --- Основное меню ---

def main():
    print("=== Лаба №17: Операции над БДП ===")
    # Пример валидного БДП для ввода: 8 (3 (1, 6 (4, 7)), 10 ( , 14 (13, )))
    print("Введите дерево в линейно-скобочной записи.")
    print("Пример БДП: 8 (3 (1, 6 (4, 7)), 10 ( , 14 (13, )))")

    raw_input = input("Ввод: ")
    root = parse_tree(raw_input)

    while True:
        print("\n--- МЕНЮ ---")
        print("1. Найти вершину")
        print("2. Добавить вершину")
        print("3. Удалить вершину")
        print("4. Показать текущее дерево (строка)")
        print("0. Выход (с печатью результата)")

        choice = input("Ваш выбор: ")

        try:
            if choice == '1':
                val = int(input("Введите число для поиска: "))
                res = search_bst(root, val)
                if res:
                    print(f"  [+] Узел {val} найден в дереве.")
                else:
                    print(f"  [-] Узел {val} НЕ найден.")

            elif choice == '2':
                val = int(input("Введите число для добавления: "))
                # Если дерево было пустым
                if root is None:
                    root = Node(val)
                else:
                    insert_bst(root, val)
                print("  [OK] Операция выполнена.")

            elif choice == '3':
                val = int(input("Введите число для удаления: "))
                if search_bst(root, val):
                    root = delete_bst(root, val)
                    print(f"  [OK] Узел {val} удален.")
                else:
                    print(f"  [!] Узел {val} не найден, удалять нечего.")

            elif choice == '4':
                print("Текущее дерево: ", tree_to_str(root))

            elif choice == '0':
                break
            else:
                print("Неверный ввод, попробуйте снова.")
        except ValueError:
            print("Пожалуйста, вводите целые числа.")

    print("\n=== Завершение работы ===")
    print("Итоговое дерево:")
    print(tree_to_str(root))


if __name__ == "__main__":
    main()