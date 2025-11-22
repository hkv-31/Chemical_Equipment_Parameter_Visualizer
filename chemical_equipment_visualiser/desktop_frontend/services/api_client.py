import requests
import base64
from PyQt5.QtCore import QThread, pyqtSignal
import json

class APIClient:
    def __init__(self, base_url="http://localhost:8000/api", username="api_user", password="api_password123"):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth_header = self._get_auth_header()
        
    def _get_auth_header(self):
        """Create Basic Auth header"""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}
    
    def _make_request(self, method, endpoint, **kwargs):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        # Add auth header if not provided
        if 'headers' not in kwargs:
            kwargs['headers'] = self.auth_header
        else:
            kwargs['headers'].update(self.auth_header)
            
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def get_api_root(self):
        """Get API root information"""
        response = self._make_request('GET', '/')
        return response.json()
    
    def upload_csv(self, file_path, dataset_name="Uploaded Dataset"):
        """Upload CSV file"""
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file, 'text/csv')}
            data = {'name': dataset_name}
            response = self._make_request('POST', '/upload/', files=files, data=data)
            return response.json()
    
    def get_summary(self):
        """Get data summary"""
        response = self._make_request('GET', '/summary/')
        return response.json()
    
    def get_equipment(self):
        """Get equipment data"""
        response = self._make_request('GET', '/equipment/')
        return response.json()
    
    def get_equipment_types(self):
        """Get equipment type distribution"""
        response = self._make_request('GET', '/equipment-types/')
        return response.json()
    
    def get_history(self):
        """Get upload history"""
        response = self._make_request('GET', '/history/')
        return response.json()
    
    def get_dataset(self, dataset_id):
        """Get specific dataset"""
        response = self._make_request('GET', f'/history/{dataset_id}/')
        return response.json()
    
    def generate_pdf(self, save_path):
        """Generate and download PDF report"""
        response = self._make_request('POST', '/generate-pdf/')
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path

class APIWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, api_method, *args, **kwargs):
        super().__init__()
        self.api_method = api_method
        self.args = args
        self.kwargs = kwargs
        self._is_running = True
        
    def run(self):
        try:
            if not self._is_running:
                return
            result = self.api_method(*self.args, **self.kwargs)
            if self._is_running:
                self.finished.emit(result)
        except Exception as e:
            if self._is_running:
                self.error.emit(str(e))
                
    def stop(self):
        self._is_running = False
        self.quit()
        self.wait(1000)  # Wait up to 1 second for thread to finish