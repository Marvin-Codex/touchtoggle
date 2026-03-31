"""
Main Window UI Module

Contains the GUI layout and event handling for the TouchToggle application.
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from logic.touchscreen_manager import TouchScreenManager


class MainWindow(QMainWindow):
    """Main application window for TouchToggle."""
    
    # Custom signals
    status_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.touchscreen_manager = TouchScreenManager()
        self.setup_icon()
        self.setup_ui()
        self.setup_styles()
        self.check_admin_privileges()
        self.refresh_status()
    
    def setup_icon(self):
        """Set up the application icon for window and taskbar."""
        import os
        from PyQt6.QtGui import QIcon, QPixmap
        
        # Try to find the icon file
        icon_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", "touchtoggle.ico"),
            os.path.join(os.path.dirname(__file__), "..", "assets", "icons", "touchtoggle.ico"),
            "assets/icons/touchtoggle.ico",
            "touchtoggle.ico"
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    icon = QIcon(icon_path)
                    if not icon.isNull():
                        self.setWindowIcon(icon)
                        # Also set for the application
                        QApplication.instance().setWindowIcon(icon)
                        print(f"✅ Icon loaded successfully from: {icon_path}")
                        return
                except Exception as e:
                    print(f"⚠️ Failed to load icon from {icon_path}: {e}")
                    continue
        
        print("ℹ️ No icon found - using default")
        
    def setup_ui(self):
        """Initialize the user interface components with Windows 11 design."""
        self.setWindowTitle("TouchToggle")
        self.setFixedSize(400, 220)
        # Use more compatible window flags
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Center the window on screen
        self.center_window()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Title label with Windows 11 styling
        title_label = QLabel("TouchToggle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Segoe UI Variable Display", 20)
        title_font.setBold(True)
        title_font.setWeight(600)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #202020; margin-bottom: 8px;")
        main_layout.addWidget(title_label)
        
        # Status card with Windows 11 styling
        status_card = QFrame()
        status_card.setObjectName("status_card")
        status_card.setMinimumHeight(70)
        status_card.setMaximumHeight(90)
        status_card_layout = QVBoxLayout(status_card)
        status_card_layout.setContentsMargins(20, 16, 20, 16)
        
        # Status label
        self.status_label = QLabel("Status: Checking...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(35)
        status_font = QFont("Segoe UI Variable Text", 14)
        self.status_label.setFont(status_font)
        status_card_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_card)
        
        # Toggle button with Windows 11 styling
        self.toggle_button = QPushButton("Toggle Touchscreen")
        self.toggle_button.setMinimumHeight(48)
        self.toggle_button.setObjectName("toggle_button")
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        toggle_font = QFont("Segoe UI Variable Text", 14)
        toggle_font.setWeight(500)
        self.toggle_button.setFont(toggle_font)
        self.toggle_button.clicked.connect(self.toggle_touchscreen)
        main_layout.addWidget(self.toggle_button)
        
        # Connect status update signal
        self.status_updated.connect(self.update_status_label)
        
    def setup_styles(self):
        """Set up the application styling with Windows 11 Fluent Design."""
        # Windows 11 color palette
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f9f9f9;
            }
            
            QLabel {
                color: #202020;
                background: transparent;
            }
            
            #status_card {
                background-color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0, 0, 0, 0.05);
                border-radius: 8px;
                min-height: 70px;
                max-height: 90px;
            }
            
            #toggle_button {
                background-color: #005fb8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 500;
            }
            
            #toggle_button:hover {
                background-color: #0066cc;
            }
            
            #toggle_button:pressed {
                background-color: #004d99;
            }
            
            #toggle_button:disabled {
                background-color: #e5e5e5;
                color: #8a8a8a;
            }
            
            #toggle_button_disable {
                background-color: #c42b1c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 500;
            }
            
            #toggle_button_disable:hover {
                background-color: #d13438;
            }
            
            #toggle_button_disable:pressed {
                background-color: #a4262c;
            }
            
            #toggle_button_enable {
                background-color: #107c10;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 500;
            }
            
            #toggle_button_enable:hover {
                background-color: #0e6e0e;
            }
            
            #toggle_button_enable:pressed {
                background-color: #0c5a0c;
            }
        """)
    
    def center_window(self):
        """Center the window on the screen."""
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
            window_geometry.moveCenter(center_point)
            self.move(window_geometry.topLeft())
    
    def check_admin_privileges(self):
        """Check if running with administrator privileges and show warning if not."""
        if not self.touchscreen_manager.is_admin():
            QMessageBox.warning(
                self,
                "Administrator Rights Required",
                "This application requires administrator privileges to modify touchscreen settings.\n\n"
                "Please restart the application as an administrator for full functionality.",
                QMessageBox.StandardButton.Ok
            )
            self.toggle_button.setEnabled(False)
            self.toggle_button.setText("Admin Rights Required")
            self.toggle_button.setObjectName("toggle_button")  # Use default disabled styling
    
    def refresh_status(self):
        """Refresh the touchscreen status display with Windows 11 styling."""
        is_enabled, status_msg = self.touchscreen_manager.get_touchscreen_status()
        self.status_updated.emit(status_msg)
        
        # Update toggle button text and styling based on current status
        if self.toggle_button.isEnabled():
            if is_enabled:
                self.toggle_button.setText("Disable Touchscreen")
                self.toggle_button.setObjectName("toggle_button_disable")
            else:
                self.toggle_button.setText("Enable Touchscreen")
                self.toggle_button.setObjectName("toggle_button_enable")
            # Refresh the styling
            self.toggle_button.setStyle(self.toggle_button.style())
    
    def update_status_label(self, status_text):
        """Update the status label with Windows 11 styling."""
        self.status_label.setText(f"{status_text}")
        
        # Windows 11 color coding for status
        if "ON" in status_text or "enabled" in status_text:
            self.status_label.setStyleSheet("""
                QLabel { 
                    color: #107c10; 
                    font-weight: 600;
                    background: transparent;
                }
            """)
        elif "OFF" in status_text or "disabled" in status_text:
            self.status_label.setStyleSheet("""
                QLabel { 
                    color: #d13438; 
                    font-weight: 600;
                    background: transparent;
                }
            """)
        else:
            self.status_label.setStyleSheet("""
                QLabel { 
                    color: #605e5c; 
                    font-weight: 400;
                    background: transparent;
                }
            """)
    
    def toggle_touchscreen(self):
        """Handle the toggle touchscreen button click."""
        # Immediately update UI to show processing state
        self.toggle_button.setEnabled(False)
        self.toggle_button.setText("Processing...")
        self.status_updated.emit("Processing request...")
        
        # Force the UI to update immediately
        QApplication.processEvents()
        
        # Use QTimer to defer the actual operation slightly to ensure UI updates
        QTimer.singleShot(50, self._perform_toggle_operation)
    
    def _perform_toggle_operation(self):
        """Perform the actual toggle operation (called after UI update)."""
        # Perform the toggle operation
        success, message = self.touchscreen_manager.toggle_touchscreen()
        
        if success:
            # Wait a moment for the system to update, then refresh status
            QTimer.singleShot(1000, self.refresh_status)
        else:
            # Show error message
            QMessageBox.critical(
                self,
                "Operation Failed",
                f"Failed to toggle touchscreen:\n{message}",
                QMessageBox.StandardButton.Ok
            )
            self.status_updated.emit(message)
        
        # Re-enable button
        self.toggle_button.setEnabled(True)
        QTimer.singleShot(1000, self.refresh_status)
    
    def closeEvent(self, event):
        """Handle the window close event."""
        # Simple close without confirmation for better UX
        event.accept()
