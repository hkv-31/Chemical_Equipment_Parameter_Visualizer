from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from .models import EquipmentDataset

def generate_pdf_report(dataset):
    """Generate PDF report for equipment dataset"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Chemical Equipment Analysis Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Dataset Info
    story.append(Paragraph(f"Dataset: {dataset.name}", styles['Normal']))
    story.append(Paragraph(f"Uploaded: {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"File: {dataset.file_name}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    story.append(Paragraph("Summary Statistics", heading_style))
    
    summary = dataset.summary_stats
    stats_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', summary.get('total_count', 0)],
    ]
    
    # Add parameter statistics
    param_stats = summary.get('parameter_stats', {})
    for param, stats in param_stats.items():
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(f"{param.title()} Statistics", styles['Heading3']))
        
        param_data = [
            ['Statistic', 'Value'],
            ['Mean', f"{stats.get('mean', 0):.2f}"],
            ['Min', f"{stats.get('min', 0):.2f}"],
            ['Max', f"{stats.get('max', 0):.2f}"],
            ['Std Dev', f"{stats.get('std', 0):.2f}"],
        ]
        
        param_table = Table(param_data, colWidths=[2*inch, 1.5*inch])
        param_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(param_table)
    
    # Equipment Type Distribution
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Equipment Type Distribution", heading_style))
    
    type_dist = summary.get('equipment_type_distribution', {})
    dist_data = [['Equipment Type', 'Count']]
    for eq_type, count in type_dist.items():
        dist_data.append([eq_type, count])
    
    dist_table = Table(dist_data, colWidths=[2*inch, 1.5*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(dist_table)
    
    # Sample Data (first 10 records)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Sample Equipment Data (First 10 Records)", heading_style))
    
    equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
    for eq in dataset.equipments.all()[:10]:
        equipment_data.append([
            eq.equipment_name,
            eq.equipment_type,
            f"{eq.flowrate:.1f}",
            f"{eq.pressure:.1f}",
            f"{eq.temperature:.1f}"
        ])
    
    equipment_table = Table(equipment_data, colWidths=[1.2*inch, 1.2*inch, 0.8*inch, 0.8*inch, 1*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(equipment_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer