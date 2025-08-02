#!/usr/bin/env python3
"""
RETI-C - Registro de Equipos de Tecnologías de Información - Carlos
Entry point for the desktop application.

Author: Carlos Verastegui
Version: 1.0
Date: 02/08/2025
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.main_app import MainWindow


def main():
    """Main entry point for the RETI-C application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("RETI-C")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CFE")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 