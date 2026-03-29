import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow  # Тот самый "чистый" файл с логикой

def main():
    # 1. Создаем само приложение (движок Qt)
    app = QApplication(sys.argv)

    # 2. Создаем твое окно (которое само внутри подтянет дизайн и кнопки)
    window = MainWindow()
    window.show()

    # 3. Запускаем цикл обработки событий (чтобы окно не закрылось сразу)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()