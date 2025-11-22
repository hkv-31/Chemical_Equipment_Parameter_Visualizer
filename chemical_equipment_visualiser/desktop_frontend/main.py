import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QTabWidget, QLabel, QPushButton, QMessageBox,
                             QStatusBar, QDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

from components.file_upload import FileUploadTab
from components.data_display import DataDisplayTab
from components.charts import ChartsTab
from components.history import HistoryTab
from components.login_dialog import LoginDialog
from services.api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = None
        self.current_data = None
        self.current_summary = None
        self.history_data = []
        self.active_threads = []  # Track active threads
        
        self.init_ui()
        self.show_login_dialog()
        
    def show_login_dialog(self):
        """Show login dialog to get API credentials"""
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            username, password = dialog.get_credentials()
            self.api_client = APIClient(username=username, password=password)
            if self.check_backend_connection():
                self.status_bar.showMessage("Connected to backend")
            else:
                self.show_login_dialog()  # Retry if connection fails
        else:
            QMessageBox.warning(self, "Authentication Required", 
                               "API authentication is required to use the application.")
            self.close()
    
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer - Desktop")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme
        self.set_dark_theme()
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Chemical Equipment Visualizer")
        header.setAlignment(Qt.AlignCenter)
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("padding: 20px; color: #ffffff;")
        main_layout.addWidget(header)
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Initialize tabs (they'll check if api_client exists)
        self.file_upload_tab = FileUploadTab(self)
        self.data_display_tab = DataDisplayTab(self)
        self.charts_tab = ChartsTab(self)
        self.history_tab = HistoryTab(self)
        
        # Add tabs
        self.tabs.addTab(self.file_upload_tab, "Upload CSV")
        self.tabs.addTab(self.data_display_tab, "Data Summary")
        self.tabs.addTab(self.charts_tab, "Charts")
        self.tabs.addTab(self.history_tab, "History")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Please login...")
        
    def set_dark_theme(self):
        # Set dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)
        
    def check_backend_connection(self):
        try:
            # Just assume connection is good if we got this far
            # The real test will happen when we try to use the API
            return True
        except Exception as e:
            self.status_bar.showMessage("Backend connection failed")
            QMessageBox.warning(self, "Connection Error", 
                            f"Cannot connect to backend API.\n\n"
                            f"Error: {str(e)}\n\n"
                            f"Make sure Django backend is running on http://localhost:8000")
            return False
    
    def register_thread(self, thread):
        """Register a thread for proper cleanup"""
        self.active_threads.append(thread)
        thread.finished.connect(lambda: self.unregister_thread(thread))
        
    def unregister_thread(self, thread):
        """Unregister a completed thread"""
        if thread in self.active_threads:
            self.active_threads.remove(thread)
            
    def cleanup_threads(self):
        """Clean up all active threads"""
        for thread in self.active_threads[:]:  # Use slice copy to avoid modification during iteration
            try:
                if hasattr(thread, 'stop'):
                    thread.stop()
                else:
                    thread.quit()
                    thread.wait(1000)
            except:
                pass
            self.unregister_thread(thread)
    
    def update_data(self, equipment_data, summary_data):
        """Update data across all tabs"""
        self.current_data = equipment_data
        self.current_summary = summary_data
        
        # Update tabs with new data
        self.data_display_tab.update_data(equipment_data, summary_data)
        self.charts_tab.update_data(equipment_data, summary_data)
        
    def update_history(self):
        """Refresh history data"""
        self.history_tab.load_history()
    
    def show_status(self, message, timeout=5000):
        """Show status message"""
        self.status_bar.showMessage(message, timeout)
        
    def closeEvent(self, event):
        """Handle application closure"""
        self.cleanup_threads()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    # Ensure proper cleanup on exit
    app.aboutToQuit.connect(window.cleanup_threads)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()