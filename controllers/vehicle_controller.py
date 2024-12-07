from config.database import Database

class VehicleController:
    @staticmethod
    def add_vehicle(tipo_vehiculo, color, placa, hora_ingreso, pago, pendiente, observaciones, idclient=None):
        """Añadir un nuevo vehículo con estado 'Dentro del Parqueo'."""
        db = Database()
        try:
            query = """
                INSERT INTO Vehiculo (tipo_Vehiculo, Color, Placa, HoraIngreso, HoraSalida, Pago, Pendiente, Observaciones, idclient, estado)
                VALUES (%s, %s, %s, %s, NULL, %s, %s, %s, %s, 'Dentro del Parqueo')
            """
            params = (tipo_vehiculo, color, placa, hora_ingreso, pago, pendiente, observaciones, idclient)
            db.execute_query(query, params)
            return True
        except Exception as e:
            db.conn.rollback()
            print(f"Error al añadir vehículo: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def register_exit(placa, hora_salida, pago=None):
        """Registrar la salida del vehículo, actualizando su estado."""
        db = Database()
        try:
            query_select = """
                SELECT Pendiente, Pago 
                FROM Vehiculo 
                WHERE Placa = %s AND estado = 'Dentro del Parqueo'
            """
            vehicle = db.fetch_one(query_select, (placa,))
            if not vehicle:
                print(f"Vehículo con placa {placa} no encontrado o ya está fuera del parqueo.")
                return False

            pendiente = vehicle["Pendiente"]
            pago_acumulado = vehicle["Pago"]

            nuevo_pendiente = pendiente - (pago or 0)
            nuevo_pendiente = max(0, nuevo_pendiente)
            nuevo_pago = pago_acumulado + (pago or 0)

            query_update = """
                UPDATE Vehiculo
                SET HoraSalida = %s, Pago = %s, Pendiente = %s, estado = 'Fuera del Parqueo'
                WHERE Placa = %s AND estado = 'Dentro del Parqueo'
            """
            params = (hora_salida, nuevo_pago, nuevo_pendiente, placa)
            db.execute_query(query_update, params)
            return True
        except Exception as e:
            db.conn.rollback()
            print(f"Error al registrar salida: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def delete_vehicle(placa):
        """Eliminar un vehículo de la base de datos por su placa."""
        db = Database()
        try:
            query = "DELETE FROM Vehiculo WHERE Placa = %s"
            db.execute_query(query, (placa,))
            return True
        except Exception as e:
            db.conn.rollback()
            print(f"Error al eliminar vehículo: {str(e)}")
            return False
        finally:
            db.close()

    @staticmethod
    def update_vehicle(updated_vehicle):
        """Actualizar un vehículo en la base de datos."""
        db = Database()
        try:
            query = """
                UPDATE Vehiculo
                SET tipo_Vehiculo = %s, Color = %s, Placa = %s, HoraIngreso = %s, HoraSalida = %s, 
                    Pago = %s, Pendiente = %s, Observaciones = %s, estado = %s
                WHERE idvehicle = %s
            """
            params = (
                updated_vehicle["tipo_Vehiculo"], updated_vehicle["Color"], updated_vehicle["Placa"],
                updated_vehicle["HoraIngreso"], updated_vehicle["HoraSalida"], updated_vehicle["Pago"],
                updated_vehicle["Pendiente"], updated_vehicle["Observaciones"], updated_vehicle["estado"],
                updated_vehicle["idvehicle"]
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
    def get_all_vehicles():
        """Obtener todos los vehículos de la base de datos."""
        db = Database()
        try:
            query = """
                SELECT 
                    idvehicle, tipo_Vehiculo, Color, Placa, HoraIngreso, HoraSalida, Pago, Pendiente, Observaciones, estado
                FROM Vehiculo
            """
            return db.fetch_all(query)
        except Exception as e:
            print(f"Error al obtener vehículos: {str(e)}")
            return []
        finally:
            db.close()
