from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import Qt
from controllers.vehicle_controller import VehicleController


class EmployeeUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Empleado")
        self.showMaximized()

        layout = QVBoxLayout()

        self.welcome_label = QLabel("Bienvenido, Empleado")
        layout.addWidget(self.welcome_label)

        layout.addWidget(QLabel("Vehículos Registrados"))
        self.vehicle_table = QTableWidget()
        self.vehicle_table.setColumnCount(10)
        self.vehicle_table.setHorizontalHeaderLabels([
            "Tipo", "Color", "Placa", "Hora de entrada", "Hora de salida", "Pago",
            "Pendiente", "Observaciones", "Estado", "Acciones"
        ])
        self.vehicle_table.horizontalHeader().setStretchLastSection(True)
        self.vehicle_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.vehicle_table)

        button_layout = QHBoxLayout()
        self.add_vehicle_button = QPushButton("Añadir nuevo vehículo")
        button_layout.addWidget(self.add_vehicle_button)

        self.logout_button = QPushButton("Cerrar sesión")
        button_layout.addWidget(self.logout_button)

        layout.addLayout(button_layout)

        self.add_vehicle_button.clicked.connect(self.add_vehicle)
        self.logout_button.clicked.connect(self.logout)

        self.setLayout(layout)

        self.load_vehicles()

    def load_vehicles(self):
        """Cargar vehículos en la tabla."""
        try:
            vehicles = VehicleController.get_all_vehicles()

            self.vehicle_table.setRowCount(len(vehicles))
            for row, vehicle in enumerate(vehicles):
                self.vehicle_table.setItem(row, 0, QTableWidgetItem(str(vehicle["tipo_Vehiculo"])))
                self.vehicle_table.setItem(row, 1, QTableWidgetItem(str(vehicle["Color"])))
                self.vehicle_table.setItem(row, 2, QTableWidgetItem(str(vehicle["Placa"])))
                self.vehicle_table.setItem(row, 3, QTableWidgetItem(str(vehicle["HoraIngreso"])))
                self.vehicle_table.setItem(row, 4, QTableWidgetItem(str(vehicle["HoraSalida"])))
                self.vehicle_table.setItem(row, 5, QTableWidgetItem(str(vehicle["Pago"])))
                self.vehicle_table.setItem(row, 6, QTableWidgetItem(str(vehicle.get("Pendiente", "N/A"))))
                self.vehicle_table.setItem(row, 7, QTableWidgetItem(str(vehicle.get("Observaciones", "N/A"))))
                self.vehicle_table.setItem(row, 8, QTableWidgetItem(str(vehicle.get("estado", "Desconocido"))))

                button_layout = QHBoxLayout()
                button_layout.setContentsMargins(0, 0, 0, 0)

                if vehicle["estado"] == "Dentro del Parqueo":
                    exit_button = QPushButton("Registrar Salida")
                    exit_button.clicked.connect(lambda checked, row=row: self.register_exit(self.vehicle_table, row))
                    button_layout.addWidget(exit_button)

                widget = QWidget()
                widget.setLayout(button_layout)
                self.vehicle_table.setCellWidget(row, 9, widget)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar vehículos: {str(e)}")

    def add_vehicle(self):
        """Abrir ventana para añadir un vehículo."""
        from views.add_vehicle_ui import AddVehicleUI
        self.add_vehicle_window = AddVehicleUI()
        self.add_vehicle_window.exec()
        self.load_vehicles()

    def register_exit(self, table, row):
        """Registrar salida de un vehículo."""
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

    def logout(self):
        """Cerrar la sesión y salir."""
        self.close()
