import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                             QVBoxLayout, QTabWidget, QFormLayout, QLineEdit, 
                             QPushButton, QHBoxLayout, QSpinBox, QToolBar, QSizePolicy,
                             QComboBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from core.long_arithmetic import LargeNumber, add, subtract, multiply, divide, gcd, extended_gcd, _is_abs_greater_or_equal
from core.modular_arithmetic import (modular_sqrt, mod_power, 
                                     fast_modular_multiplication, 
                                     chinese_remainder_theorem, euler_totient,
                                     legendre_symbol, jacobi_symbol,
                                     find_quadratic_residues, find_cubic_residues)
from core.primality import generate_prime, generate_prime_with_factorization, generate_gost_prime, is_solovay_strassen_prime


class CryptographicCalculatorWindow(QMainWindow):
    def __init__(self, restart_callback=None):
        super().__init__()
        self.restart_callback = restart_callback
        self.setWindowTitle("Криптографический калькулятор")
        self.setGeometry(100, 100, 800, 600)

        # Главный виджет вкладок
        self.main_tabs = QTabWidget()
        self.setCentralWidget(self.main_tabs)

        # Создание и добавление основных вкладок
        self._create_classic_algorithms_tab()
        self._create_modular_arithmetic_tab()
        self._create_prime_operations_tab()
        
        self.apply_styles()

    def _create_classic_algorithms_tab(self):
        classic_tab = QWidget()
        classic_layout = QVBoxLayout(classic_tab)
        
        # Вложенный виджет вкладок для классических алгоритмов
        classic_tabs_widget = QTabWidget()
        
        # Добавляем вкладку базовой арифметики
        basic_arithmetic_tab = self._create_basic_arithmetic_tab()
        classic_tabs_widget.addTab(basic_arithmetic_tab, "Базовая арифметика")
        
        # Добавляем вкладку алгоритма Евклида
        euclidean_tab = self._create_euclidean_tab()
        classic_tabs_widget.addTab(euclidean_tab, "Алгоритм Евклида")

        classic_layout.addWidget(classic_tabs_widget)
        self.main_tabs.addTab(classic_tab, "Классические алгоритмы")

    def _create_euclidean_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)
        
        self.euclidean_a_input = QLineEdit()
        self.euclidean_b_input = QLineEdit()
        self.euclidean_result_label = QLabel("")
        calculate_button = QPushButton("Вычислить")
        calculate_button.clicked.connect(self._handle_euclidean)

        layout.addRow("Число a:", self.euclidean_a_input)
        layout.addRow("Число b:", self.euclidean_b_input)
        layout.addRow(calculate_button)
        layout.addRow("Результат:", self.euclidean_result_label)
        
        return tab

    def _handle_euclidean(self):
        try:
            a_str = self.euclidean_a_input.text()
            b_str = self.euclidean_b_input.text()
            
            if not a_str or not b_str:
                self.euclidean_result_label.setText("Ошибка: введите оба числа.")
                return

            a = LargeNumber(a_str)
            b = LargeNumber(b_str)

            # Стандартный алгоритм
            gcd_res = gcd(a, b)
            
            # Расширенный алгоритм
            d, x, y = extended_gcd(a, b)

            result_text = (
                f"НОД(a, b) = {gcd_res.to_string()}\n"
                f"Расширенный алгоритм Евклида:\n"
                f"  d = {d.to_string()}\n"
                f"  x = {x.to_string()}\n"
                f"  y = {y.to_string()}\n"
                f"Проверка: {a_str}*({x.to_string()}) + {b_str}*({y.to_string()}) = {d.to_string()}"
            )
            self.euclidean_result_label.setText(result_text)
            self.euclidean_result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        except Exception as e:
            self.euclidean_result_label.setText(f"Ошибка: {e}")

    def _create_basic_arithmetic_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        form_layout = QFormLayout()
        
        self.base_selector = QSpinBox()
        self.base_selector.setRange(2, 36)
        self.base_selector.setValue(10)
        self.base_selector.setToolTip("Выберите систему счисления (от 2 до 36)")

        self.num_a_input = QLineEdit()
        self.num_a_input.setPlaceholderText("Введите неотрицательное целое число")
        
        self.num_b_input = QLineEdit()
        self.num_b_input.setPlaceholderText("Введите неотрицательное целое число")
        
        form_layout.addRow("Система счисления:", self.base_selector)
        form_layout.addRow("Число A:", self.num_a_input)
        form_layout.addRow("Число B:", self.num_b_input)
        
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Сложить (A + B)")
        subtract_button = QPushButton("Вычесть (A - B)")
        multiply_button = QPushButton("Умножить (A * B)")
        divide_button = QPushButton("Разделить (A / B)")

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(subtract_button)
        buttons_layout.addWidget(multiply_button)
        buttons_layout.addWidget(divide_button)
        
        self.result_label = QLabel("Результат:")
        self.result_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.result_label.setWordWrap(True)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.result_label)
        
        add_button.clicked.connect(self._handle_addition)
        subtract_button.clicked.connect(self._handle_subtraction)
        multiply_button.clicked.connect(self._handle_multiplication)
        divide_button.clicked.connect(self._handle_division)
        
        return widget

    def _handle_addition(self):
        try:
            base = self.base_selector.value()
            num_a_str = self.num_a_input.text() or "0"
            num_b_str = self.num_b_input.text() or "0"

            num_a = LargeNumber(num_a_str, base)
            num_b = LargeNumber(num_b_str, base)

            result = add(num_a, num_b, base)
            self.result_label.setText(f"Результат: {result.to_string(base)}")
        except ValueError as e:
            self.result_label.setText(f"Ошибка ввода: {e}")
        except Exception as e:
            self.result_label.setText(f"Произошла ошибка: {e}")

    def _handle_subtraction(self):
        try:
            base = self.base_selector.value()
            num_a_str = self.num_a_input.text() or "0"
            num_b_str = self.num_b_input.text() or "0"

            num_a = LargeNumber(num_a_str, base)
            num_b = LargeNumber(num_b_str, base)

            result = subtract(num_a, num_b, base)
            self.result_label.setText(f"Результат: {result.to_string(base)}")
        except ValueError as e:
            self.result_label.setText(f"Ошибка ввода: {e}")
        except Exception as e:
            self.result_label.setText(f"Произошла ошибка: {e}")

    def _handle_multiplication(self):
        try:
            base = self.base_selector.value()
            num_a_str = self.num_a_input.text() or "0"
            num_b_str = self.num_b_input.text() or "0"

            num_a = LargeNumber(num_a_str, base)
            num_b = LargeNumber(num_b_str, base)

            result = multiply(num_a, num_b, base)
            self.result_label.setText(f"Результат: {result.to_string(base)}")
        except ValueError as e:
            self.result_label.setText(f"Ошибка ввода: {e}")
        except Exception as e:
            self.result_label.setText(f"Произошла ошибка: {e}")

    def _handle_division(self):
        try:
            base = self.base_selector.value()
            num_a_str = self.num_a_input.text() or "0"
            num_b_str = self.num_b_input.text() or "0"
            
            num_a = LargeNumber(num_a_str, base)
            num_b = LargeNumber(num_b_str, base)

            quotient, remainder = divide(num_a, num_b, base)
            self.result_label.setText(f"Частное: {quotient.to_string(base)}<br>Остаток: {remainder.to_string(base)}")
        except ZeroDivisionError:
            self.result_label.setText("Ошибка: Деление на ноль.")
        except ValueError as e:
            self.result_label.setText(f"Ошибка ввода: {e}")
        except Exception as e:
            self.result_label.setText(f"Произошла ошибка: {e}")

    def _create_sqrt_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()

        self.sqrt_c_input = QLineEdit()
        self.sqrt_c_input.setPlaceholderText("Введите число C (шифртекст)")
        
        self.sqrt_p_input = QLineEdit()
        self.sqrt_p_input.setPlaceholderText("Введите простое число p")
        
        self.sqrt_q_input = QLineEdit()
        self.sqrt_q_input.setPlaceholderText("Введите простое число q")

        form_layout.addRow("Число C:", self.sqrt_c_input)
        form_layout.addRow("Число p:", self.sqrt_p_input)
        form_layout.addRow("Число q:", self.sqrt_q_input)

        calculate_button = QPushButton("Вычислить корни")
        calculate_button.clicked.connect(self._handle_modular_sqrt)
        
        self.sqrt_result_label = QLabel("Результаты:")
        self.sqrt_result_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.sqrt_result_label.setWordWrap(True)

        layout.addLayout(form_layout)
        layout.addWidget(calculate_button)
        layout.addWidget(self.sqrt_result_label)

        return widget

    def _handle_modular_sqrt(self):
        try:
            c_str = self.sqrt_c_input.text()
            p_str = self.sqrt_p_input.text()
            q_str = self.sqrt_q_input.text()

            if not (c_str and p_str and q_str):
                self.sqrt_result_label.setText("Ошибка: Все поля должны быть заполнены.")
                return

            c = LargeNumber(c_str, 10)
            p = LargeNumber(p_str, 10)
            q = LargeNumber(q_str, 10)

            roots = modular_sqrt(c, p, q)
            
            result_text = "Найденные корни:<br>"
            for i, root in enumerate(roots):
                result_text += f"M<sub>{i+1}</sub> = {root.to_string(10)}<br>"

            self.sqrt_result_label.setText(result_text)

        except ValueError as e:
            self.sqrt_result_label.setText(f"Ошибка ввода: {e}")
        except Exception as e:
            self.sqrt_result_label.setText(f"Произошла ошибка: {e}")

    def _create_fast_mul_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()

        self.fast_mul_a_input = QLineEdit()
        self.fast_mul_b_input = QLineEdit()
        self.fast_mul_n_input = QLineEdit()
        self.fast_mul_c_input = QLineEdit()
        self.fast_mul_sign_combo = QComboBox()
        self.fast_mul_sign_combo.addItems(['+', '-'])

        form_layout.addRow("Число A:", self.fast_mul_a_input)
        form_layout.addRow("Число B:", self.fast_mul_b_input)
        form_layout.addRow("n (для p = 2^n ± c):", self.fast_mul_n_input)
        form_layout.addRow("c (для p = 2^n ± c):", self.fast_mul_c_input)
        form_layout.addRow("Знак (±):", self.fast_mul_sign_combo)

        calculate_button = QPushButton("Вычислить")
        calculate_button.clicked.connect(self._handle_fast_mod_mul)

        self.fast_mul_result_label = QLabel("Результат:")
        self.fast_mul_result_label.setWordWrap(True)

        layout.addLayout(form_layout)
        layout.addWidget(calculate_button)
        layout.addWidget(self.fast_mul_result_label)
        
        return widget

    def _handle_fast_mod_mul(self):
        try:
            a = LargeNumber(self.fast_mul_a_input.text())
            b = LargeNumber(self.fast_mul_b_input.text())
            n_val = LargeNumber(self.fast_mul_n_input.text())
            c_val = LargeNumber(self.fast_mul_c_input.text())
            sign = self.fast_mul_sign_combo.currentText()
            
            result, p = fast_modular_multiplication(a, b, n_val, c_val, sign)

            self.fast_mul_result_label.setText(
                f"Модуль p = {p.to_string(10)}<br>"
                f"Результат (a*b mod p): {result.to_string(10)}"
            )
        except Exception as e:
            self.fast_mul_result_label.setText(f"Ошибка: {e}")

    def _create_mod_power_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()
        
        self.mod_power_base_input = QLineEdit()
        self.mod_power_exp_input = QLineEdit()
        self.mod_power_mod_input = QLineEdit()

        form_layout.addRow("Основание:", self.mod_power_base_input)
        form_layout.addRow("Показатель:", self.mod_power_exp_input)
        form_layout.addRow("Модуль:", self.mod_power_mod_input)

        calculate_button = QPushButton("Вычислить")
        calculate_button.clicked.connect(self._handle_mod_power)
        
        self.mod_power_result_label = QLabel("Результат:")
        self.mod_power_result_label.setWordWrap(True)

        layout.addLayout(form_layout)
        layout.addWidget(calculate_button)
        layout.addWidget(self.mod_power_result_label)
        
        return widget

    def _handle_mod_power(self):
        try:
            base_num = LargeNumber(self.mod_power_base_input.text())
            exp_num = LargeNumber(self.mod_power_exp_input.text())
            mod_num = LargeNumber(self.mod_power_mod_input.text())

            result = mod_power(base_num, exp_num, mod_num)
            self.mod_power_result_label.setText(f"Результат: {result.to_string(10)}")
        except Exception as e:
            self.mod_power_result_label.setText(f"Ошибка: {e}")

    def _create_crt_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        info_label = QLabel(
            "Введите систему сравнений. Каждое сравнение вида 'a, n' "
            "(где x ≡ a mod n) в новой строке.\n"
            "Модули 'n' должны быть попарно взаимно простыми."
        )
        info_label.setWordWrap(True)

        self.crt_input_text = QTextEdit()
        self.crt_input_text.setPlaceholderText("Пример:\n2, 3\n3, 5\n2, 7")

        calculate_button = QPushButton("Решить систему")
        calculate_button.clicked.connect(self._handle_crt_solve)

        self.crt_result_label = QLabel("Результат:")
        self.crt_result_label.setWordWrap(True)
        
        layout.addWidget(info_label)
        layout.addWidget(self.crt_input_text)
        layout.addWidget(calculate_button)
        layout.addWidget(self.crt_result_label)

        return widget

    def _handle_crt_solve(self):
        try:
            lines = self.crt_input_text.toPlainText().strip().split('\n')
            if not lines or not lines[0]:
                self.crt_result_label.setText("Ошибка: Поле ввода пусто.")
                return

            congruences = []
            for line in lines:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) != 2:
                    raise ValueError(f"Неверный формат строки: '{line}'. Ожидается 'a, n'.")
                
                a_str, n_str = parts
                if not a_str.isdigit() or not n_str.isdigit():
                    raise ValueError(f"Неверный формат строки: '{line}'. 'a' и 'n' должны быть числами.")

                congruences.append(
                    (LargeNumber(a_str), LargeNumber(n_str))
                )

            if len(congruences) < 2:
                self.crt_result_label.setText("Ошибка: Необходимо как минимум два сравнения.")
                return

            solution, N = chinese_remainder_theorem(congruences)

            self.crt_result_label.setText(
                f"Общий модуль N = {N.to_string(10)}\n\n"
                f"Решение: x ≡ {solution.to_string(10)} (mod {N.to_string(10)})"
            )

        except ValueError as e:
            self.crt_result_label.setText(f"Ошибка ввода: {e}")
        except Exception as e:
            self.crt_result_label.setText(f"Произошла ошибка: {e}")

    def _create_prime_gen_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        form_layout = QFormLayout()

        self.prime_bit_length_input = QSpinBox()
        self.prime_bit_length_input.setRange(8, 512)
        self.prime_bit_length_input.setValue(64)

        self.prime_rounds_input = QSpinBox()
        self.prime_rounds_input.setRange(1, 100)
        self.prime_rounds_input.setValue(20)

        form_layout.addRow("Битовая длина:", self.prime_bit_length_input)
        form_layout.addRow("Раунды проверки (k):", self.prime_rounds_input)

        generate_button = QPushButton("Сгенерировать")
        generate_button.clicked.connect(self._handle_generate_prime)

        self.prime_result_label = QLabel("Результат:")
        self.prime_result_label.setWordWrap(True)
        self.prime_result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addLayout(form_layout)
        layout.addWidget(generate_button)
        layout.addWidget(self.prime_result_label)

        return widget

    def _handle_generate_prime(self):
        try:
            bit_length = self.prime_bit_length_input.value()
            k = self.prime_rounds_input.value()

            self.prime_result_label.setText("Идёт генерация, пожалуйста, подождите...")
            QApplication.processEvents() # Обновляем UI

            prime = generate_prime(bit_length, k)
            
            self.prime_result_label.setText(
                f"Сгенерировано псевдопростое число ({bit_length} бит):\n"
                f"{prime.to_string(10)}"
            )

        except Exception as e:
            self.prime_result_label.setText(f"Произошла ошибка: {e}")

    def _create_det_prime_gen_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        form_layout = QFormLayout()

        self.det_prime_k_input = QSpinBox()
        self.det_prime_k_input.setRange(5, 100)
        self.det_prime_k_input.setValue(10)
        self.det_prime_k_input.setToolTip("Кол-во малых простых для генерации (k)")

        self.det_prime_bits_input = QSpinBox()
        self.det_prime_bits_input.setRange(8, 32)
        self.det_prime_bits_input.setValue(16)
        self.det_prime_bits_input.setToolTip("Битовая длина малых простых")

        self.det_prime_h_input = QSpinBox()
        self.det_prime_h_input.setRange(2, 100)
        self.det_prime_h_input.setValue(3)
        self.det_prime_h_input.setToolTip("Кол-во сомножителей для p-1 (h)")
        
        self.det_prime_witness_input = QSpinBox()
        self.det_prime_witness_input.setRange(1, 100)
        self.det_prime_witness_input.setValue(5)
        self.det_prime_witness_input.setToolTip("Кол-во свидетелей для теста")

        form_layout.addRow("Кол-во малых простых (k):", self.det_prime_k_input)
        form_layout.addRow("Бит. длина малых простых:", self.det_prime_bits_input)
        form_layout.addRow("Кол-во сомножителей (h):", self.det_prime_h_input)
        form_layout.addRow("Кол-во свидетелей:", self.det_prime_witness_input)

        generate_button = QPushButton("Сгенерировать")
        generate_button.clicked.connect(self._handle_det_generate_prime)

        self.det_prime_result_label = QLabel("Результат:")
        self.det_prime_result_label.setWordWrap(True)
        self.det_prime_result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addLayout(form_layout)
        layout.addWidget(generate_button)
        layout.addWidget(self.det_prime_result_label)

        return widget

    def _handle_det_generate_prime(self):
        try:
            k = self.det_prime_k_input.value()
            bits = self.det_prime_bits_input.value()
            h = self.det_prime_h_input.value()
            witnesses = self.det_prime_witness_input.value()

            self.det_prime_result_label.setText("Идёт генерация, это может занять время...")
            QApplication.processEvents()

            p, factors, small_primes = generate_prime_with_factorization(k, bits, h, witnesses)

            factors_str = ", ".join(f.to_string(10) for f in factors)
            small_primes_str = ", ".join(sp.to_string(10) for sp in small_primes)

            result_text = (
                f"<b>Сгенерированное простое число p:</b><br>{p.to_string(10)}<br><br>"
                f"<b>Разложение p-1:</b><br>p-1 = 2 * {factors_str}<br><br>"
                f"<b>Исходный набор малых простых:</b><br>{small_primes_str}"
            )
            self.det_prime_result_label.setText(result_text)

        except Exception as e:
            self.det_prime_result_label.setText(f"Произошла ошибка: {e}")

    def _create_gost_prime_gen_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        form_layout = QFormLayout()

        self.gost_bit_length_input = QSpinBox()
        self.gost_bit_length_input.setRange(17, 1024)
        self.gost_bit_length_input.setValue(128)
        self.gost_bit_length_input.setToolTip("Целевая битовая длина (>= 17)")

        form_layout.addRow("Битовая длина:", self.gost_bit_length_input)
        
        generate_button = QPushButton("Сгенерировать")
        generate_button.clicked.connect(self._handle_gost_generate_prime)

        self.gost_result_text = QTextEdit()
        self.gost_result_text.setReadOnly(True)
        self.gost_result_text.setPlaceholderText("Здесь будет отображаться процесс генерации и результат...")

        layout.addLayout(form_layout)
        layout.addWidget(generate_button)
        layout.addWidget(self.gost_result_text)

        return widget

    def _handle_gost_generate_prime(self):
        try:
            bit_length = self.gost_bit_length_input.value()
            
            self.gost_result_text.clear()
            self.gost_result_text.append("Начало генерации по ГОСТ Р 34.10-94...")
            QApplication.processEvents()

            def progress_update(message, is_sub_step=False):
                if not is_sub_step:
                    self.gost_result_text.append(message)
                QApplication.processEvents()
            
            prime = generate_gost_prime(bit_length, progress_callback=progress_update)
            
            self.gost_result_text.append(f"\n<b>Успех! Сгенерированное простое число ({bit_length} бит):</b>")
            self.gost_result_text.append(prime.to_string(10))

        except Exception as e:
            self.gost_result_text.append(f"\nПроизошла ошибка: {e}") 

    def _create_modular_arithmetic_tab(self):
        modular_tab = QWidget()
        modular_layout = QVBoxLayout(modular_tab)
        
        modular_tabs_widget = QTabWidget()
        
        modular_tabs_widget.addTab(self._create_mod_power_tab(), "Возведение в степень")
        modular_tabs_widget.addTab(self._create_fast_mul_tab(), "Ускоренное умножение")
        modular_tabs_widget.addTab(self._create_crt_tab(), "Системы сравнений (КТО)")
        modular_tabs_widget.addTab(self._create_euler_tab(), "Функция Эйлера")
        modular_tabs_widget.addTab(self._create_legendre_jacobi_tab(), "Символы Лежандра/Якоби")
        modular_tabs_widget.addTab(self._create_residue_finder_tab(), "Поиск вычетов")

        modular_layout.addWidget(modular_tabs_widget)
        self.main_tabs.addTab(modular_tab, "Модульная арифметика")
    
    def _create_prime_operations_tab(self):
        prime_tab = QWidget()
        prime_layout = QVBoxLayout(prime_tab)
        
        prime_tabs_widget = QTabWidget()
        
        prime_tabs_widget.addTab(self._create_sqrt_tab(), "Извлечение корня")
        prime_tabs_widget.addTab(self._create_prime_gen_tab(), "Генерация псевдопростых")
        prime_tabs_widget.addTab(self._create_det_prime_gen_tab(), "Детерминистическая (p-1)")
        prime_tabs_widget.addTab(self._create_gost_prime_gen_tab(), "Детерминистическая (ГОСТ)")

        prime_layout.addWidget(prime_tabs_widget)
        self.main_tabs.addTab(prime_tab, "Операции с простыми числами")

    def _create_euler_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        form_layout = QFormLayout()

        self.euler_m_input = QLineEdit()
        self.euler_m_input.setPlaceholderText("Введите натуральное число m")
        
        form_layout.addRow("Число m:", self.euler_m_input)

        calculate_button = QPushButton("Вычислить φ(m)")
        calculate_button.clicked.connect(self._handle_euler_totient)
        
        self.euler_result_label = QLabel("Результат:")
        self.euler_result_label.setWordWrap(True)
        self.euler_result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addLayout(form_layout)
        layout.addWidget(calculate_button)
        layout.addWidget(self.euler_result_label)
        
        return widget

    def _handle_euler_totient(self):
        try:
            m_str = self.euler_m_input.text()
            if not m_str:
                self.euler_result_label.setText("Ошибка: введите число m.")
                return

            m = LargeNumber(m_str)
            if m.is_negative or m.to_string() == "0":
                self.euler_result_label.setText("Ошибка: число m должно быть натуральным ( > 0).")
                return

            self.euler_result_label.setText("Вычисление... Это может занять время для больших чисел.")
            QApplication.processEvents()

            result = euler_totient(m)
            
            self.euler_result_label.setText(f"φ({m_str}) = {result.to_string()}")

        except Exception as e:
            self.euler_result_label.setText(f"Произошла ошибка: {e}")

    def _create_legendre_jacobi_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout = QFormLayout()

        self.lj_a_input = QLineEdit()
        self.lj_a_input.setPlaceholderText("Введите целое число a")
        self.lj_n_input = QLineEdit()
        self.lj_n_input.setPlaceholderText("Введите простое p или нечетное n > 1")
        
        form_layout.addRow("Число a:", self.lj_a_input)
        form_layout.addRow("Число p (или n):", self.lj_n_input)

        calculate_button = QPushButton("Вычислить")
        calculate_button.clicked.connect(self._handle_legendre_jacobi)
        
        self.lj_result_label = QLabel("Результат:")
        self.lj_result_label.setWordWrap(True)
        self.lj_result_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addLayout(form_layout)
        layout.addWidget(calculate_button)
        layout.addWidget(self.lj_result_label)
        
        return widget

    def _handle_legendre_jacobi(self):
        try:
            a_str = self.lj_a_input.text()
            n_str = self.lj_n_input.text()

            if not a_str or not n_str:
                self.lj_result_label.setText("Ошибка: введите оба числа.")
                return

            a = LargeNumber(a_str)
            n = LargeNumber(n_str)
            
            one = LargeNumber("1")
            two = LargeNumber("2")
            _, n_rem_2 = divide(n, two)
            is_n_odd = n_rem_2.to_string() != "0"

            if not _is_abs_greater_or_equal(n, one):
                self.lj_result_label.setText("Ошибка: n должно быть > 0.")
                return
            
            result_text = ""
            
            # Проверка на простоту (вероятностная)
            is_n_prime = is_solovay_strassen_prime(n, k=20)
            
            if is_n_prime:
                result_text += f"Число {n_str} вероятно простое.\n"
                l_symbol = 0
                if n.to_string() == "2":
                    # (a/2) = 0 если a четное, 1 если a нечетное
                    _, a_rem_2 = divide(a, two)
                    l_symbol = 0 if a_rem_2.to_string() == "0" else 1
                else: # n - нечетное простое
                    l_symbol = legendre_symbol(a, n)
                result_text += f"Символ Лежандра ({a_str}/{n_str}) = {l_symbol}\n\n"
            
            # Символ Якоби определен для нечетных n > 1
            if is_n_odd and _is_abs_greater_or_equal(n, one):
                j_symbol = jacobi_symbol(a, n)
                result_text += f"Символ Якоби ({a_str}/{n_str}) = {j_symbol}\n"
            elif not is_n_odd and n.to_string() != "2":
                 result_text += "Символ Якоби не определён для четных составных n."

            self.lj_result_label.setText(result_text.strip())

        except ValueError as ve:
            self.lj_result_label.setText(f"Ошибка ввода: {ve}")
        except Exception as e:
            self.lj_result_label.setText(f"Произошла ошибка: {e}")

    def _create_residue_finder_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        form_layout = QFormLayout()

        self.residue_n_input = QLineEdit()
        self.residue_n_input.setPlaceholderText("Введите модуль n > 1")
        
        self.residue_type_combo = QComboBox()
        self.residue_type_combo.addItems(["Квадратичные", "Кубические"])

        form_layout.addRow("Модуль n:", self.residue_n_input)
        form_layout.addRow("Тип вычета:", self.residue_type_combo)

        calculate_button = QPushButton("Найти вычеты")
        calculate_button.clicked.connect(self._handle_find_residues)
        
        self.residue_result_text = QTextEdit()
        self.residue_result_text.setReadOnly(True)
        self.residue_result_text.setPlaceholderText("Здесь будет список вычетов...")

        layout.addLayout(form_layout)
        layout.addWidget(calculate_button)
        layout.addWidget(self.residue_result_text)
        
        return widget

    def _handle_find_residues(self):
        try:
            n_str = self.residue_n_input.text()
            if not n_str:
                self.residue_result_text.setText("Ошибка: введите модуль n.")
                return

            n = LargeNumber(n_str)
            if not _is_abs_greater_or_equal(n, LargeNumber("2")):
                self.residue_result_text.setText("Ошибка: модуль n должен быть больше 1.")
                return
            
            self.residue_result_text.setText("Вычисление... Это может занять время для больших n.")
            QApplication.processEvents()

            residue_type = self.residue_type_combo.currentText()
            residues = []
            if residue_type == "Квадратичные":
                residues = find_quadratic_residues(n)
            else: # Кубические
                residues = find_cubic_residues(n)
            
            result_str = f"Найдено {len(residues)} {residue_type.lower()} вычетов по модулю {n_str}:\n\n"
            result_str += ", ".join([r.to_string() for r in residues])
            self.residue_result_text.setText(result_str)

        except Exception as e:
            self.residue_result_text.setText(f"Произошла ошибка: {e}")

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QLabel { font-size: 14px; color: #333; }
            QLineEdit, QSpinBox, QComboBox, QTextEdit {
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 14px;
                border-radius: 3px;
                background-color: white;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 3px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #005a9e; }
            QTabWidget::pane {
                border: 1px solid #c4c4c4;
                border-top: none;
                background: white;
            }
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 1px solid #c4c4c4;
                border-bottom-color: #c2c2c2;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 10px 25px;
                font-size: 15px;
                font-weight: bold;
                color: #333;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }
            QTabBar::tab:selected {
                border-color: #9B9B9B;
                border-bottom-color: #fafafa;
            }
            QTabBar::tab:!selected {
                margin-top: 2px; 
            }
        """)