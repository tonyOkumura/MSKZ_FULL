# Модульное возведение в степень

Этот документ описывает алгоритм модульного возведения в степень, который позволяет эффективно вычислять `(base ^ exponent) mod n` для очень больших чисел. Прямой расчет `base ^ exponent` и последующее взятие остатка невозможны из-за огромного размера промежуточного результата.

## Алгоритм бинарного возведения в степень (справа-налево)

Основная идея заключается в том, чтобы использовать двоичное представление показателя степени `exponent`. Алгоритм работает следующим образом:

1.  Инициализируется результат `result = 1`.
2.  Начальное значение `base` приводится по модулю `n`.
3.  Цикл продолжается, пока показатель степени `exponent` больше нуля.
4.  На каждой итерации цикла:
    a.  Проверяется, является ли `exponent` нечетным (т.е. последний бит в его двоичном представлении равен 1). Если да, то `result` умножается на текущее значение `base` по модулю `n`.
    b.  `base` возводится в квадрат по модулю `n` (`base = (base * base) mod n`).
    c.  `exponent` целочисленно делится на 2 (что эквивалентно сдвигу вправо на один бит).

Этот подход значительно сокращает количество необходимых умножений. Вместо `exponent - 1` умножений требуется всего `O(log(exponent))` умножений. Применение операции по модулю на каждом шаге предотвращает рост промежуточных чисел.

## Реализация

Функция `mod_power` реализует описанный алгоритм. Она принимает основание `base_num`, показатель `exp_num` и модуль `mod_num`.

### Исходный код

```python
from .long_arithmetic import (LargeNumber, add, subtract, multiply, divide, 
                                _is_abs_greater_or_equal as is_greater_or_equal, 
                                power_integer, gcd)

def mod_power(base_num, exp_num, mod_num):
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    result = LargeNumber("1", base)

    # Приводим основание по модулю
    _, base_val = divide(base_num, mod_num, base) 
    
    exp_val = LargeNumber(exp_num.to_string(base), base)

    # Цикл, пока показатель степени > 0
    while is_greater_or_equal(exp_val, one):
        # Если показатель нечетный, умножаем результат на основание
        _, remainder = divide(exp_val, two, base)
        if remainder.to_string(base) == "1":
            result = multiply(result, base_val, base)
            _, result = divide(result, mod_num, base)
        
        # Делим показатель на 2
        exp_val, _ = divide(exp_val, two, base)
        
        # Возводим основание в квадрат
        base_val = multiply(base_val, base_val, base)
        _, base_val = divide(base_val, mod_num, base)
        
    return result
``` 