from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload-csv'),
    path('summary/', views.get_summary, name='get-summary'),
    path('equipment/', views.get_equipment_data, name='get-equipment'),
    path('equipment-types/', views.get_equipment_types, name='get-equipment-types'),
    path('history/', views.get_history, name='get-history'),
    path('history/<int:dataset_id>/', views.get_dataset_detail, name='get-dataset-detail'),
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
]