import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

class FileMorphApp(QMainWindow):
   
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileMorph")
        self.resize(400, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMorphApp()
    window.show()
    sys.exit(app.exec_())