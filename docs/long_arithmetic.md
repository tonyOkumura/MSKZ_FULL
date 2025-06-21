# Длинная арифметика: Сложение, вычитание, умножение и деление

В этом документе описаны реализации базовых арифметических операций для чисел произвольной длины. Основой для всех операций является класс `LargeNumber`, который представляет число как список его цифр в обратном порядке и отдельный флаг для знака.

## Представление `LargeNumber`

Число хранится в виде объекта со следующими полями:
- `digits`: Список (list) целых чисел, где каждый элемент — это цифра числа. Цифры хранятся в обратном порядке для удобства вычислений (младший разряд находится в начале списка). Например, число `123` будет представлено как `[3, 2, 1]`.
- `is_negative`: Булево значение, `True` если число отрицательное, и `False` в противном случае.

```python
class LargeNumber:
    def __init__(self, value_str: str = "0", base: int = 10):
        if not (2 <= base <= 36):
            raise ValueError("Основание системы счисления должно быть от 2 до 36.")
        
        self.is_negative = False
        if value_str.startswith('-'):
            self.is_negative = True
            value_str = value_str[1:]
            if not value_str: # Handle case of "-"
                 raise ValueError("Недопустимое число: '-'")

        self.digits = []
        for char in reversed(value_str.upper()):
            digit = _char_to_int(char)
            if digit >= base:
                raise ValueError(f"Цифра '{char}' недопустима для основания {base}.")
            self.digits.append(digit)
        
        if not self.digits:
            self.digits.append(0)
            
        _remove_leading_zeros(self.digits)

        # Ноль не может быть отрицательным
        if len(self.digits) == 1 and self.digits[0] == 0:
            self.is_negative = False
```

---

## 1. Сложение

Логика сложения зависит от знаков чисел.

- **Если знаки одинаковые**: Модули чисел складываются "в столбик". Знак результата совпадает со знаком слагаемых.
- **Если знаки разные**: Из модуля большего числа вычитается модуль меньшего. Знак результата совпадает со знаком числа с большим модулем.

Это реализовано в функции `add`, которая делегирует вычисления вспомогательным функциям `_add_abs` (сложение модулей) и `_subtract_abs` (вычитание модулей).

### Исходный код

```python
def _add_abs(num_a, num_b, base=10):
    # Эта функция складывает абсолютные значения
    result_digits = []
    carry = 0
    max_len = max(len(num_a.digits), len(num_b.digits))
    for i in range(max_len):
        digit_a = num_a.digits[i] if i < len(num_a.digits) else 0
        digit_b = num_b.digits[i] if i < len(num_b.digits) else 0
        total = digit_a + digit_b + carry
        result_digits.append(total % base)
        carry = total // base
    if carry > 0:
        result_digits.append(carry)
    result = LargeNumber("0", base)
    result.digits = _remove_leading_zeros(result_digits)
    return result

def add(num_a: LargeNumber, num_b: LargeNumber, base: int = 10) -> LargeNumber:
    if num_a.is_negative == num_b.is_negative:
        result = _add_abs(num_a, num_b, base)
        result.is_negative = num_a.is_negative
    else:
        if _is_abs_greater_or_equal(num_a, num_b):
            result = _subtract_abs(num_a, num_b, base)
            result.is_negative = num_a.is_negative
        else:
            result = _subtract_abs(num_b, num_a, base)
            result.is_negative = num_b.is_negative
    return result
```

---

## 2. Вычитание

Вычитание реализовано через сложение. Операция `A - B` эквивалентна `A + (-B)`. Это позволяет повторно использовать уже реализованную логику сложения, просто поменяв знак у вычитаемого.

### Исходный код

```python
def _subtract_abs(num_a, num_b, base=10):
    # Эта функция вычитает абсолютные значения, |num_a| >= |num_b|
    result_digits = []
    borrow = 0
    for i in range(len(num_a.digits)):
        digit_a = num_a.digits[i]
        digit_b = num_b.digits[i] if i < len(num_b.digits) else 0
        diff = digit_a - digit_b - borrow
        if diff < 0:
            diff += base
            borrow = 1
        else:
            borrow = 0
        result_digits.append(diff)
    result = LargeNumber("0", base)
    result.digits = _remove_leading_zeros(result_digits)
    return result

def subtract(num_a: LargeNumber, num_b: LargeNumber, base: int = 10) -> LargeNumber:
    neg_b = LargeNumber(num_b.to_string(base), base)
    if neg_b.to_string(base) != "0":
        neg_b.is_negative = not neg_b.is_negative
    return add(num_a, neg_b, base)
```

---

## 3. Умножение

Реализован классический алгоритм умножения "в столбик".

