from PyQt6.QtWidgets import QMainWindow, QLabel

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Control - Principal")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel("¡Bienvenido al sistema de control de parqueo!", self)
        self.label.move(200, 200)
