from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
)
from controllers.vehicle_controller import VehicleController
from datetime import datetime

class RegisterExitUI(QDialog):
    def __init__(self, vehicle):
        super().__init__()

        self.vehicle = vehicle

        self.setWindowTitle(f"Registrar Salida - {vehicle['Placa']}")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.tipo_label = QLabel(vehicle["tipo_Vehiculo"])
        self.color_label = QLabel(vehicle["Color"])
        self.placa_label = QLabel(vehicle["Placa"])
        self.hora_ingreso_label = QLabel(vehicle["HoraIngreso"])
        self.pendiente_label = QLabel(f"{float(vehicle['Pendiente']):.2f}")

        self.pago_checkbox = QCheckBox("¿Pagó?")
        self.pago_input = QLineEdit()
        self.pago_input.setDisabled(True)
        self.pago_checkbox.stateChanged.connect(self.toggle_payment)

        self.hora_salida = datetime.now().strftime("%I:%M %p")
        self.hora_salida_label = QLabel(self.hora_salida)

        form_layout.addRow("Tipo de Vehículo:", self.tipo_label)
        form_layout.addRow("Color:", self.color_label)
        form_layout.addRow("Placa:", self.placa_label)
        form_layout.addRow("Hora de Ingreso:", self.hora_ingreso_label)
        form_layout.addRow("Hora de Salida:", self.hora_salida_label)
        form_layout.addRow("Pendiente:", self.pendiente_label)
        form_layout.addRow(self.pago_checkbox)
        form_layout.addRow("Pago:", self.pago_input)

        save_button = QPushButton("Registrar Salida")
        save_button.clicked.connect(self.save_exit)

        layout.addLayout(form_layout)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def toggle_payment(self):
        """Habilitar o deshabilitar el campo de pago según el estado del checkbox."""
        if self.pago_checkbox.isChecked():
            self.pago_input.setDisabled(False)
        else:
            self.pago_input.setDisabled(True)
            self.pago_input.setText("")

    def save_exit(self):
        """Guardar la salida del vehículo."""
        try:
            pendiente = float(self.vehicle["Pendiente"]) if self.vehicle["Pendiente"] else 0.0
            pago = float(self.pago_input.text()) if self.pago_checkbox.isChecked() and self.pago_input.text() else 0.0

            if pago > pendiente:
                QMessageBox.warning(self, "Advertencia", "El pago excede el monto pendiente. Revise los datos.")
                return

            success = VehicleController.register_exit(
                self.vehicle["Placa"],
                self.hora_salida,
                pago
            )

            if success:
                QMessageBox.information(self, "Éxito", "Salida registrada correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la salida. Verifique los datos.")
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese un valor de pago válido.")
