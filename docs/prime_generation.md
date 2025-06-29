# Генерация простых и псевдопростых чисел

Генерация больших простых чисел является фундаментальной задачей для многих криптографических алгоритмов, таких как RSA, DSA и других. В этом документе описаны различные методы генерации, реализованные в проекте.

---

## 1. Вероятностная генерация псевдопростых чисел

Этот метод является наиболее быстрым способом получения чисел, которые с очень высокой вероятностью являются простыми. Он не дает 100% гарантии, но для криптографических целей вероятность ошибки можно сделать пренебрежимо малой.

### Алгоритм

1.  Генерируется случайное нечетное число `p` заданной битовой длины.
2.  Это число `p` проходит через серию вероятностных тестов на простоту. В данной реализации используются два теста:
    *   **Тест Ферма**: Быстрый тест, основанный на малой теореме Ферма (`a^(p-1) ≡ 1 (mod p)`). Он отсеивает большинство составных чисел, но пропускает числа Кармайкла.
    *   **Тест Соловея-Штрассена**: Более надежный тест, основанный на критерии Эйлера и символе Якоби/Лежандра. Он не имеет аналогов чисел Кармайкла и дает более строгую оценку вероятности.
3.  Если число проходит оба теста для `k` различных случайных оснований, оно объявляется псевдопростым и возвращается. В противном случае генерируется новое случайное число.

### Исходный код

```python
import random
from .long_arithmetic import LargeNumber, add, subtract, multiply, divide
from .modular_arithmetic import mod_power, legendre_symbol

def is_fermat_prime(p, k):
    """Тест Ферма на простоту. k - количество раундов."""
    # ... (реализация теста) ...

def is_solovay_strassen_prime(p, k):
    """Тест Соловея-Штрассена на простоту. k - количество раундов."""
    # ... (реализация теста) ...

def generate_prime(bit_length, k):
    """Генерирует псевдопростое число заданной битовой длины."""
    if bit_length < 2:
        raise ValueError("Длина битов должна быть >= 2")

    while True:
        min_val = 1 << (bit_length - 1)
        max_val = (1 << bit_length) - 1
        p_int = random.randint(min_val, max_val)
        if p_int % 2 == 0:
            p_int += 1
        
        p = LargeNumber(str(p_int))
        
        # Комбинация тестов для надежности
        if is_fermat_prime(p, 5) and is_solovay_strassen_prime(p, k):
            return p 
```

---

## 2. Генерация доказуемо простых чисел (Теорема Поклингтона)

Этот метод позволяет генерировать числа, простота которых математически доказана. Он основан на теореме Поклингтона, которая дает достаточное условие простоты числа `p`, если известно частичное разложение `p-1` на простые множители.

### Алгоритм

1.  **Генерация малых простых**: Сначала генерируется набор `m` небольших, детерминистически проверенных простых чисел (например, с помощью пробных делений).
2.  **Конструирование кандидата**: Из этого набора случайным образом выбирается подмножество простых `m₁, m₂, ..., mₕ`. На их основе конструируется кандидат в простые числа: `p = 2 * m₁ * m₂ * ... * mₕ + 1`.
3.  **Проверка по Поклингтону**: Для кандидата `p` проводится тест Поклингтона. Тест заключается в поиске "свидетеля" `b` такого, что:
    *   `b^(p-1) ≡ 1 (mod p)`
    *   `НОД(b^((p-1)/mᵢ) - 1, p) = 1` для каждого простого множителя `mᵢ`.
4.  Если такой свидетель найден, то число `p` является гарантированно простым. Если нет, выбирается новое подмножество малых простых и процесс повторяется.

Этот метод полезен, когда требуется не только простое число, но и информация о разложении `p-1`.

### Исходный код

