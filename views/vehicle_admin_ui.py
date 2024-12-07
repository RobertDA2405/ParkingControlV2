from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QDialog
from controllers.vehicle_controller import VehicleController

class VehicleAdminUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Administrar Vehículos")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.vehicle_table = QTableWidget()
        layout.addWidget(self.vehicle_table)

        self.add_vehicle_button = QPushButton("Agregar Vehículo")
        self.delete_vehicle_button = QPushButton("Eliminar Vehículo")
        self.update_vehicle_button = QPushButton("Actualizar Vehículo")

        layout.addWidget(self.add_vehicle_button)
        layout.addWidget(self.delete_vehicle_button)
        layout.addWidget(self.update_vehicle_button)

        self.add_vehicle_button.clicked.connect(self.add_vehicle)
        self.delete_vehicle_button.clicked.connect(self.delete_vehicle)
        self.update_vehicle_button.clicked.connect(self.update_vehicle)

        self.setLayout(layout)

        self.load_vehicles()

    def load_vehicles(self):
        vehicles = VehicleController.get_all_vehicles()

        if vehicles:
            self.vehicle_table.setRowCount(len(vehicles))
            self.vehicle_table.setColumnCount(6)
            self.vehicle_table.setHorizontalHeaderLabels(["Placa", "Tipo", "Color", "Hora Ingreso", "Hora Salida", "Pago"])

            for row, vehicle in enumerate(vehicles):
                self.vehicle_table.setItem(row, 0, QTableWidgetItem(vehicle["Placa"]))
                self.vehicle_table.setItem(row, 1, QTableWidgetItem(vehicle["tipo_Vehiculo"]))
                self.vehicle_table.setItem(row, 2, QTableWidgetItem(vehicle["Color"]))
                self.vehicle_table.setItem(row, 3, QTableWidgetItem(vehicle["HoraIngreso"]))
                self.vehicle_table.setItem(row, 4, QTableWidgetItem(vehicle["HoraSalida"]))
                self.vehicle_table.setItem(row, 5, QTableWidgetItem(str(vehicle["Pago"])))

            self.vehicle_table.setSortingEnabled(True)
        else:
            print("No se encontraron vehículos registrados.")

    def add_vehicle(self):
        self.welcome_label.setText("Agregar nuevo vehículo...")

    def delete_vehicle(self):
        selected_row = self.vehicle_table.currentRow()
        if selected_row != -1:
            placa = self.vehicle_table.item(selected_row, 0).text()
            success = VehicleController.delete_vehicle(placa)
            if success:
                self.load_vehicles()
                print(f"Vehículo con placa {placa} eliminado.")
            else:
                print("Error al eliminar el vehículo.")
        else:
            print("Por favor, seleccione un vehículo para eliminar.")

    def update_vehicle(self):
        selected_row = self.vehicle_table.currentRow()
        if selected_row != -1:
            placa = self.vehicle_table.item(selected_row, 0).text()
            self.welcome_label.setText(f"Actualizar vehículo con placa {placa}...")
        else:
            print("Por favor, seleccione un vehículo para actualizar.")
