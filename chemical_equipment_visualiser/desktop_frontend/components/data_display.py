from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QGroupBox, QHeaderView, QScrollArea, QGridLayout,
                             QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt
from services.api_client import APIWorker
import json

class DataDisplayTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Debug info
        self.debug_label = QLabel("Debug: No data loaded yet")
        self.debug_label.setStyleSheet("background: yellow; color: black; padding: 5px;")
        layout.addWidget(self.debug_label)
        
        # Header with refresh button
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Data Summary"))
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(self.refresh_btn)
        
        # Force load button
        self.force_load_btn = QPushButton("Force Load All Data")
        self.force_load_btn.clicked.connect(self.force_load_data)
        header_layout.addWidget(self.force_load_btn)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Summary section
        self.summary_group = QGroupBox("Dataset Overview")
        self.summary_layout = QVBoxLayout()
        self.summary_content = QTextEdit()
        self.summary_content.setReadOnly(True)
        self.summary_content.setHtml("""
        <div style="text-align: center; padding: 40px; color: #888;">
            <h3>No data available</h3>
            <p>Please upload a CSV file first or click "Force Load All Data"</p>
        </div>
        """)
        self.summary_layout.addWidget(self.summary_content)
        self.summary_group.setLayout(self.summary_layout)
        layout.addWidget(self.summary_group)
        
        # PDF generation button
        self.pdf_btn = QPushButton("Generate PDF Report")
        self.pdf_btn.clicked.connect(self.generate_pdf)
        self.pdf_btn.setEnabled(False)
        layout.addWidget(self.pdf_btn)
        
        # Data table
        self.table_group = QGroupBox("Equipment Data")
        table_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.data_table)
        self.table_group.setLayout(table_layout)
        layout.addWidget(self.table_group)
        
        self.setLayout(layout)
        
    def showEvent(self, event):
        """When tab is shown, refresh data if none exists"""
        try:
            # Safe check for current_data
            if hasattr(self.main_window, 'current_data') and self.main_window.current_data is not None:
                data_length = len(self.main_window.current_data)
                self.debug_label.setText(f"Debug: Tab shown. Current data: {data_length} items")
                self.update_data(self.main_window.current_data, getattr(self.main_window, 'current_summary', None))
            else:
                self.debug_label.setText("Debug: Tab shown. No data found, refreshing...")
                self.refresh_data()
        except Exception as e:
            self.debug_label.setText(f"Debug: Error in showEvent: {str(e)}")
            self.refresh_data()
        super().showEvent(event)
        
    def refresh_data(self):
        """Manual refresh of data"""
        if self.main_window.api_client is None:
            self.debug_label.setText("Debug: API client not available - please login first")
            QMessageBox.warning(self, "Authentication Required", "Please login first to load data")
            return
    
        self.debug_label.setText("Debug: Starting refresh...")
        self.main_window.show_status("Refreshing data...")
        
        # Load equipment data
        equipment_worker = APIWorker(self.main_window.api_client.get_equipment)
        self.main_window.register_thread(equipment_worker)  # Register for cleanup
        equipment_worker.finished.connect(self.on_equipment_refreshed)
        equipment_worker.error.connect(self.on_refresh_error)
        equipment_worker.start()
        
    def force_load_data(self):
        """Force load both equipment and summary data"""
        self.debug_label.setText("Debug: Force loading all data...")
        
        # Load equipment data
        equipment_worker = APIWorker(self.main_window.api_client.get_equipment)
        self.main_window.register_thread(equipment_worker)  # Register for cleanup
        equipment_worker.finished.connect(self.on_equipment_force_loaded)
        equipment_worker.error.connect(self.on_refresh_error)
        equipment_worker.start()

    def on_equipment_refreshed(self, equipment_data):
        self.debug_label.setText(f"Debug: Equipment data loaded: {len(equipment_data) if equipment_data else 0} items")
        self.main_window.current_data = equipment_data
        self.main_window.show_status("Equipment data refreshed")
        
        # Now load summary data
        summary_worker = APIWorker(self.main_window.api_client.get_summary)
        self.main_window.register_thread(summary_worker)  # Register for cleanup
        summary_worker.finished.connect(self.on_summary_refreshed)
        summary_worker.error.connect(self.on_refresh_error)
        summary_worker.start()

    def on_equipment_force_loaded(self, equipment_data):
        self.debug_label.setText(f"Debug: Equipment data force loaded: {len(equipment_data) if equipment_data else 0} items")
        self.main_window.current_data = equipment_data
        
        # Now load summary data
        summary_worker = APIWorker(self.main_window.api_client.get_summary)
        self.main_window.register_thread(summary_worker)  # Register for cleanup
        summary_worker.finished.connect(self.on_summary_force_loaded)
        summary_worker.error.connect(self.on_refresh_error)
        summary_worker.start()

    def on_summary_refreshed(self, summary_data):
        self.debug_label.setText("Debug: Summary data loaded")
        self.main_window.current_summary = summary_data
        self.main_window.show_status("Summary data refreshed")
        # Update display with new data
        self.update_data(self.main_window.current_data, summary_data)

    def on_summary_force_loaded(self, summary_data):
        self.debug_label.setText("Debug: Summary data force loaded")
        self.main_window.current_summary = summary_data
        # Update display with new data
        self.update_data(self.main_window.current_data, summary_data)
        QMessageBox.information(self, "Success", "Data loaded successfully!")

    def on_refresh_error(self, error_message):
        self.debug_label.setText(f"Debug: Error: {error_message}")
        self.main_window.show_status(f"Error: {error_message}")
        QMessageBox.critical(self, "Error", f"Failed to load data:\n{error_message}")
        
    def update_data(self, equipment_data, summary_data):
        """Update display with new data"""
        try:
            equipment_count = len(equipment_data) if equipment_data else 0
            has_summary = summary_data is not None
            self.debug_label.setText(f"Debug: Updating display - Equipment: {equipment_count}, Summary: {has_summary}")
            
            if not equipment_data or not summary_data:
                self.debug_label.setText("Debug: No data to display")
                self.summary_content.setHtml("""
                <div style="text-align: center; padding: 40px; color: #888;">
                    <h3>No data available</h3>
                    <p>Please upload a CSV file first or click "Force Load All Data"</p>
                </div>
                """)
                self.pdf_btn.setEnabled(False)
                self.data_table.setRowCount(0)
                return
                
            self.debug_label.setText("Debug: Displaying data...")
            self.pdf_btn.setEnabled(True)
            self.update_summary_display(summary_data)
            self.update_table_display(equipment_data)
        except Exception as e:
            self.debug_label.setText(f"Debug: Error in update_data: {str(e)}")
        
    def update_summary_display(self, summary_data):
        """Update the summary display"""
        try:
            summary_html = f"""
            <div style="font-family: Arial, sans-serif; color: white;">
                <h3 style="color: #4BC0C0; margin-bottom: 20px; text-align: center;">Dataset Overview</h3>
                
                <div style="background: #2a82da; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 32px; font-weight: bold; color: white;">{summary_data.get('total_count', 0)}</div>
                    <div style="color: #e0e0e0; font-size: 16px;">Total Equipment Records</div>
                </div>
                
                <h4 style="color: #FFCE56; margin-bottom: 15px;">Equipment Type Distribution</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 25px;">
            """
            
            for eq_type, count in summary_data.get('equipment_type_distribution', {}).items():
                summary_html += f"""
                    <div style="background: #404040; padding: 15px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 24px; font-weight: bold; color: #4BC0C0;">{count}</div>
                        <div style="color: #b0b0b0; text-transform: capitalize; font-size: 14px;">{eq_type}</div>
                    </div>
                """
                
            summary_html += """
                </div>
                
                <h4 style="color: #FFCE56; margin-bottom: 15px;">Parameter Statistics</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px;">
            """
            
            colors = ['#FF6384', '#36A2EB', '#FFCE56']
            color_index = 0
            
            for param, stats in summary_data.get('parameter_stats', {}).items():
                color = colors[color_index % len(colors)]
                color_index += 1
                
                summary_html += f"""
                    <div style="background: #404040; padding: 20px; border-radius: 10px; border-left: 5px solid {color};">
                        <h5 style="color: {color}; margin: 0 0 15px 0; text-transform: capitalize; font-size: 16px;">{param}</h5>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 14px;">
                            <div style="color: #b0b0b0;">Mean:</div>
                            <div style="color: white; font-weight: bold;">{stats.get('mean', 0):.2f}</div>
                            
                            <div style="color: #b0b0b0;">Minimum:</div>
                            <div style="color: white; font-weight: bold;">{stats.get('min', 0):.2f}</div>
                            
                            <div style="color: #b0b0b0;">Maximum:</div>
                            <div style="color: white; font-weight: bold;">{stats.get('max', 0):.2f}</div>
                            
                            <div style="color: #b0b0b0;">Std Deviation:</div>
                            <div style="color: white; font-weight: bold;">{stats.get('std', 0):.2f}</div>
                        </div>
                    </div>
                """
                
            summary_html += """
                </div>
            </div>
            """
            
            self.summary_content.setHtml(summary_html)
            self.debug_label.setText("Debug: Summary display updated successfully")
            
        except Exception as e:
            self.debug_label.setText(f"Debug: Error in summary display: {str(e)}")
            self.summary_content.setHtml(f"""
            <div style="color: red; padding: 20px;">
                <h3>Error displaying summary</h3>
                <p>{str(e)}</p>
            </div>
            """)
        
    def update_table_display(self, equipment_data):
        """Update the table with equipment data"""
        try:
            if not equipment_data:
                self.debug_label.setText("Debug: No equipment data for table")
                return
                
            self.debug_label.setText(f"Debug: Updating table with {len(equipment_data)} items")
            
            # Set table dimensions
            self.data_table.setRowCount(len(equipment_data))
            self.data_table.setColumnCount(5)
            self.data_table.setHorizontalHeaderLabels([
                "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
            ])
            
            # Populate table
            for row, equipment in enumerate(equipment_data):
                self.data_table.setItem(row, 0, QTableWidgetItem(str(equipment.get('equipment_name', ''))))
                self.data_table.setItem(row, 1, QTableWidgetItem(str(equipment.get('equipment_type', ''))))
                self.data_table.setItem(row, 2, QTableWidgetItem(str(equipment.get('flowrate', ''))))
                self.data_table.setItem(row, 3, QTableWidgetItem(str(equipment.get('pressure', ''))))
                self.data_table.setItem(row, 4, QTableWidgetItem(str(equipment.get('temperature', ''))))
                
            # Adjust column widths
            header = self.data_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            
            self.debug_label.setText("Debug: Table updated successfully")
            
        except Exception as e:
            self.debug_label.setText(f"Debug: Error in table display: {str(e)}")
        
    def generate_pdf(self):
        """Generate PDF report"""
        from PyQt5.QtWidgets import QFileDialog
        
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", "equipment_report.pdf", "PDF Files (*.pdf)"
        )
        
        if save_path:
            self.worker = APIWorker(self.main_window.api_client.generate_pdf, save_path)
            self.main_window.register_thread(self.worker)  # Register for cleanup
            self.worker.finished.connect(self.on_pdf_generated)
            self.worker.error.connect(self.on_pdf_error)
            self.worker.start()
            
    def on_pdf_generated(self, file_path):
        self.debug_label.setText(f"Debug: PDF generated: {file_path}")
        self.main_window.show_status(f"PDF report saved: {file_path}")
        QMessageBox.information(self, "Success", f"PDF report generated successfully!\n\nSaved to: {file_path}")
        
    def on_pdf_error(self, error_message):
        self.debug_label.setText(f"Debug: PDF error: {error_message}")
        self.main_window.show_status(f"PDF generation failed: {error_message}")
        QMessageBox.critical(self, "Error", f"Failed to generate PDF report:\n{error_message}")

    