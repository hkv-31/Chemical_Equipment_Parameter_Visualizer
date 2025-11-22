import React, { useEffect, useState } from 'react';
import { equipmentAPI } from '../services/api';
import { useEquipment } from '../services/EquipmentContext';

function History() {
  const { state, dispatch } = useEquipment();
  const [loading, setLoading] = useState(false);
  const [selectedDataset, setSelectedDataset] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const history = await equipmentAPI.getHistory();
      dispatch({ type: 'SET_HISTORY', payload: history });
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadDataset = async (datasetId) => {
    try {
      const dataset = await equipmentAPI.getDataset(datasetId);
      setSelectedDataset(dataset);
      
      // Update current data with selected dataset
      dispatch({ type: 'SET_EQUIPMENT_DATA', payload: dataset.equipments });
      dispatch({ type: 'SET_SUMMARY', payload: dataset.summary_stats });
      dispatch({ type: 'SET_CURRENT_DATASET', payload: dataset });
      
    } catch (error) {
      console.error('Error loading dataset:', error);
    }
  };

  if (loading) return <div className="loading">Loading history...</div>;

  return (
    <div className="card">
      <h2>Upload History</h2>
      <p>Last 5 uploaded datasets</p>

      {state.history.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
          No upload history available.
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
          {state.history.map((dataset) => (
            <div
              key={dataset.id}
              style={{
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                padding: '1rem',
                background: selectedDataset?.id === dataset.id ? '#f0f9ff' : 'white',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
              }}
              onClick={() => loadDataset(dataset.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                <h3 style={{ margin: 0, color: '#333' }}>{dataset.name}</h3>
                <span style={{ color: '#666', fontSize: '0.9rem' }}>
                  {new Date(dataset.uploaded_at).toLocaleDateString()}
                </span>
              </div>
              
              <div style={{ color: '#666', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                File: {dataset.file_name}
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '1rem', fontSize: '0.8rem' }}>
                <div>
                  <strong>Total Records:</strong> {dataset.summary_stats.total_count}
                </div>
                <div>
                  <strong>Equipment Types:</strong> {Object.keys(dataset.summary_stats.equipment_type_distribution || {}).length}
                </div>
              </div>

              {selectedDataset?.id === dataset.id && (
                <div style={{ marginTop: '1rem', padding: '1rem', background: '#e8f4fd', borderRadius: '5px' }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>Currently Loaded</div>
                  <div style={{ fontSize: '0.9rem' }}>
                    This dataset is now active. You can view its data in the Summary, Table, and Charts tabs.
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {selectedDataset && (
        <div style={{ marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '5px' }}>
          <h3>Current Dataset: {selectedDataset.name}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            {Object.entries(selectedDataset.summary_stats.equipment_type_distribution || {}).map(([type, count]) => (
              <div key={type} style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#667eea' }}>{count}</div>
                <div style={{ color: '#666', textTransform: 'capitalize' }}>{type}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default History;