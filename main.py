class StackEmptyError(Exception): # класс исключения для создания собственного типа ошибки
    pass


class StackNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class Stack: # класс стека
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, item):
        new_node = StackNode(item, self.top)
        self.top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise StackEmptyError("Попытка извлечь элемент из пустого стека.")
        value = self.top.value
        self.top = self.top.next
        self._size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise StackEmptyError("Попытка посмотреть верхушку пустого стека.")
        return self.top.value

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size


class MathOperations: # класс для нахождения минимума/максимума
    @staticmethod # декоратор для того, чтобы можно было использовать функцию без создания экземпляра класса
    def custom_min(a, b):
        if a < b:
            return a
        return b

    @staticmethod
    def custom_max(a, b):
        if a > b:
            return a
        return b


class ExpressionEvaluator: # класс для вычисления/ выражения из стека
    def __init__(self, expression):
        self.expression = expression # сохранение строки
        self.stack = Stack() # инициализация стека

    def _validate_expression(self):
        allowed_chars = set("mM0123456789(),")
        for char in self.expression:
            if char not in allowed_chars:
                raise ValueError(f"Недопустимый символ: {char}")

        # Проверка сбалансированности скобок
        balance = 0
        for char in self.expression:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            # Скобки закрываются до открытия — ошибка
            if balance < 0:
                raise ValueError("Скобки расставлены неправильно.")
        
        if balance != 0:
            raise ValueError("Несбалансированное количество скобок.")
        
        if not any(c.isdigit() for c in self.expression):
            raise ValueError("Выражение не содержит чисел.")
        
        if not any(c in "mM" for c in self.expression):
            raise ValueError("Выражение не содержит операций m или M.")

    def evaluate(self):
        self._validate_expression()
        i = 0
        while i < len(self.expression): # посимвольное чтение строки
            char = self.expression[i]
            if char.isdigit(): # если символ - число
                num = ''
                while i < len(self.expression) and self.expression[i].isdigit(): # собираем число целиком
                    num += self.expression[i]
                    i += 1
                self.stack.push(int(num)) # добавляем число в стек
                continue
            elif char in ('m', 'M', '(', ',', ')'):
                self.stack.push(char)
            i += 1

        return self._process_stack() # обработка стека

    def _process_stack(self):
        temp_stack = Stack()

        while not self.stack.is_empty(): # рассматриваем стек в обратном порядке
            token = self.stack.pop()
            temp_stack.push(token)

        return self._evaluate_tokens(temp_stack) # обработка стека

    def _evaluate_tokens(self, tokens):
        while tokens.size() > 1:
            temp = Stack()
            while not tokens.is_empty():
                token = tokens.pop()
                if token == ')': # если нашли закрывающую скобку, начинаем собирать выражение
                    try:
                        arg2 = temp.pop()
                        comma = temp.pop()
                        arg1 = temp.pop()
                        open_bracket = temp.pop()
                        func = temp.pop()
                    except StackEmptyError:
                        raise ValueError('Некорректное выражение: недостаточно символов.')

                    if func == 'm':
                        result = MathOperations.custom_min(arg1, arg2)
                    elif func == 'M':
                        result = MathOperations.custom_max(arg1, arg2)
                    else:
                        raise ValueError(f"Неизвестная операция: {func}")

                    temp.push(result) # результат операции добавляем обратно в стек
                else:
                    temp.push(token)

            tokens = temp

        if tokens.is_empty():
            raise ValueError('Некорректное выражение.')
        return tokens.pop()


if __name__ == "__main__":
    while True:
        try:
            expression = input("Введите выражение (например, M(15,m(16,8))): ")
            evaluator = ExpressionEvaluator(expression)
            result = evaluator.evaluate()
            print(f"Результат: {result}")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            print('Введите данные снова.')