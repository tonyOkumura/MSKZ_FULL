# Извлечение квадратных корней по составному модулю

В этом документе описывается алгоритм для нахождения квадратных корней по составному модулю `n`, который является произведением двух различных простых чисел `p` и `q`. Эта задача часто встречается в криптографии, например, в криптосистеме Рабина.

## Теоретическая основа

Задача состоит в том, чтобы найти все решения `x` для сравнения:
`x^2 ≡ c (mod n)`
где `n = p * q`.

Используя **Китайскую теорему об остатках (КТО)**, мы можем разбить это одно сравнение на систему из двух сравнений:
1.  `x^2 ≡ c (mod p)`
2.  `x^2 ≡ c (mod q)`

Решив каждое из них, мы получим наборы корней по модулю `p` и по модулю `q`. Затем, комбинируя их с помощью КТО, мы найдем все четыре квадратных корня по исходному модулю `n`.

### 1. Нахождение корней по простому модулю

Реализация в проекте использует эффективный метод для частного случая, когда простые `p` и `q` имеют вид `4k + 3`. Для такого простого числа `p`, если `c` является квадратичным вычетом, его квадратные корни вычисляются по формуле:
`x_p = ± c^((p+1)/4) mod p`

Аналогично для `q`:
`x_q = ± c^((q+1)/4) mod q`

Таким образом, мы получаем два корня по модулю `p` (`mp1`, `mp2`) и два корня по модулю `q` (`mq1`, `mq2`).

### 2. Комбинация решений с помощью КТО

Имея корни по простым модулям, мы формируем четыре системы сравнений:
1. `x ≡ mp1 (mod p)` и `x ≡ mq1 (mod q)`
2. `x ≡ mp1 (mod p)` и `x ≡ mq2 (mod q)`
3. `x ≡ mp2 (mod p)` и `x ≡ mq1 (mod q)`
4. `x ≡ mp2 (mod p)` и `x ≡ mq2 (mod q)`

Каждая система решается с помощью КТО, что дает нам четыре итоговых корня по модулю `n`. Решение для системы `x ≡ a (mod p)` и `x ≡ b (mod q)` имеет вид:
`x = (a * q * mod_inverse(q, p) + b * p * mod_inverse(p, q)) mod n`

## Реализация

Функция `modular_sqrt` принимает на вход число `c` и два простых сомножителя `p` и `q`. Она последовательно выполняет шаги, описанные выше, и возвращает список из четырех квадратных корней.

### Исходный код

```python
from .long_arithmetic import (LargeNumber, add, subtract, multiply, divide, 
                                _is_abs_greater_or_equal as is_greater_or_equal, 
                                power_integer, gcd)

def mod_power(base_num, exp_num, mod_num):
    # ... (реализация модульного возведения в степень)
    pass

def mod_inverse(num, mod):
    # ... (реализация нахождения обратного элемента)
    pass

def modular_sqrt(c, p, q):
    base = 10
    one = LargeNumber("1", base)
    four = LargeNumber("4", base)
    n = multiply(p, q, base)
    
    # Находим корни по модулю p: ±c^((p+1)/4) mod p
    exp_p_num = add(p, one, base)
    exp_p, _ = divide(exp_p_num, four, base)
    mp1 = mod_power(c, exp_p, p)
    mp2 = subtract(p, mp1, base)
    
    # Находим корни по модулю q: ±c^((q+1)/4) mod q
    exp_q_num = add(q, one, base)
    exp_q, _ = divide(exp_q_num, four, base)
    mq1 = mod_power(c, exp_q, q)
    mq2 = subtract(q, mq1, base)
    
    # Используем КТО для нахождения 4-х корней по модулю n
    q_inv_p = mod_inverse(q, p)
    p_inv_q = mod_inverse(p, q)
    
    term_a = multiply(q, q_inv_p, base)
    term_b = multiply(p, p_inv_q, base)
    
    # Корень 1: (mp1, mq1)
    part1_m1 = multiply(mp1, term_a, base)
    part2_m1 = multiply(mq1, term_b, base)
    sum_m1 = add(part1_m1, part2_m1, base)
    _, m1 = divide(sum_m1, n, base)
    
    # Корень 2: (mp1, mq2)
    part1_m2 = multiply(mp1, term_a, base)
    part2_m2 = multiply(mq2, term_b, base)
    sum_m2 = add(part1_m2, part2_m2, base)
    _, m2 = divide(sum_m2, n, base)
    
    # Корень 3: (mp2, mq1)
    part1_m3 = multiply(mp2, term_a, base)
    part2_m3 = multiply(mq1, term_b, base)
    sum_m3 = add(part1_m3, part2_m3, base)
    _, m3 = divide(sum_m3, n, base)

    # Корень 4: (mp2, mq2)
    part1_m4 = multiply(mp2, term_a, base)
    part2_m4 = multiply(mq2, term_b, base)
    sum_m4 = add(part1_m4, part2_m4, base)
    _, m4 = divide(sum_m4, n, base)
    
    return [m1, m2, m3, m4]
```
Примечание: В приведенном выше коде функции `mod_power` и `mod_inverse` предполагаются уже реализованными. 