from django.db import models
import json

class EquipmentDataset(models.Model):
    name = models.CharField(max_length=255, default="Untitled Dataset")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    
    # Store summary statistics as JSON
    summary_stats = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('Pump', 'Pump'),
        ('Compressor', 'Compressor'),
        ('Valve', 'Valve'),
        ('HeatExchanger', 'Heat Exchanger'),
        ('Reactor', 'Reactor'),
        ('Condenser', 'Condenser'),
    ]
    
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='equipments')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return self.equipment_name