1.  Создается массив для хранения результата, его размер равен сумме длин сомножителей.
2.  Алгоритм итерируется по каждой цифре второго числа (`num_b`).
3.  Во внутреннем цикле он итерируется по каждой цифре первого числа (`num_a`).
4.  Произведение текущих цифр `num_a.digits[j] * num_b.digits[i]` добавляется к соответствующей позиции в результирующем массиве `result_digits[i + j]`.
5.  Вычисляется и переносится остаток (`carry`) на следующую позицию.
6.  Знак результата определяется по правилу: `минус` на `плюс` дает `минус`. Если знаки сомножителей разные, результат будет отрицательным.

### Исходный код

```python
def multiply(num_a: LargeNumber, num_b: LargeNumber, base: int = 10) -> LargeNumber:
    """Умножает два больших числа (Алгоритм 3)."""
    if (len(num_a.digits) == 1 and num_a.digits[0] == 0) or \
       (len(num_b.digits) == 1 and num_b.digits[0] == 0):
        return LargeNumber("0", base)

    len_a = len(num_a.digits)
    len_b = len(num_b.digits)
    result_digits = [0] * (len_a + len_b)

    for i in range(len_b):
        carry = 0
        for j in range(len_a):
            total = result_digits[i + j] + num_a.digits[j] * num_b.digits[i] + carry
            result_digits[i + j] = total % base
            carry = total // base
        if carry > 0:
            result_digits[i + len_a] += carry

    result = LargeNumber("0", base)
    result.digits = _remove_leading_zeros(result_digits)
    result.is_negative = num_a.is_negative != num_b.is_negative
    if len(result.digits) == 1 and result.digits[0] == 0:
        result.is_negative = False
    return result
```

---

## 4. Деление

Деление реализует алгоритм деления "в столбик" и возвращает пару (частное, остаток).

1.  Операция выполняется над абсолютными значениями чисел.
2.  Алгоритм итерируется по цифрам делимого (`num_a`), последовательно формируя текущее делимое (`current_dividend`).
3.  На каждом шаге определяется очередная цифра частного. Для этого используется **бинарный поиск**, который находит максимальную цифру `q` (от 0 до `base-1`), такую что `q * делитель <= current_dividend`. Это эффективнее, чем последовательный перебор.
4.  Найденная цифра `q` добавляется к результату (частному).
5.  Из `current_dividend` вычитается `q * делитель`, и к нему дописывается следующая цифра из `num_a`.
6.  Процесс повторяется до тех пор, пока не будут обработаны все цифры делимого.
7.  Знаки частного и остатка определяются в конце:
    - Знак частного отрицателен, если знаки делимого и делителя разные.
    - Знак остатка совпадает со знаком делимого.

### Исходный код

```python
def divide(num_a: LargeNumber, num_b: LargeNumber, base: int = 10) -> (LargeNumber, LargeNumber):
    """Делит два больших числа (A / B), возвращая частное и остаток."""
    if len(num_b.digits) == 1 and num_b.digits[0] == 0:
        raise ZeroDivisionError("Деление на ноль.")

    # Работаем с абсолютными значениями
    a_abs = LargeNumber(num_a.to_string(base).replace('-', ''), base)
    b_abs = LargeNumber(num_b.to_string(base).replace('-', ''), base)

    if not _is_abs_greater_or_equal(a_abs, b_abs):
        return LargeNumber("0", base), LargeNumber(num_a.to_string(base), base)

    quotient_str = ""
    current_dividend = LargeNumber("0", base)
    
    for digit_char in a_abs.to_string(base):
        current_dividend_str = current_dividend.to_string(base)
        if current_dividend_str == "0":
             current_dividend_str = ""
        current_dividend = LargeNumber(current_dividend_str + digit_char, base)
        
        if not _is_abs_greater_or_equal(current_dividend, b_abs):
            if quotient_str: 
                quotient_str += "0"
            continue
        
        q_digit = 0
        low, high = 0, base
        while low < high:
            mid = (low + high) // 2
            if mid == 0: # Avoid infinite loop
                low = 1
                continue
            
            test_product = multiply(b_abs, LargeNumber(_int_to_char(mid), base), base)
            if _is_abs_greater_or_equal(current_dividend, test_product):
                q_digit = mid
                low = mid + 1
            else:
                high = mid
        
        quotient_str += _int_to_char(q_digit)
        subtrahend = multiply(b_abs, LargeNumber(_int_to_char(q_digit), base), base)
        current_dividend = _subtract_abs(current_dividend, subtrahend, base)

    final_quotient = LargeNumber(quotient_str or "0", base)
    final_remainder = LargeNumber(current_dividend.to_string(base) or "0", base)

    final_quotient.is_negative = num_a.is_negative != num_b.is_negative
    if len(final_quotient.digits) == 1 and final_quotient.digits[0] == 0:
        final_quotient.is_negative = False
    
    # Знак остатка обычно совпадает со знаком делимого
    final_remainder.is_negative = num_a.is_negative
    if len(final_remainder.digits) == 1 and final_remainder.digits[0] == 0:
        final_remainder.is_negative = False
        
    return final_quotient, final_remainder
``` 