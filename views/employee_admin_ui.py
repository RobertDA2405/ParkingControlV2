from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class EmployeeAdminUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Empleados")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.welcome_label = QLabel("Bienvenido a la gestión de empleados")
        layout.addWidget(self.welcome_label)

        self.add_employee_button = QPushButton("Añadir Nuevo Empleado")
        layout.addWidget(self.add_employee_button)

        self.employee_table = QTableWidget()
        layout.addWidget(self.employee_table)

        self.employee_table.setColumnCount(2)
        self.employee_table.setHorizontalHeaderLabels(["Nombre", "Puesto"])

        self.add_employee_button.clicked.connect(self.add_employee)

        self.setLayout(layout)

    def add_employee(self):
        self.welcome_label.setText("Añadiendo un nuevo empleado...")
