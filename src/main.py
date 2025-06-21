import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication
from presentation.main_window import CryptographicCalculatorWindow

def main():
    app = QApplication(sys.argv)
    
    # Используем nonlocal для изменения ссылки на окно в замыкании
    window = None
    
    def restart():
        nonlocal window
        
        # Создаем новое окно и показываем его
        new_window = CryptographicCalculatorWindow(restart_callback=restart)
        new_window.show()
        
        # Если старое окно существует, закрываем его
        if window:
            window.close()
        
        # Обновляем ссылку на текущее окно
        window = new_window

    # Первый запуск приложения
    restart()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 