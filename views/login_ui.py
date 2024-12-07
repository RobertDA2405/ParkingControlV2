from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from views.admin_ui import AdminUI
from views.employee_ui import EmployeeUI
from controllers.auth_controller import AuthController


class LoginUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Iniciar Sesión")
        self.message_label = QLabel()

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.message_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        success, user_role = AuthController.login(username, password)

        if success:
            self.message_label.setText("Login exitoso")
            self.message_label.setStyleSheet("color: green;")
            
            self.close()

            if user_role == "admin":
                self.open_admin_ui()
            elif user_role == "employee":
                self.open_employee_ui()
            else:
                self.message_label.setText("Rol desconocido")
                self.message_label.setStyleSheet("color: red;")
        else:
            self.message_label.setText("Usuario o contraseña incorrectos")
            self.message_label.setStyleSheet("color: red;")

    def open_admin_ui(self):
        self.admin_ui = AdminUI()
        self.admin_ui.show()

    def open_employee_ui(self):
        self.employee_ui = EmployeeUI()
        self.employee_ui.show()
