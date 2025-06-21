import unittest
from src.core.long_arithmetic import LargeNumber
from src.core.primality import generate_prime, is_solovay_strassen_prime

class TestPrimality(unittest.TestCase):
    def test_generate_prime(self):
        """Тестирует генерацию простого числа."""
        # Просто проверяем, что функция генерирует число без ошибок
        # и оно проходит тест простоты.
        prime_candidate = generate_prime(16, 20)
        self.assertIsInstance(prime_candidate, LargeNumber)
        self.assertTrue(is_solovay_strassen_prime(prime_candidate, 20))

    def test_known_primes_and_composites(self):
        """Тестирует на известных простых и составных числах."""
        self.assertTrue(is_solovay_strassen_prime(LargeNumber("7"), 20))
        self.assertTrue(is_solovay_strassen_prime(LargeNumber("13"), 20))
        self.assertFalse(is_solovay_strassen_prime(LargeNumber("10"), 20))
        self.assertFalse(is_solovay_strassen_prime(LargeNumber("25"), 20))


if __name__ == '__main__':
    unittest.main() 