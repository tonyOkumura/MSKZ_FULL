import unittest

from src.core.long_arithmetic import (LargeNumber, add, subtract, multiply, 
                                      divide, gcd, extended_gcd, _is_abs_greater_or_equal)

class TestLongArithmetic(unittest.TestCase):

    def test_signed_init_and_to_string(self):
        self.assertEqual(LargeNumber("-123").to_string(10), "-123")
        self.assertFalse(LargeNumber("123").is_negative)
        self.assertTrue(LargeNumber("-123").is_negative)
        self.assertFalse(LargeNumber("-0").is_negative)
        self.assertEqual(LargeNumber("-0").to_string(10), "0")

    def test_addition(self):
        # Base 10
        num1 = LargeNumber("123")
        num2 = LargeNumber("456")
        result = add(num1, num2, 10)
        self.assertEqual(result.to_string(10), "579")

        # Base 16 (Hex)
        num1_hex = LargeNumber("A", 16)
        num2_hex = LargeNumber("B", 16)
        result_hex = add(num1_hex, num2_hex, 16)
        self.assertEqual(result_hex.to_string(16), "15")

        # Новые тесты для знаков
        self.assertEqual(add(LargeNumber("-10"), LargeNumber("-20")).to_string(10), "-30")
        self.assertEqual(add(LargeNumber("30"), LargeNumber("-10")).to_string(10), "20")
        self.assertEqual(add(LargeNumber("10"), LargeNumber("-30")).to_string(10), "-20")
        self.assertEqual(add(LargeNumber("-10"), LargeNumber("30")).to_string(10), "20")

    def test_subtraction(self):
        # Base 10
        num1 = LargeNumber("579")
        num2 = LargeNumber("123")
        result = subtract(num1, num2, 10)
        self.assertEqual(result.to_string(10), "456")

        # Base 2 (Binary)
        num1_bin = LargeNumber("1101", 2) # 13
        num2_bin = LargeNumber("101", 2)  # 5
        result_bin = subtract(num1_bin, num2_bin, 2) # 8
        self.assertEqual(result_bin.to_string(2), "1000")

        # Новые тесты для знаков
        self.assertEqual(subtract(LargeNumber("10"), LargeNumber("20")).to_string(10), "-10")
        self.assertEqual(subtract(LargeNumber("-10"), LargeNumber("20")).to_string(10), "-30")
        self.assertEqual(subtract(LargeNumber("10"), LargeNumber("-20")).to_string(10), "30")

    def test_multiplication(self):
        # Base 10
        num1 = LargeNumber("12")
        num2 = LargeNumber("10")
        result = multiply(num1, num2, 10)
        self.assertEqual(result.to_string(10), "120")
        
        # Base 16 (Hex)
        num1_hex = LargeNumber("F", 16) # 15
        num2_hex = LargeNumber("F", 16) # 15
        result_hex = multiply(num1_hex, num2_hex, 16) # 225
        self.assertEqual(result_hex.to_string(16), "E1")

        # Новые тесты для знаков
        self.assertEqual(multiply(LargeNumber("-12"), LargeNumber("10")).to_string(10), "-120")
        self.assertEqual(multiply(LargeNumber("12"), LargeNumber("-10")).to_string(10), "-120")
        self.assertEqual(multiply(LargeNumber("-12"), LargeNumber("-10")).to_string(10), "120")
        self.assertEqual(multiply(LargeNumber("0"), LargeNumber("-10")).to_string(10), "0")

    def test_division(self):
        # Base 10
        num1 = LargeNumber("123")
        num2 = LargeNumber("10")
        quotient, remainder = divide(num1, num2, 10)
        self.assertEqual(quotient.to_string(10), "12")
        self.assertEqual(remainder.to_string(10), "3")

        # Новые тесты для знаков
        q, r = divide(LargeNumber("-123"), LargeNumber("10"))
        self.assertEqual(q.to_string(10), "-12")
        self.assertEqual(r.to_string(10), "-3")

        q, r = divide(LargeNumber("123"), LargeNumber("-10"))
        self.assertEqual(q.to_string(10), "-12")
        self.assertEqual(r.to_string(10), "3")

    def test_is_abs_greater_or_equal(self):
        self.assertTrue(_is_abs_greater_or_equal(LargeNumber("100"), LargeNumber("10")))
        self.assertTrue(_is_abs_greater_or_equal(LargeNumber("10"), LargeNumber("10")))
        self.assertFalse(_is_abs_greater_or_equal(LargeNumber("10"), LargeNumber("100")))

    def test_extended_gcd(self):
        """Тестирует расширенный алгоритм Евклида."""
        a = LargeNumber("99")
        b = LargeNumber("78")
        
        d, x, y = extended_gcd(a, b)
        
        # d = НОД(99, 78) = 3
        self.assertEqual(d.to_string(10), "3")
        
        # Проверяем тождество Безу: ax + by = d
        ax = multiply(a, x)
        by = multiply(b, y)
        d_check = add(ax, by)
        self.assertEqual(d_check.to_string(10), d.to_string(10))

if __name__ == '__main__':
    unittest.main() 