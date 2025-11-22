import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QFileDialog, QProgressBar,
                             QTextEdit, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt
from services.api_client import APIWorker

class FileUploadTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # File selection group
        file_group = QGroupBox("CSV File Selection")
        file_layout = QVBoxLayout()
        
        # File path selection
        path_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select CSV file...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        
        path_layout.addWidget(QLabel("File:"))
        path_layout.addWidget(self.file_path)
        path_layout.addWidget(browse_btn)
        file_layout.addLayout(path_layout)
        
        # Dataset name
        name_layout = QHBoxLayout()
        self.dataset_name = QLineEdit()
        self.dataset_name.setPlaceholderText("Enter dataset name...")
        name_layout.addWidget(QLabel("Dataset Name:"))
        name_layout.addWidget(self.dataset_name)
        file_layout.addLayout(name_layout)
        
        # Upload button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        file_layout.addWidget(self.upload_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        file_layout.addWidget(self.progress_bar)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Instructions
        instructions_group = QGroupBox("Instructions")
        instructions_layout = QVBoxLayout()
        
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml("""
        <h3>CSV Format Requirements:</h3>
        <p>Your CSV file should have the following columns:</p>
        <ul>
            <li><b>Equipment Name</b> (text)</li>
            <li><b>Type</b> (Pump, Compressor, Valve, HeatExchanger, Reactor, Condenser)</li>
            <li><b>Flowrate</b> (number)</li>
            <li><b>Pressure</b> (number)</li>
            <li><b>Temperature</b> (number)</li>
        </ul>
        <p><b>Sample CSV format:</b></p>
        <pre>
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
        </pre>
        """)
        instructions_layout.addWidget(instructions)
        instructions_group.setLayout(instructions_layout)
        layout.addWidget(instructions_group)
        
        self.setLayout(layout)
        
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.file_path.setText(file_path)
            # Set default dataset name from filename
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            self.dataset_name.setText(base_name)
            self.upload_btn.setEnabled(True)
            
    def upload_file(self):

        if self.main_window.api_client is None:
            QMessageBox.warning(self, "Authentication Required", "Please login first to upload files")
            return
        
        file_path = self.file_path.text()
        dataset_name = self.dataset_name.text() or "Uploaded Dataset"
        
        if not file_path:
            QMessageBox.warning(self, "Error", "Please select a CSV file.")
            return
            
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Error", "Selected file does not exist.")
            return
            
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.upload_btn.setEnabled(False)
        
        # Start upload in background thread
        self.worker = APIWorker(self.main_window.api_client.upload_csv, file_path, dataset_name)
        self.main_window.register_thread(self.worker)  # Register for cleanup
        self.worker.finished.connect(self.on_upload_success)
        self.worker.error.connect(self.on_upload_error)
        self.worker.start()
        
    def on_upload_success(self, result):
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        # Show success message
        QMessageBox.information(self, "Success", "CSV file uploaded successfully!")
        
        # Clear form
        self.file_path.clear()
        self.dataset_name.clear()
        
        # Refresh data in main window
        self.main_window.show_status("Data uploaded successfully")
        
        # Switch to Data Summary tab automatically
        self.main_window.tabs.setCurrentIndex(1)  # Data Summary tab is index 1
        
        # Load the new data
        self.load_current_data()
        
    def on_upload_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        QMessageBox.critical(self, "Upload Failed", f"Error uploading file:\n{error_message}")
        
    def load_current_data(self):
        """Load current equipment data and summary after upload"""
        # Load equipment data
        equipment_worker = APIWorker(self.main_window.api_client.get_equipment)
        self.main_window.register_thread(equipment_worker)  # Register for cleanup
        equipment_worker.finished.connect(self.on_equipment_loaded)
        equipment_worker.error.connect(lambda e: self.main_window.show_status(f"Error loading equipment: {e}"))
        equipment_worker.start()
        
        # Load summary data
        summary_worker = APIWorker(self.main_window.api_client.get_summary)
        self.main_window.register_thread(summary_worker)  # Register for cleanup
        summary_worker.finished.connect(self.on_summary_loaded)
        summary_worker.error.connect(lambda e: self.main_window.show_status(f"Error loading summary: {e}"))
        summary_worker.start()
        
    def on_equipment_loaded(self, equipment_data):
        self.main_window.current_data = equipment_data
        # If summary is already loaded, update the display
        if hasattr(self.main_window, 'current_summary') and self.main_window.current_summary:
            self.main_window.update_data(equipment_data, self.main_window.current_summary)
        self.main_window.show_status("Equipment data loaded")
    
    def on_summary_loaded(self, summary_data):
        self.main_window.current_summary = summary_data
        # If equipment data is already loaded, update the display
        if hasattr(self.main_window, 'current_data') and self.main_window.current_data:
            self.main_window.update_data(self.main_window.current_data, summary_data)
        # Refresh history
        self.main_window.update_history()
        self.main_window.show_status("Summary data loaded")