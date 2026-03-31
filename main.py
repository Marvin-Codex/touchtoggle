"""
TouchToggle Desktop Application

A lightweight Windows utility for enabling/disabling laptop touchscreens
with a single click using PyQt6 and PowerShell commands.

Author: TouchToggle Development Team
Version: 1.0.0
Platform: Windows 10/11
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Add the current directory to Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def setup_logging():
    """Set up logging configuration."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('touchtoggle.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def check_system_compatibility():
    """Check if the system is compatible with TouchToggle."""
    if sys.platform != 'win32':
        QMessageBox.critical(
            None,
            "System Compatibility Error",
            "TouchToggle is designed for Windows systems only.\n"
            f"Current platform: {sys.platform}",
            QMessageBox.StandardButton.Ok
        )
        return False
    
    # Check Python version
    if sys.version_info < (3, 7):
        QMessageBox.critical(
            None,
            "Python Version Error",
            "TouchToggle requires Python 3.7 or higher.\n"
            f"Current version: {sys.version}",
            QMessageBox.StandardButton.Ok
        )
        return False
    
    return True


def main():
    """Main application entry point."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting TouchToggle application")
    
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("TouchToggle")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Marvin tech solutions")
    app.setApplicationDisplayName("Touchscreen Control Utility by Marvin")
    
    # Set application icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons", "touchtoggle.ico")
        if os.path.exists(icon_path):
            from PyQt6.QtGui import QIcon
            app.setWindowIcon(QIcon(icon_path))
    except Exception:
        pass  # Continue without icon if there's an issue
    
    # High DPI support is automatic in Qt 6
    
    # Check system compatibility
    if not check_system_compatibility():
        logger.error("System compatibility check failed")
        sys.exit(1)
    
    try:
        # Create and show main window
        main_window = MainWindow()
        main_window.show()
        
        logger.info("TouchToggle application started successfully")
        
        # Start the application event loop
        exit_code = app.exec()
        
        logger.info(f"TouchToggle application exiting with code: {exit_code}")
        sys.exit(exit_code)
        
    except ImportError as e:
        error_msg = f"Missing required dependency: {e}"
        logger.error(error_msg)
        QMessageBox.critical(
            None,
            "Dependency Error",
            f"Failed to import required modules:\n{error_msg}\n\n"
            "Please ensure PyQt6 is installed:\npip install PyQt6",
            QMessageBox.StandardButton.Ok
        )
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(error_msg, exc_info=True)
        QMessageBox.critical(
            None,
            "Application Error", 
            f"An unexpected error occurred:\n{error_msg}",
            QMessageBox.StandardButton.Ok
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
