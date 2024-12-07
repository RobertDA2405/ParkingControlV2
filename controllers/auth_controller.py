from models.user_model import UserModel
from config.database import Database

class AuthController:
    @staticmethod
    def login(username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        params = (username, password)
        
        db_instance = Database()
        
        user = db_instance.fetch_one(query, params)
        
        if user:
            user_role = user['role']
            return True, user_role
        return False, None
