from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Equipment, EquipmentDataset
from .serializers import EquipmentSerializer, EquipmentDatasetSerializer
from .utils import process_csv_file
from .pdf_generator import generate_pdf_report
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Handle CSV file upload and processing"""
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
        
        dataset_name = request.data.get('name', 'Uploaded Dataset')
        dataset = process_csv_file(file, dataset_name)
        
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    """Get summary statistics from the latest dataset"""
    try:
        latest_dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()
        if not latest_dataset:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(latest_dataset.summary_stats)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment_data(request):
    """Get all equipment data from the latest dataset"""
    try:
        latest_dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()
        if not latest_dataset:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        
        equipment = latest_dataset.equipments.all()
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment_types(request):
    """Get equipment type distribution"""
    try:
        latest_dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()
        if not latest_dataset:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        
        distribution = latest_dataset.summary_stats.get('equipment_type_distribution', {})
        return Response(distribution)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """Get upload history (last 5 datasets)"""
    datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, dataset_id):
    """Get specific dataset details"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id)
        serializer = EquipmentDatasetSerializer(dataset)
        return Response(serializer.data)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_pdf(request):
    """Generate PDF report for the latest dataset"""
    try:
        latest_dataset = EquipmentDataset.objects.order_by('-uploaded_at').first()
        if not latest_dataset:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        
        pdf_buffer = generate_pdf_report(latest_dataset)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{latest_dataset.id}.pdf"'
        return response
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)