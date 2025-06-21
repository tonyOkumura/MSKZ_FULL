# Алгоритм Евклида и Расширенный алгоритм Евклида

Этот документ описывает алгоритм Евклида для нахождения наибольшего общего делителя (НОД) двух чисел и его расширенную версию, которая также находит коэффициенты Безу.

---

## 1. Алгоритм Евклида (для НОД)

Алгоритм Евклида — это эффективный метод вычисления наибольшего общего делителя (НОД) двух целых чисел.

### Алгоритм

Основан на принципе, что НОД двух чисел не меняется, если большее число заменить на его остаток от деления на меньшее число.
1.  Берем два числа, `a` и `b`.
2.  Пока `b` не равно нулю, заменяем `a` на `b`, а `b` — на остаток от деления `a` на `b`.
3.  Когда `b` становится равным нулю, `a` и есть НОД исходных чисел.

### Исходный код

```python
def gcd(a: LargeNumber, b: LargeNumber) -> LargeNumber:
    """Вычисляет наибольший общий делитель (НОД) для двух больших чисел."""
    base = 10
    zero = LargeNumber("0", base)
    
    # Работаем с абсолютными значениями
    a_abs = LargeNumber(a.to_string(base).replace('-', ''), base)
    b_abs = LargeNumber(b.to_string(base).replace('-', ''), base)

    while b_abs.to_string(base) != zero.to_string(base):
        _, remainder = divide(a_abs, b_abs, base)
        a_abs = b_abs
        b_abs = remainder
        
    return a_abs
```

---

## 2. Расширенный алгоритм Евклида

Расширенный алгоритм Евклида не только находит НОД чисел `a` и `b`, но и находит пару целых чисел `x` и `y` (коэффициенты Безу), которые удовлетворяют уравнению:
`a*x + b*y = НОД(a, b)`

Это свойство является ключевым для вычисления мультипликативного обратного элемента в модульной арифметике.

### Алгоритм

Алгоритм является итеративным расширением стандартного алгоритма Евклида. На каждом шаге он вычисляет не только остатки, но и коэффициенты для них.

1. Инициализируем `(x, last_x) = (0, 1)` и `(y, last_y) = (1, 0)`.
2. В цикле, пока `b` не ноль:
    a. Вычисляем частное `q = a // b`.
    b. Обновляем `a` и `b`: `(a, b) = (b, a % b)`.
    c. Обновляем коэффициенты: `(x, last_x) = (last_x - q*x, x)` и `(y, last_y) = (last_y - q*y, y)`.
3. В конце `last_x` и `last_y` будут искомыми коэффициентами, а `a` — НОД.

### Исходный код

```python
def extended_gcd(a: LargeNumber, b: LargeNumber) -> (LargeNumber, LargeNumber, LargeNumber):
    """
    Выполняет расширенный алгоритм Евклида.
    Возвращает (g, x, y), где g = НОД(a, b) и a*x + b*y = g.
    """
    base = 10
    zero = LargeNumber("0", base)
    one = LargeNumber("1", base)

    # Инициализация коэффициентов Безу
    x, last_x = LargeNumber("0", base), LargeNumber("1", base)
    y, last_y = LargeNumber("1", base), LargeNumber("0", base)

    # Алгоритм работает с копиями, чтобы не изменять оригинальные числа
    a_copy = LargeNumber(a.to_string(base), base)
    b_copy = LargeNumber(b.to_string(base), base)

    while b_copy.to_string(base) != "0":
        quotient, remainder = divide(a_copy, b_copy, base)
        
        a_copy, b_copy = b_copy, remainder

        # Обновляем коэффициенты x
        temp_x = x
        x = subtract(last_x, multiply(quotient, x, base), base)
        last_x = temp_x

        # Обновляем коэффициенты y
        temp_y = y
        y = subtract(last_y, multiply(quotient, y, base), base)
        last_y = temp_y
        
    # a_copy теперь содержит НОД
    # last_x и last_y - коэффициенты Безу
    return a_copy, last_x, last_y
``` 