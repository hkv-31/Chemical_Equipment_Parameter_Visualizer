import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

// Add authentication (you'll need to set this up based on your Django auth)
// For basic auth, you can set it like this:
// api.defaults.auth = { username: 'admin', password: 'password' }

// Alternatively, use session-based auth if you're using Django sessions
// The proxy in package.json will handle CORS for development

export const equipmentAPI = {
  // Upload CSV file
  uploadCSV: async (file, name = 'Uploaded Dataset') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    
    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get summary statistics
  getSummary: async () => {
    const response = await api.get('/summary/');
    return response.data;
  },

  // Get equipment data
  getEquipment: async () => {
    const response = await api.get('/equipment/');
    return response.data;
  },

  // Get equipment type distribution
  getEquipmentTypes: async () => {
    const response = await api.get('/equipment-types/');
    return response.data;
  },

  // Get upload history
  getHistory: async () => {
    const response = await api.get('/history/');
    return response.data;
  },

  // Get specific dataset
  getDataset: async (datasetId) => {
    const response = await api.get(`/history/${datasetId}/`);
    return response.data;
  },

  // Generate PDF report
  generatePDF: async () => {
    const response = await api.post('/generate-pdf/', {}, {
      responseType: 'blob'
    });
    return response.data;
  }
};

export default api;