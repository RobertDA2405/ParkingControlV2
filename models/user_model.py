from config.database import Database

class UserModel:
    @staticmethod
    def validate_user(username, password):
        db_instance = Database()
        
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        params = (username, password)
        user = db_instance.fetch_one(query, params)
        
        db_instance.close()
        
        return user
