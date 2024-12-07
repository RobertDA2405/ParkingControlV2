from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QSpinBox, QCheckBox
)
from controllers.vehicle_controller import VehicleController


class AddVehicleUI(QDialog):
    VEHICLE_PRICES = {
        "Carro": 30,
        "Moto": 20,
        "Caponera": 30,
        "Camioneta": 40,
        "Microbus": 40,
        "Vehiculo pequeño": 40,
        "Vehiculo Regular": 50,
        "Vehiculo Grande": 60,
        "Vehiculo Extra Grande": 70,
        "Otro": 0,
    }

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Añadir Nuevo Vehículo")
        self.setGeometry(200, 200, 400, 500)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(self.VEHICLE_PRICES.keys())
        self.tipo_combo.currentTextChanged.connect(self.update_price)

        self.color_input = QLineEdit()
        self.placa_input = QLineEdit()

        self.hora_ingreso_spinbox = QSpinBox()
        self.hora_ingreso_spinbox.setRange(1, 12)

        self.minuto_ingreso_spinbox = QSpinBox()
        self.minuto_ingreso_spinbox.setRange(0, 59)

        self.periodo_ingreso_combo = QComboBox()
        self.periodo_ingreso_combo.addItems(["AM", "PM"])

        self.pago_checkbox = QCheckBox("¿Pagó?")
        self.pago_checkbox.stateChanged.connect(self.toggle_payment)

        self.pago_input = QLineEdit()
        self.pago_input.setDisabled(True)

        self.pendiente_input = QLineEdit()
        self.pendiente_input.setReadOnly(True)

        self.observaciones_input = QLineEdit()

        form_layout.addRow("Tipo de Vehículo:", self.tipo_combo)
        form_layout.addRow("Color:", self.color_input)
        form_layout.addRow("Placa:", self.placa_input)

        form_layout.addRow(QLabel("Hora de Ingreso:"), self.hora_ingreso_spinbox)
        form_layout.addRow(QLabel("Minuto de Ingreso:"), self.minuto_ingreso_spinbox)
        form_layout.addRow(QLabel("Periodo de Ingreso:"), self.periodo_ingreso_combo)

        form_layout.addRow(self.pago_checkbox)
        form_layout.addRow("Pago:", self.pago_input)
        form_layout.addRow("Pendiente:", self.pendiente_input)
        form_layout.addRow("Observaciones:", self.observaciones_input)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_vehicle)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def update_price(self):
        """Actualizar el precio de 'Pendiente' según el tipo de vehículo seleccionado."""
        tipo = self.tipo_combo.currentText()
        precio = self.VEHICLE_PRICES.get(tipo, 0)

        if tipo == "Otro":
            self.pendiente_input.setReadOnly(False)
            self.pendiente_input.setText("")
        else:
            self.pendiente_input.setReadOnly(True)
            self.pendiente_input.setText(str(precio))

    def toggle_payment(self):
        """Habilitar o deshabilitar el campo de pago según el estado del checkbox."""
        if self.pago_checkbox.isChecked():
            self.pago_input.setDisabled(False)
        else:
            self.pago_input.setDisabled(True)
            self.pago_input.setText("")

    def save_vehicle(self):
        """Guardar el vehículo en la base de datos."""
        tipo = self.tipo_combo.currentText()
        color = self.color_input.text()
        placa = self.placa_input.text()

        hora_ingreso = f"{self.hora_ingreso_spinbox.value():02}:{self.minuto_ingreso_spinbox.value():02} {self.periodo_ingreso_combo.currentText()}"
        hora_salida = None

        try:
            pago = float(self.pago_input.text()) if self.pago_input.text() else 0
            pendiente = float(self.pendiente_input.text()) if self.pendiente_input.text() else 0
            pendiente -= pago
        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, asegúrate de que los campos de pago y pendiente sean válidos.")
            return

        observaciones = self.observaciones_input.text()

        if not tipo or not color or not placa:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos obligatorios.")
            return

        try:
            success = VehicleController.add_vehicle(
                tipo_vehiculo=tipo,
                color=color,
                placa=placa,
                hora_ingreso=hora_ingreso,
                pago=pago,
                pendiente=pendiente,
                observaciones=observaciones,
            )
            if success:
                QMessageBox.information(self, "Éxito", "Vehículo añadido correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo añadir el vehículo.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar vehículo: {str(e)}")
