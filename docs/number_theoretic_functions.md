# Теоретико-числовые функции

В этом документе описаны важные теоретико-числовые функции, которые используются в качестве строительных блоков в более сложных криптографических алгоритмах, таких как тесты на простоту.

---

## 1. Функция Эйлера

Функция Эйлера `φ(n)` (фи от n) подсчитывает количество натуральных чисел до `n`, которые взаимно просты с `n`. Эта функция является центральной в криптосистеме RSA.

### Алгоритм вычисления

Если известна каноническая факторизация числа `n = p₁^k₁ * p₂^k₂ * ... * pᵣ^kᵣ`, где `pᵢ` — различные простые делители, то функция Эйлера вычисляется по формуле:
`φ(n) = n * (1 - 1/p₁) * (1 - 1/p₂) * ... * (1 - 1/pᵣ)`

Реализация следует этому подходу:
1.  Найти все уникальные простые делители числа `n` (с помощью пробных делений).
2.  Применить вышеуказанную формулу.

### Исходный код

```python
def prime_factorization(n: LargeNumber) -> list[LargeNumber]:
    """Находит уникальные простые делители числа n методом пробных делений."""
    # ... (реализация) ...

def euler_totient(m: LargeNumber) -> LargeNumber:
    """Вычисляет функцию Эйлера φ(m)."""
    one = LargeNumber("1")
    if m.to_string() == one.to_string():
        return one
    
    factors = prime_factorization(m)
    result = LargeNumber(m.to_string())
    
    for p in factors:
        p_minus_1 = subtract(p, one)
        # Эквивалентно result = result * (1 - 1/p)
        result = multiply(result, p_minus_1)
        result, _ = divide(result, p)
        
    return result
```

---

## 2. Символ Лежандра

Символ Лежандра `(a/p)` определяет, является ли число `a` квадратичным вычетом по модулю нечетного простого числа `p`.

-   `(a/p) = 1`, если `a` — квадратичный вычет по модулю `p` (т.е. существует `x` такой, что `x² ≡ a (mod p)`) и `a` не делится на `p`.
-   `(a/p) = -1`, если `a` — квадратичный невычет по модулю `p`.
-   `(a/p) = 0`, если `a ≡ 0 (mod p)`.

### Алгоритм вычисления (Критерий Эйлера)

Символ Лежандра эффективно вычисляется с помощью критерия Эйлера:
`(a/p) ≡ a^((p-1)/2) (mod p)`

### Исходный код

```python
from .modular_arithmetic import mod_power

def legendre_symbol(a, p):
    """
    Вычисляет символ Лежандра (a/p) используя критерий Эйлера.
    Возвращает 1, -1 или 0.
    """
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    
    # (a/p) = 0 если a делится на p
    _, rem = divide(a, p)
    if rem.to_string() == "0":
        return 0

    p_minus_1 = subtract(p, one, base)
    exponent, _ = divide(p_minus_1, two, base)
    
    result_large_num = mod_power(a, exponent, p)
    
    if result_large_num.to_string(base) == "1":
        return 1
    else: # Для простого p, если результат не 1, он должен быть p-1.
        return -1
```

---

## 3. Символ Якоби

Символ Якоби `(a/n)` является обобщением символа Лежандра на случай, когда `n` — любое нечетное положительное целое число. Если `n = p₁ * p₂ * ... * pₖ` — разложение `n` на простые множители, то:
`(a/n) = (a/p₁) * (a/p₂) * ... * (a/pₖ)`

**Важно**: Если `(a/n) = -1`, то `a` точно является квадратичным невычетом по модулю `n`. Однако, если `(a/n) = 1`, это **не** означает, что `a` является квадратичным вычетом.

### Алгоритм вычисления

Символ Якоби вычисляется без необходимости факторизации `n`, используя набор свойств, включая закон квадратичной взаимности. Это делает его вычисление очень быстрым. Алгоритм рекурсивно упрощает символ, пока не дойдет до базового случая.

### Исходный код

```python
def jacobi_symbol(a: LargeNumber, n: LargeNumber) -> int:
    """
    Вычисляет символ Якоби (a/n).
    n должно быть нечетным положительным целым числом.
    """
    # ... (длинная реализация, использующая свойства символа Якоби) ...
    # 1. (a/n) = (a mod n / n)
    # 2. (2k/n) = (2/n)(k/n), и свойство для (2/n)
    # 3. (m/n) = -(n/m), если m=n=3 (mod 4), иначе (m/n)=(n/m) (закон взаимности)
    # ...
    zero = LargeNumber("0")
    one = LargeNumber("1")
    two = LargeNumber("2")
    three = LargeNumber("3")
    four = LargeNumber("4")
    five = LargeNumber("5")
    seven = LargeNumber("7")
    eight = LargeNumber("8")

    _, n_rem_2 = divide(n, two)
    if not is_greater_or_equal(n, one) or n_rem_2.to_string() == zero.to_string():
        raise ValueError("n должно быть нечетным положительным числом.")

    # 1. a = a mod n
    _, a = divide(a, n)
    t = 1
    
    while a.to_string() != zero.to_string():
        # 2. Факторизация степеней двойки из a
        while True:
            _, a_rem_2 = divide(a, two)
            if a_rem_2.to_string() != zero.to_string():
                break  # a - нечетное
            
            a, _ = divide(a, two)
            
            _, n_rem_8 = divide(n, eight)
            n_mod_8_str = n_rem_8.to_string()
            
            if n_mod_8_str == three.to_string() or n_mod_8_str == five.to_string():
                t = -t
        
        # 3. Применение закона квадратичной взаимности
        a, n = n, a
        
        _, a_rem_4 = divide(a, four)
        _, n_rem_4 = divide(n, four)

        if a_rem_4.to_string() == three.to_string() and n_rem_4.to_string() == three.to_string():
            t = -t
        
        _, a = divide(a, n)
        
    if n.to_string() == one.to_string():
        return t
    else:
        return 0
``` 