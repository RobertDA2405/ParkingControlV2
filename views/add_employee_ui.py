from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from controllers.employee_controller import EmployeeController


class AddEmployeeUI(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Añadir Nuevo Empleado")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_input = QLineEdit()

        layout.addWidget(QLabel("Nombre de Usuario:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Rol (admin/employee):"))
        layout.addWidget(self.role_input)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_employee)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_employee(self):
        """Guardar el nuevo empleado en la base de datos."""
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.text()

        if not username or not password or not role:
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos.")
            return

        try:
            EmployeeController.add_employee(username, password, role)
            QMessageBox.information(self, "Éxito", "Empleado añadido correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al añadir empleado: {str(e)}")
