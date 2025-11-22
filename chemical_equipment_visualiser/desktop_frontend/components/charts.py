from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QGroupBox, QGridLayout, QTextEdit)
from PyQt5.QtCore import Qt
import json

class ChartsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # View type selector
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("View Type:"))
        self.view_selector = QComboBox()
        self.view_selector.addItems([
            "Equipment Type Distribution",
            "Parameter Statistics", 
            "Data Summary"
        ])
        self.view_selector.currentTextChanged.connect(self.update_display)
        control_layout.addWidget(self.view_selector)
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # Display area
        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        layout.addWidget(self.display_area)
        
        self.setLayout(layout)
        
        # Initial message
        self.display_area.setHtml("""
        <div style="text-align: center; padding: 50px; color: #888; font-size: 16px;">
            No data available. Please upload a CSV file first.
        </div>
        """)
        
    def update_data(self, equipment_data, summary_data):
        """Update display with new data"""
        self.equipment_data = equipment_data
        self.summary_data = summary_data
        
        if equipment_data and summary_data:
            self.update_display()
        else:
            self.display_area.setHtml("""
            <div style="text-align: center; padding: 50px; color: #888; font-size: 16px;">
                No data available. Please upload a CSV file first.
            </div>
            """)
            
    def update_display(self):
        """Update display based on selected view"""
        if not hasattr(self, 'equipment_data') or not self.equipment_data:
            return
            
        view_type = self.view_selector.currentText()
        
        if view_type == "Equipment Type Distribution":
            self.show_type_distribution()
        elif view_type == "Parameter Statistics":
            self.show_parameter_stats()
        elif view_type == "Data Summary":
            self.show_data_summary()
            
    def show_type_distribution(self):
        """Show equipment type distribution as text"""
        type_distribution = self.summary_data.get('equipment_type_distribution', {})
        
        html = """
        <div style="font-family: Arial, sans-serif; color: white;">
            <h2 style="color: #4BC0C0; text-align: center;">Equipment Type Distribution</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px;">
        """
        
        total_count = self.summary_data.get('total_count', 0)
        
        for eq_type, count in type_distribution.items():
            percentage = (count / total_count * 100) if total_count > 0 else 0
            html += f"""
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                        padding: 20px; border-radius: 10px; text-align: center; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 32px; font-weight: bold; color: white;">{count}</div>
                <div style="color: #e0e0e0; font-size: 14px; text-transform: capitalize;">{eq_type}</div>
                <div style="color: #FFCE56; font-size: 12px; margin-top: 5px;">{percentage:.1f}% of total</div>
            </div>
            """
            
        html += """
            </div>
        </div>
        """
        
        self.display_area.setHtml(html)
        
    def show_parameter_stats(self):
        """Show parameter statistics"""
        param_stats = self.summary_data.get('parameter_stats', {})
        
        html = """
        <div style="font-family: Arial, sans-serif; color: white;">
            <h2 style="color: #4BC0C0; text-align: center;">Parameter Statistics</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px;">
        """
        
        colors = ['#FF6384', '#36A2EB', '#FFCE56']
        color_index = 0
        
        for param, stats in param_stats.items():
            color = colors[color_index % len(colors)]
            color_index += 1
            
            html += f"""
            <div style="background: #404040; padding: 20px; border-radius: 10px; 
                        border-left: 5px solid {color};">
                <h3 style="color: {color}; margin-top: 0; text-transform: capitalize;">{param}</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
                    <div style="color: #b0b0b0;">Mean:</div>
                    <div style="color: white; font-weight: bold;">{stats['mean']:.2f}</div>
                    
                    <div style="color: #b0b0b0;">Minimum:</div>
                    <div style="color: white; font-weight: bold;">{stats['min']:.2f}</div>
                    
                    <div style="color: #b0b0b0;">Maximum:</div>
                    <div style="color: white; font-weight: bold;">{stats['max']:.2f}</div>
                    
                    <div style="color: #b0b0b0;">Std Deviation:</div>
                    <div style="color: white; font-weight: bold;">{stats['std']:.2f}</div>
                </div>
            </div>
            """
            
        html += """
            </div>
        </div>
        """
        
        self.display_area.setHtml(html)
        
    def show_data_summary(self):
        """Show comprehensive data summary"""
        html = """
        <div style="font-family: Arial, sans-serif; color: white;">
            <h2 style="color: #4BC0C0; text-align: center;">Complete Data Summary</h2>
        """
        
        # Overall statistics
        total_count = self.summary_data.get('total_count', 0)
        type_count = len(self.summary_data.get('equipment_type_distribution', {}))
        
        html += f"""
        <div style="background: #2a82da; padding: 20px; border-radius: 10px; margin: 20px; text-align: center;">
            <div style="font-size: 24px; font-weight: bold; color: white;">{total_count}</div>
            <div style="color: #e0e0e0;">Total Equipment Records</div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px;">
            <div style="background: #404040; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 20px; font-weight: bold; color: #4BC0C0;">{type_count}</div>
                <div style="color: #b0b0b0;">Equipment Types</div>
            </div>
        """
        
        # Add parameter ranges
        param_stats = self.summary_data.get('parameter_stats', {})
        for param, stats in param_stats.items():
            html += f"""
            <div style="background: #404040; padding: 15px; border-radius: 8px;">
                <div style="color: #FFCE56; font-weight: bold; text-transform: capitalize; margin-bottom: 10px;">{param} Range</div>
                <div style="color: white; font-size: 12px;">
                    {stats['min']:.1f} - {stats['max']:.1f} (Avg: {stats['mean']:.1f})
                </div>
            </div>
            """
            
        html += """
        </div>
        """
        
        # Equipment type details
        type_distribution = self.summary_data.get('equipment_type_distribution', {})
        if type_distribution:
            html += """
            <h3 style="color: #FFCE56; margin: 20px;">Equipment Type Breakdown</h3>
            <div style="background: #404040; padding: 20px; border-radius: 10px; margin: 20px;">
            """
            
            for eq_type, count in type_distribution.items():
                percentage = (count / total_count * 100) if total_count > 0 else 0
                html += f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 8px 0; border-bottom: 1px solid #555;">
                    <span style="color: white; text-transform: capitalize;">{eq_type}</span>
                    <div>
                        <span style="color: #4BC0C0; font-weight: bold;">{count}</span>
                        <span style="color: #888; margin-left: 10px;">({percentage:.1f}%)</span>
                    </div>
                </div>
                """
                
            html += "</div>"
            
        html += "</div>"
        
        self.display_area.setHtml(html)