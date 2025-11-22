import React, { useState } from 'react';
import { equipmentAPI } from '../services/api';
import { useEquipment } from '../services/EquipmentContext';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [datasetName, setDatasetName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const { dispatch } = useEquipment();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setDatasetName(selectedFile.name.replace('.csv', ''));
      setMessage('');
    } else {
      setMessage('Please select a valid CSV file.');
      setFile(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const result = await equipmentAPI.uploadCSV(file, datasetName);
      setMessage('File uploaded successfully!');
      setFile(null);
      setDatasetName('');
      
      // Refresh data
      dispatch({ type: 'SET_CURRENT_DATASET', payload: result });
      
    } catch (error) {
      setMessage(`Upload failed: ${error.response?.data?.error || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload CSV File</h2>
      
      {message && (
        <div className={message.includes('failed') ? 'error' : 'success'}>
          {message}
        </div>
      )}

      <form onSubmit={handleUpload}>
        <div className="form-group">
          <label htmlFor="csvFile">Select CSV File:</label>
          <input
            type="file"
            id="csvFile"
            accept=".csv"
            onChange={handleFileChange}
            className="form-control"
            disabled={uploading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="datasetName">Dataset Name:</label>
          <input
            type="text"
            id="datasetName"
            value={datasetName}
            onChange={(e) => setDatasetName(e.target.value)}
            className="form-control"
            placeholder="Enter a name for this dataset"
            disabled={uploading}
          />
        </div>

        <button 
          type="submit" 
          className="btn" 
          disabled={!file || uploading}
        >
          {uploading ? 'Uploading...' : 'Upload CSV'}
        </button>
      </form>

      <div style={{ marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '5px' }}>
        <h3>CSV Format Requirements:</h3>
        <p>Your CSV file should have the following columns:</p>
        <ul>
          <li><strong>Equipment Name</strong> (text)</li>
          <li><strong>Type</strong> (Pump, Compressor, Valve, HeatExchanger, Reactor, Condenser)</li>
          <li><strong>Flowrate</strong> (number)</li>
          <li><strong>Pressure</strong> (number)</li>
          <li><strong>Temperature</strong> (number)</li>
        </ul>
      </div>
    </div>
  );
}

export default FileUpload;