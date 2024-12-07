from config.database import Database

class EmployeeController:
    @staticmethod
    def add_employee(username, password, role):
        db = Database()
        try:
            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            db.execute_query(query, (username, password, role))
        except Exception as e:
            db.conn.rollback()
            raise e
        finally:
            db.close()
