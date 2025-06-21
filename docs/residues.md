# Поиск квадратичных и кубических вычетов

Этот документ описывает алгоритмы для нахождения множеств квадратичных и кубических вычетов по заданному модулю `n`.

---

## 1. Квадратичные вычеты

Число `a` называется **квадратичным вычетом** по модулю `n`, если оно взаимно просто с `n` и сравнение `x² ≡ a (mod n)` имеет решение. Другими словами, квадратичный вычет — это число, из которого можно извлечь квадратный корень по модулю `n`.

### Алгоритм поиска

Реализованный метод является прямым и следует из определения:
1.  Создается пустое множество для хранения уникальных вычетов.
2.  Алгоритм итерируется по всем числам `i` от 1 до `n-1`.
3.  Для каждого `i` вычисляется `residue = i² mod n`.
4.  Полученное значение `residue` добавляется в множество.
5.  В конце множество преобразуется в отсортированный список.

Этот метод прост, но может быть вычислительно затратным для очень больших `n`.

### Исходный код

```python
from .long_arithmetic import (LargeNumber, add, subtract, multiply, divide, 
                                _is_abs_greater_or_equal as is_greater_or_equal)

def find_quadratic_residues(n: LargeNumber) -> list[LargeNumber]:
    """Находит все квадратичные вычеты по модулю n."""
    residues = set()
    one = LargeNumber("1")
    i = LargeNumber("1")
    
    # Итерируемся от i = 1 до n-1
    while is_greater_or_equal(subtract(n, one), i):
        # Вычисляем i^2 mod n
        i_squared = multiply(i, i)
        _, residue = divide(i_squared, n)
        residues.add(residue.to_string())
        i = add(i, one)
        
    sorted_residues = sorted(list(residues), key=lambda x: LargeNumber(x))
    return [LargeNumber(r) for r in sorted_residues]
```

---

## 2. Кубические вычеты

Аналогично, число `a` называется **кубическим вычетом** по модулю `n`, если сравнение `x³ ≡ a (mod n)` имеет решение.

### Алгоритм поиска

Алгоритм полностью аналогичен поиску квадратичных вычетов, за исключением того, что на каждом шаге вычисляется куб числа, а не квадрат.
1.  Создается пустое множество.
2.  В цикле от `i = 1` до `n-1` вычисляется `residue = i³ mod n`.
3.  Результат добавляется в множество.
4.  Возвращается отсортированный список уникальных вычетов.

### Исходный код

```python
def find_cubic_residues(n: LargeNumber) -> list[LargeNumber]:
    """Находит все кубические вычеты по модулю n."""
    residues = set()
    one = LargeNumber("1")
    three = LargeNumber("3") # Для показателя степени
    i = LargeNumber("1")
    
    while is_greater_or_equal(subtract(n, one), i):
        # Вычисляем i^3 mod n
        i_cubed = power_integer(i, three) # Используем готовую функцию возведения в степень
        _, residue = divide(i_cubed, n)
        residues.add(residue.to_string())
        i = add(i, one)
        
    sorted_residues = sorted(list(residues), key=lambda x: LargeNumber(x))
    return [LargeNumber(r) for r in sorted_residues]

```
*Примечание: В реализации для кубических вычетов предполагается использование функции `power_integer` для возведения в степень.* 