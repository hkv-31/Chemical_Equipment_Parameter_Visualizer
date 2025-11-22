import csv
import json
from io import TextIOWrapper
from .models import Equipment, EquipmentDataset

def analyze_equipment_data(data):
    """Perform analytics on equipment data and return summary statistics"""
    
    flowrates = [float(row['Flowrate']) for row in data]
    pressures = [float(row['Pressure']) for row in data]
    temperatures = [float(row['Temperature']) for row in data]
    types = [row['Type'] for row in data]
    
    # Calculate type distribution
    type_distribution = {}
    for eq_type in types:
        type_distribution[eq_type] = type_distribution.get(eq_type, 0) + 1
    
    # Calculate statistics manually
    def calculate_stats(values):
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        return {
            'mean': mean,
            'min': min(values),
            'max': max(values),
            'std': std_dev
        }
    
    summary = {
        'total_count': len(data),
        'equipment_type_distribution': type_distribution,
        'parameter_stats': {
            'flowrate': calculate_stats(flowrates),
            'pressure': calculate_stats(pressures),
            'temperature': calculate_stats(temperatures)
        }
    }
    
    return summary

def process_csv_file(file, dataset_name="Uploaded Dataset"):
    """Process uploaded CSV file and store in database"""
    
    # Read CSV file using built-in csv module
    csv_reader = csv.DictReader(TextIOWrapper(file, encoding='utf-8'))
    data = list(csv_reader)
    
    # Validate required columns
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    if not all(col in data[0].keys() for col in required_columns):
        raise ValueError("CSV file missing required columns")
    
    # Perform analysis
    summary_stats = analyze_equipment_data(data)
    
    # Create dataset record
    dataset = EquipmentDataset.objects.create(
        name=dataset_name,
        file_name=file.name,
        summary_stats=summary_stats
    )
    
    # Create equipment records
    equipment_objects = []
    for row in data:
        equipment_objects.append(Equipment(
            dataset=dataset,
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=float(row['Flowrate']),
            pressure=float(row['Pressure']),
            temperature=float(row['Temperature'])
        ))
    
    Equipment.objects.bulk_create(equipment_objects)
    
    # Enforce 5 dataset limit
    datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')
    if len(datasets) > 5:
        for old_dataset in datasets[5:]:
            old_dataset.delete()
    
    return dataset