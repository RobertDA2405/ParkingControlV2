import sys
from PyQt6.QtWidgets import QApplication
from views.login_ui import LoginUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginUI()
    login.show()
    sys.exit(app.exec())