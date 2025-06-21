# Ускоренное модульное умножение

Этот документ описывает реализацию алгоритма ускоренного модульного умножения, который оптимизирован для модулей специального вида `p = 2^n ± c`, где `c` — небольшое число. Такой подход позволяет избежать стандартного долгого деления на `p` и заменить его более быстрыми операциями.

## Основная идея алгоритма

Пусть нам нужно вычислить `(a * b) mod p`.
1.  Сначала вычисляется произведение `prod = a * b`.
2.  Это произведение можно представить в виде `prod = A * 2^n + B`, где `A` — это частное, а `B` — остаток от деления `prod` на `2^n`. Деление на `2^n` является очень быстрой операцией, так как сводится к побитовому сдвигу.
3.  Из основного тождества `p = 2^n ± c` мы можем выразить `2^n = p ∓ c`.
4.  Подставляем это в представление `prod`:
    `prod = A * (p ∓ c) + B = A*p ∓ A*c + B`
5.  Поскольку `A*p` делится на `p` нацело, остаток от деления `prod` на `p` будет таким же, как остаток от деления `B ∓ A*c` на `p`.
    `(a * b) mod p = (B ∓ A*c) mod p`

Таким образом, мы заменили одно большое деление на `p` на:
- Одно деление на `2^n` (быстрое).
- Одно умножение на малое число `c`.
- Одно сложение или вычитание.
- Одно финальное деление на `p`, но уже от гораздо меньшего числа.

## Реализация

Функция `fast_modular_multiplication` принимает на вход два числа `a` и `b`, параметры `n` и `c` для вычисления модуля `p`, а также `sign` (`+` или `-`), определяющий вид модуля.

### Исходный код

```python
from .long_arithmetic import (LargeNumber, add, subtract, multiply, divide, 
                                _is_abs_greater_or_equal as is_greater_or_equal, 
                                power_integer, gcd)

def fast_modular_multiplication(a, b, n_val, c_val, sign):
    base = 10
    two = LargeNumber("2", base)
    two_n = power_integer(two, n_val)
    p = add(two_n, c_val, base) if sign == '+' else subtract(two_n, c_val, base)
    prod = multiply(a, b, base)
    A, B = divide(prod, two_n, base)
    cA = multiply(c_val, A, base)
    if sign == '+':
        if is_greater_or_equal(B, cA):
            temp_res = subtract(B, cA, base)
        else:
            diff = subtract(cA, B, base)
            _, diff_mod_p = divide(diff, p, base)
            temp_res = LargeNumber("0", base) if diff_mod_p.to_string(base) == "0" else subtract(p, diff_mod_p, base)
    else:
        temp_res = add(B, cA, base)
    _, final_result = divide(temp_res, p, base)
    return final_result, p 