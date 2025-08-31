# FileMorph

<img width="3780" height="1890" alt="Image" src="https://github.com/user-attachments/assets/ff7f9df7-ea19-4356-b35f-15dca36b7e22" />

## Overview
FileMorph is a Python-based GUI application built with PyQt5 that allows users to convert files between `.txt`, `.csv`, `.json`, and `.xml` formats. The application features a user-friendly interface with a title, logo, file selection, browse button, output format dropdown, conversion button, and status messages.
---
## Features
- Convert between `.txt`, `.csv`, `.json`, and `.xml` formats.
- Browse and select files directly from the system.
- Status updates for conversion progress and errors.
- Includes a logo and themed GUI for improved user experience.
---
## Installation
1. Ensure Python 3.x is installed.
2. Install required packages:
```bash
pip install pyqt5
```
3. Download the project files, including `main.py` and `logo.png`.
---
## Usage
1. Run the application:
```bash
python main.py
```
2. Select the input file using the Browse button or by entering the path manually.
3. Choose the desired output format from the dropdown.
4. Click Convert to save the file in the new format.
---
## Notes
- The application currently supports the following conversions:
  - `.txt` ↔ `.csv`
  - `.txt` ↔ `.json`
  - `.csv` ↔ `.json`
  - `.json` ↔ `.xml`
- Ensure `logo.png` is in the same directory as the `.exe` when building with PyInstaller.
- Review code for potential errors or unsupported file structures when converting complex files.
- this is just a basic code , I am planning on upgrading it motre in the near future

