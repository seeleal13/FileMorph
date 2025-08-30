import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, 
    QHBoxLayout, QLineEdit, QPushButton, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class FileMorphApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileMorph")
        self.resize(400, 300)  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_layout = QHBoxLayout()
        self.title_layout.setAlignment(Qt.AlignHCenter)  
        self.layout.addLayout(self.title_layout)

        # Logo label
        self.logo_label = QLabel()
        pixmap = QPixmap("logo.png")  
        if not pixmap.isNull():
            pixmap = pixmap.scaled(65, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("(Logo)")  
        self.title_layout.addWidget(self.logo_label)

        
        self.title_label = QLabel("FileMorph")
        font = QFont("Lilita One", 24)  
        font.setBold(True)  
        self.title_label.setFont(font)
        self.title_layout.addWidget(self.title_label)

        
        self.layout.setContentsMargins(0, 20, 0, 0)  
        self.layout.addSpacing(10)  

       
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Enter or select a file...")
        self.layout.addWidget(self.file_path_edit)

        
        self.output_combo = QComboBox()
        self.output_combo.addItems([".txt", ".csv", ".json", ".xml"])
        self.layout.addWidget(self.output_combo)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.layout.addWidget(self.convert_btn)

        # Status label
        self.status_label = QLabel("Ready")
        self.layout.addWidget(self.status_label)



        self.setStyleSheet("""
            QMainWindow {
                background-color: #C34915;
            }
            QLabel, QLineEdit, QComboBox, QPushButton {
                color: #F9E0AD;
            }
            QLineEdit, QComboBox, QPushButton {
                background-color: #A83C12; 
                border: 1px solid #F9E0AD;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #D95A1A;  
            }
        """)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMorphApp()
    window.show()
    sys.exit(app.exec_())