from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QListWidgetItem,
                             QGroupBox, QMessageBox, QSplitter, QTextEdit)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont
from services.api_client import APIWorker

class HistoryTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        # Don't load history immediately - wait for API client to be ready
        self.loaded = False
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Upload History"))
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_history)
        header_layout.addWidget(self.refresh_btn)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Splitter for list and details
        splitter = QSplitter(Qt.Horizontal)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemSelectionChanged.connect(self.on_dataset_selected)
        splitter.addWidget(self.history_list)
        
        # Details panel
        self.details_panel = QWidget()
        details_layout = QVBoxLayout(self.details_panel)
        
        self.dataset_info = QTextEdit()
        self.dataset_info.setReadOnly(True)
        self.dataset_info.setHtml("""
        <div style="text-align: center; padding: 40px; color: #888;">
            <h3>No history data loaded</h3>
            <p>Click 'Refresh' to load upload history</p>
        </div>
        """)
        details_layout.addWidget(QLabel("Dataset Details:"))
        details_layout.addWidget(self.dataset_info)
        
        self.load_btn = QPushButton("Load This Dataset")
        self.load_btn.clicked.connect(self.load_selected_dataset)
        self.load_btn.setEnabled(False)
        details_layout.addWidget(self.load_btn)
        
        details_layout.addStretch()
        splitter.addWidget(self.details_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 600])
        layout.addWidget(splitter)
        
        self.setLayout(layout)
        
    def showEvent(self, event):
        """Load history when tab is shown for the first time"""
        if not self.loaded and self.main_window.api_client is not None:
            self.load_history()
            self.loaded = True
        super().showEvent(event)
        
    def load_history(self):
        """Load upload history from API"""
        # Check if API client is available
        if self.main_window.api_client is None:
            self.history_list.clear()
            item = QListWidgetItem("Please login first to load history")
            item.setForeground(Qt.red)
            self.history_list.addItem(item)
            return
            
        self.worker = APIWorker(self.main_window.api_client.get_history)
        self.main_window.register_thread(self.worker)
        self.worker.finished.connect(self.on_history_loaded)
        self.worker.error.connect(self.on_history_error)
        self.worker.start()
        
    def on_history_loaded(self, history_data):
        """Handle loaded history data"""
        self.history_list.clear()
        self.main_window.history_data = history_data
        
        if not history_data:
            item = QListWidgetItem("No history available")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.history_list.addItem(item)
            return
            
        for dataset in history_data:
            item_text = f"{dataset['name']}\nUploaded: {dataset['uploaded_at']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, dataset['id'])
            self.history_list.addItem(item)
            
    def on_history_error(self, error_message):
        """Handle history loading error"""
        self.history_list.clear()
        item = QListWidgetItem(f"Error loading history: {error_message}")
        item.setForeground(Qt.red)
        self.history_list.addItem(item)
        
    def on_dataset_selected(self):
        """Handle dataset selection"""
        current_item = self.history_list.currentItem()
        if not current_item or not hasattr(current_item, 'data'):
            self.load_btn.setEnabled(False)
            return
            
        dataset_id = current_item.data(Qt.UserRole)
        if not dataset_id:
            self.load_btn.setEnabled(False)
            return
            
        # Load dataset details
        self.worker = APIWorker(self.main_window.api_client.get_dataset, dataset_id)
        self.main_window.register_thread(self.worker)
        self.worker.finished.connect(self.on_dataset_details_loaded)
        self.worker.error.connect(self.on_dataset_details_error)
        self.worker.start()
        
    def on_dataset_details_loaded(self, dataset):
        """Handle loaded dataset details"""
        self.selected_dataset = dataset
        self.load_btn.setEnabled(True)
        
        # Format dataset info
        info_html = f"""
        <div style="font-family: Arial, sans-serif; color: white;">
            <h3 style="color: #4BC0C0;">{dataset['name']}</h3>
            <p><b>File:</b> {dataset['file_name']}</p>
            <p><b>Uploaded:</b> {dataset['uploaded_at']}</p>
            <p><b>Total Records:</b> {dataset['summary_stats']['total_count']}</p>
            
            <h4 style="color: #FFCE56;">Equipment Distribution:</h4>
        """
        
        for eq_type, count in dataset['summary_stats']['equipment_type_distribution'].items():
            info_html += f"<p style='margin-left: 20px;'>• {eq_type}: <b>{count}</b></p>"
            
        info_html += """
            <h4 style="color: #FFCE56;">Parameter Statistics:</h4>
        """
        
        for param, stats in dataset['summary_stats']['parameter_stats'].items():
            info_html += f"""
            <div style="margin-left: 20px; margin-bottom: 10px;">
                <b>{param.title()}:</b><br>
                <span style="margin-left: 20px;">
                    Mean: {stats['mean']:.2f} | 
                    Min: {stats['min']:.2f} | 
                    Max: {stats['max']:.2f} | 
                    Std: {stats['std']:.2f}
                </span>
            </div>
            """
            
        info_html += "</div>"
        
        self.dataset_info.setHtml(info_html)
        
    def on_dataset_details_error(self, error_message):
        """Handle dataset details error"""
        self.dataset_info.setHtml(f"<div style='color: red;'>Error loading dataset details: {error_message}</div>")
        self.load_btn.setEnabled(False)
        
    def load_selected_dataset(self):
        """Load the selected dataset as current data"""
        if not hasattr(self, 'selected_dataset'):
            return
            
        # Update main window with selected dataset data
        self.main_window.update_data(
            self.selected_dataset['equipments'],
            self.selected_dataset['summary_stats']
        )
        
        # Show success message
        QMessageBox.information(self, "Dataset Loaded", 
                               f"Dataset '{self.selected_dataset['name']}' has been loaded successfully!")
        
        # Switch to data display tab
        self.main_window.tabs.setCurrentIndex(1)  # Data Summary tab