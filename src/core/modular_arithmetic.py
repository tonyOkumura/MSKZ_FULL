from .long_arithmetic import (LargeNumber, add, subtract, multiply, divide, 
                                _is_abs_greater_or_equal as is_greater_or_equal, 
                                power_integer, gcd)

def mod_power(base_num, exp_num, mod_num):
    base = 10
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)
    result = LargeNumber("1", base)
    _, base_val = divide(base_num, mod_num, base) 
    exp_val = LargeNumber(exp_num.to_string(base), base)
    while is_greater_or_equal(exp_val, one):
        _, remainder = divide(exp_val, two, base)
        if remainder.to_string(base) == "1":
            result = multiply(result, base_val, base)
            _, result = divide(result, mod_num, base)
        exp_val, _ = divide(exp_val, two, base)
        base_val = multiply(base_val, base_val, base)
        _, base_val = divide(base_val, mod_num, base)
    return result

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

def mod_inverse(num, mod):
    base = 10
    two = LargeNumber("2", base)
    exponent = subtract(mod, two, base)
    return mod_power(num, exponent, mod)

def modular_sqrt(c, p, q):
    base = 10
    one = LargeNumber("1", base)
    four = LargeNumber("4", base)
    n = multiply(p, q, base)
    exp_p_num = add(p, one, base)
    exp_p, _ = divide(exp_p_num, four, base)
    mp1 = mod_power(c, exp_p, p)
    mp2 = subtract(p, mp1, base)
    exp_q_num = add(q, one, base)
    exp_q, _ = divide(exp_q_num, four, base)
    mq1 = mod_power(c, exp_q, q)
    mq2 = subtract(q, mq1, base)
    q_inv_p = mod_inverse(q, p)
    p_inv_q = mod_inverse(p, q)
    term_a = multiply(q, q_inv_p, base)
    term_b = multiply(p, p_inv_q, base)
    part1_m1 = multiply(mp1, term_a, base)
    part2_m1 = multiply(mq1, term_b, base)
    sum_m1 = add(part1_m1, part2_m1, base)
    _, m1 = divide(sum_m1, n, base)
    part1_m2 = multiply(mp1, term_a, base)
    part2_m2 = multiply(mq2, term_b, base)
    sum_m2 = add(part1_m2, part2_m2, base)
    _, m2 = divide(sum_m2, n, base)
    part1_m3 = multiply(mp2, term_a, base)
    part2_m3 = multiply(mq1, term_b, base)
    sum_m3 = add(part1_m3, part2_m3, base)
    _, m3 = divide(sum_m3, n, base)
    part1_m4 = multiply(mp2, term_a, base)
    part2_m4 = multiply(mq2, term_b, base)
    sum_m4 = add(part1_m4, part2_m4, base)
    _, m4 = divide(sum_m4, n, base)
    return [m1, m2, m3, m4]

def chinese_remainder_theorem(congruences):
    base = 10
    N = LargeNumber("1", base)
    for _, n_i in congruences:
        N = multiply(N, n_i, base)
    total_sum = LargeNumber("0", base)
    for a_i, n_i in congruences:
        N_i, _ = divide(N, n_i, base)
        y_i = mod_inverse(N_i, n_i)
        term = multiply(a_i, N_i, base)
        term = multiply(term, y_i, base)
        total_sum = add(total_sum, term, base)
    _, solution = divide(total_sum, N, base)
    return solution, N

def prime_factorization(n: LargeNumber) -> list[LargeNumber]:
    """Находит уникальные простые делители числа n методом пробных делений."""
    factors = set()
    d = LargeNumber("2")
    temp_n = LargeNumber(n.to_string())
    zero = LargeNumber("0")
    one = LargeNumber("1")
    two = LargeNumber("2")

    # Обработка делителя 2
    while True:
        quotient, remainder = divide(temp_n, d)
        if remainder.to_string() == zero.to_string():
            factors.add(d.to_string())
            temp_n = quotient
        else:
            break
    
    # Обработка нечетных делителей
    d = LargeNumber("3")
    while is_greater_or_equal(temp_n, multiply(d, d)):
        quotient, remainder = divide(temp_n, d)
        if remainder.to_string() == zero.to_string():
            factors.add(d.to_string())
            temp_n = quotient
        else:
            d = add(d, two)
    
    # Если осталось число > 1, это тоже простой делитель
    if temp_n.to_string() != one.to_string():
        factors.add(temp_n.to_string())
        
    return [LargeNumber(f) for f in sorted(list(factors), key=lambda x: int(x))]

def euler_totient(m: LargeNumber) -> LargeNumber:
    """Вычисляет функцию Эйлера φ(m)."""
    one = LargeNumber("1")
    if m.to_string() == one.to_string():
        return one
    
    factors = prime_factorization(m)
    result = LargeNumber(m.to_string())
    
    for p in factors:
        p_minus_1 = subtract(p, one)
        # result = result * (p - 1) / p
        result = multiply(result, p_minus_1)
        result, _ = divide(result, p)
        
    return result

def legendre_symbol(a: LargeNumber, p: LargeNumber) -> int:
    """
    Вычисляет символ Лежандра (a/p) используя критерий Эйлера.
    p должно быть нечетным простым числом.
    Возвращает 1, -1 или 0.
    """
    zero = LargeNumber("0")
    one = LargeNumber("1")
    two = LargeNumber("2")

    # Символ Лежандра (a/p) равен 0, если a ≡ 0 (mod p).
    _, rem = divide(a, p)
    if rem.to_string() == zero.to_string():
        return 0

    # (a/p) ≡ a^((p-1)/2) (mod p)
    p_minus_1 = subtract(p, one)
    exponent, _ = divide(p_minus_1, two)
    
    result = mod_power(a, exponent, p)

    # Результат будет 1 или p-1. p-1 ≡ -1 (mod p)
    if result.to_string() == one.to_string():
        return 1
    else:
        # Если результат не 1, для простого p он должен быть p-1.
        return -1

def jacobi_symbol(a: LargeNumber, n: LargeNumber) -> int:
    """
    Вычисляет символ Якоби (a/n).
    n должно быть нечетным положительным целым числом.
    """
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

def find_quadratic_residues(n: LargeNumber) -> list[LargeNumber]:
    """Находит все квадратичные вычеты по модулю n."""
    residues = set()
    one = LargeNumber("1")
    i = LargeNumber("1")
    
    while is_greater_or_equal(subtract(n, one), i):
        # Вычисляем i^2 mod n
        i_squared = multiply(i, i)
        _, residue = divide(i_squared, n)
        residues.add(residue.to_string())
        i = add(i, one)
        
    sorted_residues = sorted(list(residues), key=lambda x: int(x))
    return [LargeNumber(r) for r in sorted_residues]

def find_cubic_residues(n: LargeNumber) -> list[LargeNumber]:
    """Находит все кубические вычеты по модулю n."""
    residues = set()
    one = LargeNumber("1")
    i = LargeNumber("1")
    
    while is_greater_or_equal(subtract(n, one), i):
        # Вычисляем i^3 mod n
        i_squared = multiply(i, i)
        i_cubed = multiply(i_squared, i)
        _, residue = divide(i_cubed, n)
        residues.add(residue.to_string())
        i = add(i, one)
        
    sorted_residues = sorted(list(residues), key=lambda x: int(x))
    return [LargeNumber(r) for r in sorted_residues] 