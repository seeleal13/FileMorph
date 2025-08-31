import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, 
    QHBoxLayout, QLineEdit, QPushButton, QComboBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import json
import csv
import xml.etree.ElementTree as ET

class FileMorphApp(QMainWindow):
    """
    FileMorph application with a themed PyQt5 GUI for file conversion.
    Features a centered, bold title with a logo (65x65 pixels), file path entry,
    browse button, output format dropdown, convert button, and status label.
    Supports conversions: .txt ↔ .csv, .txt ↔ .json, .csv ↔ .json, .json ↔ .xml.
    Uses Lilita One font, #F9E0AD text color, and #C34915 background.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FileMorph")
        self.resize(400, 300)

        # Central widget and main vertical layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Horizontal layout for logo and title
        self.title_layout = QHBoxLayout()
        self.title_layout.setAlignment(Qt.AlignHCenter)  # Center horizontally
        self.layout.addLayout(self.title_layout)

        # Logo label
        self.logo_label = QLabel()
        pixmap = QPixmap("logo.png")  # Placeholder path to logo image
        if not pixmap.isNull():
            pixmap = pixmap.scaled(65, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("(Logo)")  # Fallback if image not found
        self.title_layout.addWidget(self.logo_label)

        # Title label
        self.title_label = QLabel("FileMorph")
        font = QFont("Lilita One", 24)  # Lilita One font, size 24
        font.setBold(True)  # Bold title
        self.title_label.setFont(font)
        self.title_layout.addWidget(self.title_label)

        # Spacing for title/logo
        self.layout.setContentsMargins(0, 20, 0, 0)  # Slight upward positioning
        self.layout.addSpacing(10)  # Gap before input components

        # Input file path entry
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Select a file...")
        self.layout.addWidget(self.file_path_edit)

        # Browse button
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_file)
        self.layout.addWidget(self.browse_btn)

        # Output format dropdown
        self.output_combo = QComboBox()
        self.output_combo.addItems([".txt", ".csv", ".json", ".xml"])
        self.layout.addWidget(self.output_combo)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert_file)
        self.layout.addWidget(self.convert_btn)

        # Status label
        self.status_label = QLabel("Ready")
        self.layout.addWidget(self.status_label)

        # Add stretch to push content upward
        self.layout.addStretch()

        # Apply theme via stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #C34915;
            }
            QLabel, QLineEdit, QComboBox, QPushButton {
                color: #F9E0AD;
            }
            QLineEdit, QComboBox, QPushButton {
                background-color: #A83C12;  /* Slightly darker shade for contrast */
                border: 1px solid #F9E0AD;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #D95A1A;  /* Lighter shade on hover */
            }
        """)

    def browse_file(self):
        """Open file dialog to select input file and display its path."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "Text Files (*.txt *.csv *.json *.xml);;All Files (*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
            self.status_label.setText("File selected.")

    def convert_file(self):
        """Handle file conversion based on input file and selected output format."""
        input_path = self.file_path_edit.text()
        if not input_path:
            self.status_label.setText("Error: No file selected.")
            return

        # Extract input extension
        input_ext = '.' + input_path.split('.')[-1].lower()
        output_ext = self.output_combo.currentText()

        if input_ext not in [".txt", ".csv", ".json", ".xml"]:
            self.status_label.setText("Error: Unsupported input format.")
            return

        # Check if conversion is supported
        if not self.is_conversion_possible(input_ext, output_ext):
            self.status_label.setText("Error: Conversion not supported.")
            return

        # Load data from input file
        try:
            data = self.load_file(input_path, input_ext)
        except Exception as e:
            self.status_label.setText(f"Error loading file: {str(e)}")
            return

        # Open save dialog with appropriate extension
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Converted File", "", f"{output_ext.upper()[1:]} Files (*{output_ext})"
        )
        if not save_path:
            self.status_label.setText("Conversion cancelled.")
            return

        # Save data to output file
        try:
            self.save_file(data, save_path, output_ext)
            self.status_label.setText("Conversion successful.")
        except Exception as e:
            self.status_label.setText(f"Error saving file: {str(e)}")

    def is_conversion_possible(self, input_ext, output_ext):
        """Check if conversion between input and output formats is supported."""
        supported_conversions = {
            ('.txt', '.csv'), ('.csv', '.txt'),
            ('.txt', '.json'), ('.json', '.txt'),
            ('.csv', '.json'), ('.json', '.csv'),
            ('.json', '.xml'), ('.xml', '.json')
        }
        return (input_ext, output_ext) in supported_conversions

    def load_file(self, path, ext):
        """Load file content into a Python data structure based on extension."""
        if ext == '.txt':
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [[line.strip()] for line in lines]  # List of single-element lists
        elif ext == '.csv':
            with open(path, 'r', encoding='utf-8') as f:
                return list(csv.reader(f))
        elif ext == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif ext == '.xml':
            tree = ET.parse(path)
            return self.xml_to_dict(tree.getroot())

    def save_file(self, data, path, ext):
        """Save data to file in the specified format."""
        if ext == '.txt':
            with open(path, 'w', encoding='utf-8') as f:
                if isinstance(data, list):
                    for row in data:
                        if isinstance(row, list):
                            f.write(','.join(map(str, row)) + '\n')
                        else:
                            f.write(str(row) + '\n')
                elif isinstance(data, dict):
                    for k, v in data.items():
                        f.write(f"{k}: {v}\n")
                else:
                    f.write(str(data))
        elif ext == '.csv':
            if not isinstance(data, list) or not data or not all(isinstance(row, list) for row in data):
                raise ValueError("Data must be a list of lists for CSV.")
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        elif ext == '.json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        elif ext == '.xml':
            if not isinstance(data, dict):
                raise ValueError("Data must be a dictionary for XML.")
            root = self.dict_to_xml(data)
            ET.ElementTree(root).write(path, encoding='unicode', xml_declaration=True)

    @staticmethod
    def xml_to_dict(element):
        if len(element) == 0:
            return element.text or ''
        d = {}
        for child in element:
            value = FileMorphApp.xml_to_dict(child)
            if child.tag in d:
                if not isinstance(d[child.tag], list):
                    d[child.tag] = [d[child.tag]]
                d[child.tag].append(value)
            else:
                d[child.tag] = value
        return d

    @staticmethod
    def dict_to_xml(d, root_name='root'):
        root = ET.Element(root_name)
        FileMorphApp._build_xml(root, d)
        return root

    @staticmethod
    def _build_xml(parent, item):
        if isinstance(item, dict):
            for k, v in item.items():
                child = ET.SubElement(parent, k)
                FileMorphApp._build_xml(child, v)
        elif isinstance(item, list):
            for v in item:
                child = ET.SubElement(parent, 'item')
                FileMorphApp._build_xml(child, v)
        else:
            parent.text = str(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileMorphApp()
    window.show()
    sys.exit(app.exec_())