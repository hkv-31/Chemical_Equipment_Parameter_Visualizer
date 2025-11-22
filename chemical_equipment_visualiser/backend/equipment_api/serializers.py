from rest_framework import serializers
from .models import Equipment, EquipmentDataset

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class EquipmentDatasetSerializer(serializers.ModelSerializer):
    equipments = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'name', 'uploaded_at', 'file_name', 'summary_stats', 'equipments']