from config.database import Database


class VehicleController:
    @staticmethod
    def add_vehicle(tipo_vehiculo, color, placa, hora_ingreso, pago, pendiente, observaciones):
        db = Database()
        try:
            query = """
                INSERT INTO Vehiculo (tipo_Vehiculo, Color, Placa, HoraIngreso, HoraSalida, Pago, Pendiente, Observaciones)
                VALUES (%s, %s, %s, %s, NULL, %s, %s, %s)
            """
            db.execute_query(query, (tipo_vehiculo, color, placa, hora_ingreso, pago, pendiente, observaciones))
            return True
        except Exception as e:
            db.conn.rollback()
            print(f"Error al añadir vehículo: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def get_all_vehicles():
        db = Database()
        try:
            query = "SELECT * FROM Vehiculo"
            return db.fetch_all(query)
        except Exception as e:
            print(f"Error al obtener vehículos: {str(e)}")
            return []
        finally:
            db.close()

    @staticmethod
    def update_vehicle(updated_vehicle):
        db = Database()
        try:
            query = """
                UPDATE Vehiculo
                SET tipo_Vehiculo = %s, Color = %s, Placa = %s, HoraIngreso = %s,
                    HoraSalida = %s, Pago = %s, Pendiente = %s, Observaciones = %s
                WHERE idvehicle = %s
            """
            params = (
                updated_vehicle["tipo_Vehiculo"], updated_vehicle["Color"], updated_vehicle["Placa"],
                updated_vehicle["HoraIngreso"], updated_vehicle["HoraSalida"], float(updated_vehicle["Pago"]),
                float(updated_vehicle["Pendiente"]), updated_vehicle["Observaciones"], updated_vehicle["idvehicle"]
            )
            db.execute_query(query, params)
            return True
        except Exception as e:
            db.conn.rollback()
            print(f"Error al actualizar vehículo: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def register_exit(vehicle_id):
        db = Database()
        try:
            query = """
                UPDATE Vehiculo
                SET HoraSalida = CURRENT_TIME()
                WHERE idvehicle = %s
            """
            db.execute_query(query, (vehicle_id,))
            return True
        except Exception as e:
            db.conn.rollback()
            print(f"Error al registrar salida: {str(e)}")
            return False
        finally:
            db.close()
