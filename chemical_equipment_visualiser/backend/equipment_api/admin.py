from django.contrib import admin
from .models import EquipmentDataset, Equipment

class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 0

@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at', 'file_name']
    inlines = [EquipmentInline]

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']