```python
def _pocklington_test(p, p_minus_1_factors, num_witnesses):
    """Тест Поклингтона на простоту."""
    # ... (реализация теста) ...

def generate_prime_with_factorization(small_primes_count, small_primes_bits, h, num_witnesses):
    """
    Генерирует простое p с известным разложением p-1.
    """
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    
    # Шаг 1: Генерируем набор малых простых
    small_primes = generate_small_primes(small_primes_count, small_primes_bits)
    
    while True:
        # Шаг 2: Выбираем подмножество
        if h > len(small_primes):
            raise ValueError("h не может быть больше количества сгенерированных малых простых.")
        factors = random.sample(small_primes, h)
        
        # Шаг 3: Конструируем p = 2 * m1 * m2 * ... * mh + 1
        p_minus_1_div_2 = LargeNumber("1", base)
        for m in factors:
            p_minus_1_div_2 = multiply(p_minus_1_div_2, m, base)
        
        p = add(multiply(two, p_minus_1_div_2, base), one, base)
        
        # Шаг 4: Проверяем по Поклингтону
        if _pocklington_test(p, factors, num_witnesses):
            return p, factors, small_primes
```

---

## 3. Генерация простых чисел по ГОСТ Р 34.10-94

Это детерминированный итеративный алгоритм, описанный в российском стандарте для цифровой подписи. Он строит простое число требуемой битовой длины `t` "снизу вверх".

### Алгоритм

1.  **Построение последовательности длин**: Создается убывающая последовательность битовых длин `t₀, t₁, ..., tₘ`, где `t₀` - целевая длина, `tᵢ ≈ tᵢ₋₁ / 2`, а последняя `tₘ` - относительно мала (например, 17-33 бит).
2.  **Генерация базового простого**: Генерируется базовое простое число `pₘ` длиной `tₘ` бит (например, методом пробных делений).
3.  **Итеративное построение**: Алгоритм итеративно строит большее простое число `pᵢ₋₁` из предыдущего `pᵢ`. На каждой итерации:
    a. Ищется такое четное число `N`, чтобы кандидат `p = N*pᵢ + 1` имел требуемую битовую длину `tᵢ₋₁`.
    b. Для кандидата `p` проводится специальная проверка на простоту из стандарта:
        *   `2^(p-1) ≡ 1 (mod p)`
        *   `2^N <binary data, 2 bytes> 1 (mod p)`
    c. Если проверка проходит, `p` становится новым `pᵢ₋₁` и процесс переходит на следующий, больший уровень. Если нет, `N` увеличивается на 2 и генерируется новый кандидат.
4.  Процесс повторяется, пока не будет сгенерировано итоговое простое число `p₀` целевой длины `t₀`.

### Исходный код

```python
def _gost_primality_test(p, N):
    """
    Выполняет проверку на простоту по двум условиям из ГОСТ Р 34.10-94.
    """
    # ... (реализация теста) ...

def generate_gost_prime(target_bit_length, progress_callback=None):
    """
    Генерирует простое число по алгоритму из ГОСТ Р 34.10-94.
    """
    base = 10
    two = LargeNumber("2", base)

    # 1. Строим убывающую последовательность битовых длин
    t_list = [target_bit_length]
    while t_list[-1] >= 34:
        t_list.append(t_list[-1] // 2)
    t_list.reverse()
    
    # 2. Генерируем базовое малое простое p_s
    ts = t_list[0]
    p_current = generate_small_primes(1, ts)[0]

    # 3. Основной цикл генерации
    for i in range(len(t_list) - 1):
        p_i = p_current
        t_next = t_list[i+1]
            
        # Находим начальное значение для N
        min_p_next = power_integer(two, LargeNumber(str(t_next - 1)))
        N, _ = divide(min_p_next, p_i)
        
        if divide(N, two)[1].to_string(base) != "0": # N должно быть четным
            N = add(N, LargeNumber("1", base))
            
        # Итеративно ищем подходящее p
        while True:
            p_next = add(multiply(p_i, N), LargeNumber("1", base))
            
            if len(p_next.to_string(2)) > t_next:
                # p перескочило битность, начинаем сначала для этого уровня
                N, _ = divide(min_p_next, p_i) 
                if divide(N, two)[1].to_string(base) != "0": N = add(N, LargeNumber("1", base))
                continue
                
            if _gost_primality_test(p_next, N):
                p_current = p_next
                break
            else:
                N = add(N, two)
                
    return p_current 
```