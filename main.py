class StackEmptyError(Exception):
    pass


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise StackEmptyError("Попытка извлечь элемент из пустого стека.")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise StackEmptyError("Попытка посмотреть верхушку пустого стека.")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


class MathOperations:
    @staticmethod
    def custom_min(a, b):
        if a < b:
            return a
        return b

    @staticmethod
    def custom_max(a, b):
        if a > b:
            return a
        return b


class ExpressionEvaluator:
    def __init__(self, expression):
        self.expression = expression
        self.stack = Stack()

    def evaluate(self):
        i = 0
        while i < len(self.expression):
            char = self.expression[i]
            if char.isdigit():
                num = ''
                while i < len(self.expression) and self.expression[i].isdigit():
                    num += self.expression[i]
                    i += 1
                self.stack.push(int(num))
                continue  # не увеличиваем i здесь, т.к. он уже инкрементирован
            elif char in ('m', 'M', '(', ',', ')'):
                self.stack.push(char)
            i += 1

        return self._process_stack()

    def _process_stack(self):
        temp_stack = Stack()

        while not self.stack.is_empty():
            token = self.stack.pop()
            temp_stack.push(token)

        return self._evaluate_tokens(temp_stack)

    def _evaluate_tokens(self, tokens: Stack):
        while tokens.size() > 1:
            temp = Stack()
            while not tokens.is_empty():
                token = tokens.pop()
                if token == ')':
                    arg2 = temp.pop()
                    comma = temp.pop()
                    arg1 = temp.pop()
                    open_bracket = temp.pop()
                    func = temp.pop()

                    if func == 'm':
                        result = MathOperations.custom_min(arg1, arg2)
                    elif func == 'M':
                        result = MathOperations.custom_max(arg1, arg2)
                    else:
                        raise ValueError(f"Неизвестная операция: {func}")

                    temp.push(result)
                else:
                    temp.push(token)

            tokens = temp

        return tokens.pop()


if __name__ == "__main__":
    try:
        expression = input("Введите выражение (например, M(15,m(16,8))): ")
        evaluator = ExpressionEvaluator(expression)
        result = evaluator.evaluate()
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")
