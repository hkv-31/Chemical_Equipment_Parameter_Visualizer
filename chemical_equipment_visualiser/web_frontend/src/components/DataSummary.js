import React, { useEffect, useState } from 'react';
import { equipmentAPI } from '../services/api';
import { useEquipment } from '../services/EquipmentContext';

function DataSummary() {
  const { state, dispatch } = useEquipment();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    setLoading(true);
    try {
      const summary = await equipmentAPI.getSummary();
      dispatch({ type: 'SET_SUMMARY', payload: summary });
    } catch (error) {
      console.error('Error fetching summary:', error);
    } finally {
      setLoading(false);
    }
  };

  const generatePDF = async () => {
    try {
      const pdfBlob = await equipmentAPI.generatePDF();
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'equipment_report.pdf';
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error generating PDF report');
    }
  };

  if (loading) return <div className="loading">Loading summary...</div>;
  if (!state.summary) return <div className="card">No data available. Please upload a CSV file first.</div>;

  const { summary } = state;

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2>Data Summary</h2>
        <button className="btn" onClick={generatePDF}>
          Generate PDF Report
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ background: '#e8f4fd', padding: '1rem', borderRadius: '8px' }}>
          <h3 style={{ color: '#1890ff', marginBottom: '0.5rem' }}>Total Equipment</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1890ff' }}>
            {summary.total_count}
          </p>
        </div>
      </div>

      <h3>Equipment Type Distribution</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        {Object.entries(summary.equipment_type_distribution || {}).map(([type, count]) => (
          <div key={type} style={{ background: '#f0f9ff', padding: '1rem', borderRadius: '8px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#667eea' }}>{count}</div>
            <div style={{ color: '#666', textTransform: 'capitalize' }}>{type}</div>
          </div>
        ))}
      </div>

      <h3>Parameter Statistics</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {Object.entries(summary.parameter_stats || {}).map(([parameter, stats]) => (
          <div key={parameter} style={{ background: '#f8f9fa', padding: '1.5rem', borderRadius: '8px' }}>
            <h4 style={{ textTransform: 'capitalize', marginBottom: '1rem', color: '#333' }}>{parameter}</h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
              <div>Mean:</div>
              <div style={{ fontWeight: 'bold' }}>{stats.mean?.toFixed(2)}</div>
              
              <div>Min:</div>
              <div style={{ fontWeight: 'bold' }}>{stats.min?.toFixed(2)}</div>
              
              <div>Max:</div>
              <div style={{ fontWeight: 'bold' }}>{stats.max?.toFixed(2)}</div>
              
              <div>Std Dev:</div>
              <div style={{ fontWeight: 'bold' }}>{stats.std?.toFixed(2)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DataSummary;