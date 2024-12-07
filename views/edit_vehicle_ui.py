from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class EditVehicleUI(QDialog):
    def __init__(self, vehicle):
        super().__init__()

        self.vehicle = vehicle
        self.setWindowTitle(f"Editar Vehículo - {vehicle['Placa']}")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        self.tipo_input = QLineEdit(vehicle.get("tipo_Vehiculo", ""))
        self.color_input = QLineEdit(vehicle.get("Color", ""))
        self.placa_input = QLineEdit(vehicle.get("Placa", ""))
        self.hora_ingreso_input = QLineEdit(vehicle.get("HoraIngreso", ""))
        self.hora_salida_input = QLineEdit(vehicle.get("HoraSalida", "") or "")  # Manejar None
        self.pago_input = QLineEdit(str(vehicle.get("Pago", 0)))
        self.pendiente_input = QLineEdit(str(vehicle.get("Pendiente", 0)))
        self.observaciones_input = QLineEdit(vehicle.get("Observaciones", ""))

        layout.addWidget(QLabel("Tipo de Vehículo:"))
        layout.addWidget(self.tipo_input)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.color_input)
        layout.addWidget(QLabel("Placa:"))
        layout.addWidget(self.placa_input)
        layout.addWidget(QLabel("Hora de Ingreso:"))
        layout.addWidget(self.hora_ingreso_input)
        layout.addWidget(QLabel("Hora de Salida:"))
        layout.addWidget(self.hora_salida_input)
        layout.addWidget(QLabel("Pago:"))
        layout.addWidget(self.pago_input)
        layout.addWidget(QLabel("Pendiente:"))
        layout.addWidget(self.pendiente_input)
        layout.addWidget(QLabel("Observaciones:"))
        layout.addWidget(self.observaciones_input)

        save_button = QPushButton("Guardar Cambios")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_changes(self):
        updated_vehicle = {
            "idvehicle": self.vehicle.get("idvehicle"),
            "tipo_Vehiculo": self.tipo_input.text(),
            "Color": self.color_input.text(),
            "Placa": self.placa_input.text(),
            "HoraIngreso": self.hora_ingreso_input.text(),
            "HoraSalida": self.hora_salida_input.text() or None,
            "Pago": float(self.pago_input.text()) if self.pago_input.text() else 0,
            "Pendiente": float(self.pendiente_input.text()) if self.pendiente_input.text() else 0,
            "Observaciones": self.observaciones_input.text()
        }

        try:
            from controllers.vehicle_controller import VehicleController
            success = VehicleController.update_vehicle(updated_vehicle)

            if success:
                QMessageBox.information(self, "Éxito", "Vehículo actualizado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar el vehículo.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese valores numéricos válidos en los campos de pago y pendiente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar cambios: {str(e)}")
