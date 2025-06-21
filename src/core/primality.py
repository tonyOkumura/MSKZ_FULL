import math
import random
from .long_arithmetic import LargeNumber, add, subtract, multiply, divide, power_integer, gcd
from .modular_arithmetic import mod_power

def legendre_symbol(a, p):
    """
    Вычисляет символ Лежандра (a/p) используя критерий Эйлера.
    Возвращает 1, -1 или 0.
    """
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    
    p_minus_1 = subtract(p, one, base)
    exponent, _ = divide(p_minus_1, two, base)
    
    result_large_num = mod_power(a, exponent, p)
    
    if result_large_num.to_string(base) == "1":
        return 1
    elif result_large_num.to_string(base) == subtract(p, one, base).to_string(base):
        return -1
    else:
        return 0

def is_fermat_prime(p, k):
    """Тест Ферма на простоту. k - количество раундов."""
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    p_minus_1 = subtract(p, one, base)
    
    for _ in range(k):
        p_minus_2_str = subtract(p, two, base).to_string(base)
        if int(p_minus_2_str) < 2: return True
        b_str = str(random.randint(2, int(p_minus_2_str)))
        b = LargeNumber(b_str, base)
        
        if mod_power(b, p_minus_1, p).to_string(base) != "1":
            return False
    return True

def is_solovay_strassen_prime(p, k):
    """Тест Соловея-Штрассена на простоту. k - количество раундов."""
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    p_minus_1 = subtract(p, one, base)
    exponent, _ = divide(p_minus_1, two, base)

    for _ in range(k):
        p_minus_1_int = int(p_minus_1.to_string(base))
        if p_minus_1_int < 2: return True
        
        b_str = str(random.randint(2, p_minus_1_int))
        b = LargeNumber(b_str, base)
        
        r = mod_power(b, exponent, p)
        
        if r.to_string(base) != "1" and r.to_string(base) != p_minus_1.to_string(base):
            return False
            
        s = legendre_symbol(b, p)
        
        if s == 1:
            s_large = LargeNumber("1", base)
        else:
            s_large = subtract(p, one, base)
        
        if r.to_string(base) != s_large.to_string(base):
            return False
    
    return True

def is_prime_trial_division(n_large):
    """
    Детерминистический тест на простоту методом пробных делений.
    Эффективен только для относительно небольших чисел.
    """
    n_str = n_large.to_string(10)
    if not n_str.isdigit() or len(n_str) > 18: # Ограничение для int
        raise ValueError("Метод пробных делений применим только для чисел до 10^18")
    
    n = int(n_str)
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    
    limit = math.isqrt(n)
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def generate_small_primes(count, bit_length):
    """Генерирует список детерминистически проверенных малых простых чисел."""
    primes = []
    while len(primes) < count:
        min_val = 1 << (bit_length - 1)
        max_val = (1 << bit_length) - 1
        candidate_int = random.randint(min_val, max_val)
        if candidate_int % 2 == 0:
            candidate_int += 1
            
        candidate_large = LargeNumber(str(candidate_int))
        if is_prime_trial_division(candidate_large):
            primes.append(candidate_large)
    return primes

def _pocklington_test(p, p_minus_1_factors, num_witnesses):
    """Тест Поклингтона на простоту."""
    base = 10
    one = LargeNumber("1", base)
    p_minus_1, _ = divide(p, one, base)
    p_minus_1 = subtract(p, one, base)
    
    for _ in range(num_witnesses):
        b = LargeNumber(str(random.randint(2, int(p.to_string(10)) - 2)))
        
        # 1) b^(p-1) === 1 (mod p)
        if mod_power(b, p_minus_1, p).to_string(base) != "1":
            continue # Пробуем другого свидетеля
            
        # 2) gcd(b^((p-1)/mi) - 1, p) = 1 для всех mi
        all_factors_pass = True
        for factor in p_minus_1_factors:
            exponent, _ = divide(p_minus_1, factor, base)
            term = mod_power(b, exponent, p)
            term_minus_1 = subtract(term, one, base)
            
            if gcd(term_minus_1, p).to_string(base) != "1":
                all_factors_pass = False
                break
        
        if all_factors_pass:
            return True # p - простое
            
    return False

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
        
        if is_fermat_prime(p, 5) and is_solovay_strassen_prime(p, k):
            return p 

def _gost_primality_test(p, N):
    """
    Выполняет проверку на простоту по двум условиям из ГОСТ Р 34.10-94.
    p = N*q+1. Тест проверяет: 2^(p-1)==1 mod p И 2^N != 1 mod p.
    """
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    
    p_minus_1 = subtract(p, one, base)
    
    # Условие 1: 2^(p-1) mod p == 1
    if mod_power(two, p_minus_1, p).to_string(base) != "1":
        return False

    # Условие 2: 2^N mod p != 1
    if mod_power(two, N, p).to_string(base) == "1":
        return False
        
    return True

def generate_gost_prime(target_bit_length, progress_callback=None):
    """
    Генерирует простое число по алгоритму из ГОСТ Р 34.10-94.
    """
    base = 10
    two = LargeNumber("2", base)

    if target_bit_length < 17:
        raise ValueError("Целевая битовая длина должна быть >= 17.")

    # 1. Строим убывающую последовательность битовых длин
    t_list = [target_bit_length]
    while t_list[-1] >= 34: # t/2 должно быть хотя бы 17
        t_list.append(t_list[-1] // 2)
    t_list.reverse()
    
    # 2. Генерируем базовое малое простое p_s
    ts = t_list[0]
    if progress_callback: progress_callback(f"Шаг 1: Генерация базового простого числа ({ts} бит)...")
        
    p_current = generate_small_primes(1, ts)[0]

    if progress_callback: progress_callback(f"Базовое простое: {p_current.to_string(10)}")

    # 3. Основной цикл генерации: от p_s до p_0
    for i in range(len(t_list) - 1):
        p_i = p_current
        t_next = t_list[i+1]
        
        if progress_callback: progress_callback(f"\nШаг {i+2}: Генерация {t_next}-битного простого...")
            
        # Находим начальное значение для N
        min_p_next = power_integer(two, LargeNumber(str(t_next - 1)))
        N, _ = divide(min_p_next, p_i)
        
        if divide(N, two)[1].to_string(base) != "0": # N должно быть четным
            N = add(N, LargeNumber("1", base))
            
        # Итеративно ищем подходящее p_{i-1}
        while True:
            p_next = add(multiply(p_i, N), LargeNumber("1", base))
            
            if len(p_next.to_string(2)) > t_next:
                N = add(N, two) # N слишком велико, p перескочило битность
                continue

            if progress_callback: progress_callback(f"Проверка кандидата N={N.to_string(10)}...", is_sub_step=True)

            if _gost_primality_test(p_next, N):
                p_current = p_next
                if progress_callback: progress_callback(f"Найден промежуточный простой: {p_current.to_string(10)}")
                break
            else:
                N = add(N, two)

    if progress_callback: progress_callback("\nГенерация завершена.")
        
    return p_current 