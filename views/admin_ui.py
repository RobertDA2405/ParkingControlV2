from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView, QDialog
)
from PyQt6.QtCore import Qt
from controllers.vehicle_controller import VehicleController
from controllers.employee_controller import EmployeeController


class AdminUI(QWidget):
    def __init__(self, role="admin"):
        super().__init__()

        self.role = role
        self.setWindowTitle("Interfaz de Administrador")
        self.showMaximized()

        layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Bienvenido, {self.get_username()} ({role})")
        layout.addWidget(self.welcome_label)

        layout.addWidget(QLabel("Vehículos Pequeños"))
        self.small_vehicle_table = QTableWidget()
        self.small_vehicle_table.setColumnCount(10)
        self.small_vehicle_table.setHorizontalHeaderLabels([
            "Tipo", "Color", "Placa", "Hora de entrada", "Hora de salida", "Pago",
            "Pendiente", "Observaciones", "Estado", "Acciones"
        ])
        self.small_vehicle_table.horizontalHeader().setStretchLastSection(True)
        self.small_vehicle_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.small_vehicle_table)

        layout.addWidget(QLabel("Vehículos Grandes"))
        self.large_vehicle_table = QTableWidget()
        self.large_vehicle_table.setColumnCount(10)
        self.large_vehicle_table.setHorizontalHeaderLabels([
            "Tipo", "Color", "Placa", "Hora de entrada", "Hora de salida", "Pago",
            "Pendiente", "Observaciones", "Estado", "Acciones"
        ])
        self.large_vehicle_table.horizontalHeader().setStretchLastSection(True)
        self.large_vehicle_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.large_vehicle_table)

        button_layout = QHBoxLayout()
        self.add_vehicle_button = QPushButton("Añadir nuevo vehículo")
        button_layout.addWidget(self.add_vehicle_button)

        if self.role == "admin":
            self.view_employees_button = QPushButton("Ver empleados")
            button_layout.addWidget(self.view_employees_button)

            self.add_employee_button = QPushButton("Añadir nuevo empleado")
            button_layout.addWidget(self.add_employee_button)

        self.logout_button = QPushButton("Cerrar sesión")
        button_layout.addWidget(self.logout_button)

        layout.addLayout(button_layout)

        self.add_vehicle_button.clicked.connect(self.add_vehicle)
        if self.role == "admin":
            self.view_employees_button.clicked.connect(self.view_employees)
            self.add_employee_button.clicked.connect(self.add_employee)
        self.logout_button.clicked.connect(self.logout)

        self.setLayout(layout)

        self.load_vehicles()

    def get_username(self):
        """Obtener el nombre del usuario actual."""
        return "Usuario"

    def load_vehicles(self):
        try:
            vehicles = VehicleController.get_all_vehicles()

            small_vehicles = [
                v for v in vehicles if v["tipo_Vehiculo"] in ["Carro", "Moto", "Caponera", "Otro"]
            ]
            large_vehicles = [
                v for v in vehicles if v["tipo_Vehiculo"] in [
                    "Camioneta", "Microbus", "Vehiculo pequeño", "Vehiculo Regular",
                    "Vehiculo Grande", "Vehiculo Extra Grande", "Otro"
                ]
            ]

            self.populate_table(self.small_vehicle_table, small_vehicles)
            self.populate_table(self.large_vehicle_table, large_vehicles)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar vehículos: {str(e)}")

    def populate_table(self, table, vehicles):
        table.setRowCount(len(vehicles))
        for row, vehicle in enumerate(vehicles):
            table.setItem(row, 0, QTableWidgetItem(str(vehicle["tipo_Vehiculo"])))
            table.setItem(row, 1, QTableWidgetItem(str(vehicle["Color"])))
            table.setItem(row, 2, QTableWidgetItem(str(vehicle["Placa"])))
            table.setItem(row, 3, QTableWidgetItem(str(vehicle["HoraIngreso"])))
            table.setItem(row, 4, QTableWidgetItem(str(vehicle["HoraSalida"])))
            table.setItem(row, 5, QTableWidgetItem(str(vehicle["Pago"])))
            table.setItem(row, 6, QTableWidgetItem(str(vehicle.get("Pendiente", "N/A"))))
            table.setItem(row, 7, QTableWidgetItem(str(vehicle.get("Observaciones", "N/A"))))
            table.setItem(row, 8, QTableWidgetItem(str(vehicle.get("estado", "Desconocido"))))

            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(lambda checked, row=row: self.edit_vehicle(table, row))
            button_layout.addWidget(edit_button)

            if vehicle["estado"] == "Dentro del Parqueo":
                exit_button = QPushButton("Registrar Salida")
                exit_button.clicked.connect(lambda checked, row=row: self.register_exit(table, row))
                button_layout.addWidget(exit_button)

            delete_button = QPushButton("Eliminar")
            delete_button.clicked.connect(lambda checked, row=row: self.delete_vehicle(table, row))
            button_layout.addWidget(delete_button)

            widget = QWidget()
            widget.setLayout(button_layout)
            table.setCellWidget(row, 9, widget)

    def view_employees(self):
        """Abrir una ventana para mostrar la lista de empleados."""
        try:
            employees = EmployeeController.get_all_employees()

            dialog = QDialog(self)
            dialog.setWindowTitle("Lista de Empleados")
            dialog.setGeometry(200, 200, 600, 400)

            layout = QVBoxLayout()
            table = QTableWidget()
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["ID", "Nombre", "Rol"])
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            table.setRowCount(len(employees))
            for row, employee in enumerate(employees):
                table.setItem(row, 0, QTableWidgetItem(str(employee["id"])))
                table.setItem(row, 1, QTableWidgetItem(employee["nombre"]))
                table.setItem(row, 2, QTableWidgetItem(employee["rol"]))

            layout.addWidget(table)
            dialog.setLayout(layout)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar empleados: {str(e)}")

    def add_vehicle(self):
        from views.add_vehicle_ui import AddVehicleUI
        self.add_vehicle_window = AddVehicleUI()
        self.add_vehicle_window.exec()
        self.load_vehicles()

    def edit_vehicle(self, table, row):
        vehicle = {
            "idvehicle": table.item(row, 2).data(Qt.ItemDataRole.UserRole),
            "tipo_Vehiculo": table.item(row, 0).text(),
            "Color": table.item(row, 1).text(),
            "Placa": table.item(row, 2).text(),
            "HoraIngreso": table.item(row, 3).text(),
            "HoraSalida": table.item(row, 4).text(),
            "Pago": table.item(row, 5).text(),
            "Pendiente": table.item(row, 6).text(),
            "Observaciones": table.item(row, 7).text(),
            "estado": table.item(row, 8).text()
        }
        from views.edit_vehicle_ui import EditVehicleUI
        self.edit_vehicle_window = EditVehicleUI(vehicle)
        self.edit_vehicle_window.exec()
        self.load_vehicles()

    def register_exit(self, table, row):
        try:
            from views.register_exit_ui import RegisterExitUI
            vehicle = {
                "idvehicle": table.item(row, 2).data(Qt.ItemDataRole.UserRole),
                "Placa": table.item(row, 2).text(),
                "Pendiente": table.item(row, 6).text(),
                "Pago": table.item(row, 5).text(),
                "tipo_Vehiculo": table.item(row, 0).text(),
                "Color": table.item(row, 1).text(),
                "HoraIngreso": table.item(row, 3).text()
            }
            self.register_exit_window = RegisterExitUI(vehicle)
            self.register_exit_window.exec()
            self.load_vehicles()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar salida: {str(e)}")

    def delete_vehicle(self, table, row):
        try:
            placa = table.item(row, 2).text()
            confirm = QMessageBox.question(
                self, "Confirmar", f"¿Estás seguro de eliminar el vehículo con placa {placa}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                VehicleController.delete_vehicle(placa)
                QMessageBox.information(self, "Éxito", "Vehículo eliminado correctamente.")
                self.load_vehicles()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar vehículo: {str(e)}")

    def add_employee(self):
        from views.add_employee_ui import AddEmployeeUI
        self.add_employee_window = AddEmployeeUI()
        self.add_employee_window.exec()

    def view_employees(self):
        QMessageBox.information(self, "Empleados", "Función de visualización en desarrollo.")

    def logout(self):
        self.close()
