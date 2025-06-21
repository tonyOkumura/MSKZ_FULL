import unittest

from src.core.long_arithmetic import LargeNumber
from src.core.modular_arithmetic import (
    modular_sqrt, mod_power, fast_modular_multiplication, chinese_remainder_theorem,
    euler_totient, legendre_symbol, jacobi_symbol, 
    find_quadratic_residues, find_cubic_residues
)

class TestModularArithmetic(unittest.TestCase):
    def test_modular_sqrt_example(self):
        """Тестирует извлечение квадратного корня."""
        c = LargeNumber("23")
        p = LargeNumber("7")
        q = LargeNumber("11")
        expected_roots_str = {"10", "32", "45", "67"}
        calculated_roots = modular_sqrt(c, p, q)
        calculated_roots_str = {root.to_string(10) for root in calculated_roots}
        self.assertEqual(expected_roots_str, calculated_roots_str)

    def test_mod_power(self):
        """Тестирует возведение в степень по модулю."""
        base = LargeNumber("3")
        exp = LargeNumber("4")
        mod = LargeNumber("5")
        result = mod_power(base, exp, mod)
        self.assertEqual(result.to_string(10), "1")

    def test_fast_modular_multiplication(self):
        """Тестирует ускоренное умножение по модулю."""
        a1 = LargeNumber("5")
        b1 = LargeNumber("6")
        n1 = LargeNumber("4")
        c1 = LargeNumber("3")
        result1, p1 = fast_modular_multiplication(a1, b1, n1, c1, '+')
        self.assertEqual(p1.to_string(10), "19")
        self.assertEqual(result1.to_string(10), "11")

        a2 = LargeNumber("7")
        b2 = LargeNumber("8")
        n2 = LargeNumber("5")
        c2 = LargeNumber("3")
        result2, p2 = fast_modular_multiplication(a2, b2, n2, c2, '-')
        self.assertEqual(p2.to_string(10), "29")
        self.assertEqual(result2.to_string(10), "27")

    def test_chinese_remainder_theorem(self):
        """Тестирует Китайскую теорему об остатках."""
        congruences = [
            (LargeNumber("2"), LargeNumber("3")),
            (LargeNumber("3"), LargeNumber("5")),
            (LargeNumber("2"), LargeNumber("7"))
        ]
        solution, N = chinese_remainder_theorem(congruences)
        self.assertEqual(N.to_string(10), "105")
        self.assertEqual(solution.to_string(10), "23")

    def test_euler_totient(self):
        # φ(1) = 1
        self.assertEqual(euler_totient(LargeNumber("1")).to_string(), "1")
        # φ(p) = p-1 for prime p
        self.assertEqual(euler_totient(LargeNumber("13")).to_string(), "12")
        # φ(p^k) = p^k - p^(k-1) -> φ(9) = 9 - 3 = 6
        self.assertEqual(euler_totient(LargeNumber("9")).to_string(), "6")
        # φ(mn) = φ(m)φ(n) for gcd(m,n)=1 -> φ(10) = φ(2)φ(5) = 1*4 = 4
        self.assertEqual(euler_totient(LargeNumber("10")).to_string(), "4")
        self.assertEqual(euler_totient(LargeNumber("99")).to_string(), "60") # φ(9)*φ(11) = 6*10

    def test_legendre_symbol(self):
        # (2/7) = 1, т.к. 2 = 3^2 (mod 7) = 9 (mod 7) = 2
        self.assertEqual(legendre_symbol(LargeNumber("2"), LargeNumber("7")), 1)
        # (3/7) = -1
        self.assertEqual(legendre_symbol(LargeNumber("3"), LargeNumber("7")), -1)
        # (a/p) = 0 if a divisible by p
        self.assertEqual(legendre_symbol(LargeNumber("14"), LargeNumber("7")), 0)
    
    def test_jacobi_symbol(self):
        # (1001/9907), 9907 is prime -> same as legendre
        self.assertEqual(jacobi_symbol(LargeNumber("1001"), LargeNumber("9907")), -1)
        # (15/77) = (15/7)(15/11) = (1/7)(4/11) = 1 * 1 = 1
        self.assertEqual(jacobi_symbol(LargeNumber("15"), LargeNumber("77")), 1)
        # (a/n) = 0 if gcd(a,n) != 1
        self.assertEqual(jacobi_symbol(LargeNumber("21"), LargeNumber("77")), 0)
        with self.assertRaises(ValueError):
            jacobi_symbol(LargeNumber("5"), LargeNumber("10")) # n must be odd

    def test_quadratic_residues(self):
        # Вычеты по модулю 10: 1^2=1, 2^2=4, 3^2=9, 4^2=16=6, 5^2=25=5
        residues = find_quadratic_residues(LargeNumber("10"))
        self.assertEqual([r.to_string() for r in residues], ["1", "4", "5", "6", "9"])

    def test_cubic_residues(self):
        # Вычеты по модулю 7: 1^3=1, 2^3=8=1, 3^3=27=6, 4^3=64=1, 5^3=125=6, 6^3=216=6
        residues = find_cubic_residues(LargeNumber("7"))
        self.assertEqual([r.to_string() for r in residues], ["1", "6"])

if __name__ == '__main__':
    unittest.main() 