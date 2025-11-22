def format_file_size(size_bytes):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def validate_csv_headers(headers):
    """Validate CSV headers"""
    required_headers = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    return all(header in headers for header in required_headers)

def safe_float_conversion(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default