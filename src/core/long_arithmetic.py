def _char_to_int(char: str) -> int:
    """Конвертирует символ в число."""
    if '0' <= char <= '9':
        return int(char)
    elif 'a' <= char.lower() <= 'z':
        return ord(char.lower()) - ord('a') + 10
    else:
        raise ValueError(f"Недопустимый символ в числе: {char}")

def _int_to_char(value: int) -> str:
    """Конвертирует число в символ."""
    if 0 <= value <= 9:
        return str(value)
    elif 10 <= value <= 35:
        return chr(ord('A') + value - 10)
    else:
        raise ValueError(f"Недопустимое значение для конвертации в символ: {value}")

def _remove_leading_zeros(digits):
    """Убирает ведущие нули из списка цифр."""
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return digits

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

    def to_string(self, base: int = 10) -> str:
        if not (2 <= base <= 36):
            raise ValueError("Основание системы счисления должно быть от 2 до 36.")
        
        res_str = "".join(_int_to_char(d) for d in reversed(self.digits)) if self.digits else "0"

        if self.is_negative and res_str != "0":
            return "-" + res_str
        return res_str

    def __str__(self):
        return self.to_string(10)

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

def _is_abs_greater_or_equal(num_a, num_b):
    # Сравнивает абсолютные значения
    len_a = len(num_a.digits)
    len_b = len(num_b.digits)
    if len_a != len_b:
        return len_a > len_b
    for i in range(len_a - 1, -1, -1):
        if num_a.digits[i] != num_b.digits[i]:
            return num_a.digits[i] > num_b.digits[i]
    return True

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

def subtract(num_a: LargeNumber, num_b: LargeNumber, base: int = 10) -> LargeNumber:
    neg_b = LargeNumber(num_b.to_string(base), base)
    if neg_b.to_string(base) != "0":
        neg_b.is_negative = not neg_b.is_negative
    return add(num_a, neg_b, base)

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

def power_integer(base_num: LargeNumber, exp_num: LargeNumber) -> LargeNumber:
    """
    Вычисляет base_num ^ exp_num для больших чисел.
    Использует алгоритм бинарного возведения в степень.
    """
    base = 10 # Внутренняя база для операций
    one = LargeNumber("1", base)
    two = LargeNumber("2", base)

    res = LargeNumber("1", base)
    
    b = LargeNumber(base_num.to_string(base), base)
    e = LargeNumber(exp_num.to_string(base), base)
    
    while e.to_string(base) != "0":
        _, rem = divide(e, two, base)
        if rem.to_string(base) == "1":
            res = multiply(res, b, base)
        b = multiply(b, b, base)
        e, _ = divide(e, two, base)
        
    return res

def gcd(a: LargeNumber, b: LargeNumber) -> LargeNumber:
    """Вычисляет наибольший общий делитель (НОД) для двух больших чисел."""
    base = 10
    zero = LargeNumber("0", base)
    
    while b.to_string(base) != zero.to_string(base):
        _, remainder = divide(a, b, base)
        a = b
        b = remainder
        
    return a 

def extended_gcd(a: LargeNumber, b: LargeNumber):
    """
    Расширенный алгоритм Евклида. Возвращает (d, x, y), где d = НОД(a,b) = ax + by.
    """
    base = 10
    zero = LargeNumber("0", base)
    
    a_copy = LargeNumber(a.to_string(base), base)
    b_copy = LargeNumber(b.to_string(base), base)

    if b_copy.to_string(base) == zero.to_string(base):
        return a_copy, LargeNumber("1", base), LargeNumber("0", base)

    x0, x1 = LargeNumber("1", base), LargeNumber("0", base)
    y0, y1 = LargeNumber("0", base), LargeNumber("1", base)
    
    while b_copy.to_string(base) != zero.to_string(base):
        q, r = divide(a_copy, b_copy, base)
        
        a_copy, b_copy = b_copy, r
        
        # x_new = x0 - q*x1
        x_new = subtract(x0, multiply(q, x1, base), base)
        x0, x1 = x1, x_new
        
        # y_new = y0 - q*y1
        y_new = subtract(y0, multiply(q, y1, base), base)
        y0, y1 = y1, y_new
        
    return a_copy, x0, y0 