from math import log

def lab1(): # Правильная скобочная последовательность
    string = input("Введите строку: ") # ({})[  )()[]  ([)]  ([{}])  ()[({}())]  ([()])({}())
    stack = ""
    types = "()[]{}"
    tr = {")": "(", "]": "[", "}": "{"}
    try:
        for i in set(string):
            if i not in types:
                raise IndexError
        for i in string:
            if i in tr.values():
                stack += i
            elif tr.get(i) == stack[-1]:
                stack = stack[:-1]
            else:
                raise IndexError
        if stack:
            raise IndexError
        print("Строка существует")
    except IndexError:
        print("Строка не существует")


def lab2(): # Правильное математическое выражение (Обратная Польская Запись)
    def check_brackets(string: str) -> bool:
        stack = []
        for ch in string:
            if ch == '(':
                stack.append(ch)
            elif ch == ')':
                if not stack:
                    return False
                stack.pop()
        return len(stack) == 0

    def to_rpn(expr: str) -> list:
        priority = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        stack = []
        num = ''

        for ch in expr:
            if ch.isdigit() or ch == '.':
                num += ch
            else:
                if num:
                    output.append(num)
                    num = ''
                if ch in priority:
                    while stack and stack[-1] != '(' and priority[ch] <= priority[stack[-1]]:
                        output.append(stack.pop())
                    stack.append(ch)
                elif ch == '(':
                    stack.append(ch)
                elif ch == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    if not stack:
                        raise ValueError("Ошибка: скобки расставлены неверно!")
                    stack.pop()  # убрать '('
                elif ch not in ' \t':
                    raise ValueError(f"Ошибка: недопустимый символ '{ch}'!")

        if num:
            output.append(num)

        while stack:
            if stack[-1] in '()':
                raise ValueError("Ошибка: скобки расставлены неверно!")
            output.append(stack.pop())

        return output

    def calc_rpn(tokens: list) -> float:
        stack = []
        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Ошибка: неверное выражение!")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Ошибка: деление на ноль!")
                    stack.append(a / b)
                else:
                    raise ValueError(f"Ошибка: неизвестный оператор '{token}'!")
        if len(stack) != 1:
            raise ValueError("Ошибка: неверное выражение!")
        return stack[0]

    line = input("Введите выражение: ").strip() # 2+7*(3/9)-5=  (2+3*(4-1))=  4/0+2=  1+(2-3=
    if line.endswith("="):
        line = line[:-1]
    else:
        print("Ошибка: выражение должно заканчиваться знаком '='.")
        return
    if not check_brackets(line):
        print("Ошибка: скобки расставлены неверно!")
        return
    try:
        rpn = to_rpn(line)
        result = calc_rpn(rpn)
        print("Результат:", result)
    except Exception as e:
        print(e)


def lab3(): # Простые множители
    x = int(input("Введите число х, где x > 0: "))
    ans = []
    max_pow = int(log(x, 3) + 1) + 1
    for k in range(0, max_pow):
        for l in range(0, max_pow - k):
            for m in range(0, max_pow - k - 1):
                num = (3 ** k) * (5 ** l) * (7 ** m)
                if num <= x:
                    ans += [(num, k, l, m)]
    print("Числа, от 1 до х, равные 3^k * 5^l * 7^m:")
    print("\n".join([f"{number}, k = {k}, l = {l}, m = {m}" for number, k, l, m in sorted(ans, key=lambda a: a[0])]))


lab3()