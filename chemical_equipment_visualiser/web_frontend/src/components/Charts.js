import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { equipmentAPI } from '../services/api';
import { useEquipment } from '../services/EquipmentContext';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function Charts() {
  const { state } = useEquipment();
  const [typeDistribution, setTypeDistribution] = useState({});

  useEffect(() => {
    fetchTypeDistribution();
  }, []);

  const fetchTypeDistribution = async () => {
    try {
      const distribution = await equipmentAPI.getEquipmentTypes();
      setTypeDistribution(distribution);
    } catch (error) {
      console.error('Error fetching type distribution:', error);
    }
  };

  const typeDistributionData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        data: Object.values(typeDistribution),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
        ],
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  const parameterComparisonData = {
    labels: state.equipmentData.map(eq => eq.equipment_name),
    datasets: [
      {
        label: 'Flowrate',
        data: state.equipmentData.map(eq => eq.flowrate),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'Pressure',
        data: state.equipmentData.map(eq => eq.pressure),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Temperature',
        data: state.equipmentData.map(eq => eq.temperature),
        backgroundColor: 'rgba(255, 206, 86, 0.6)',
        borderColor: 'rgba(255, 206, 86, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
    },
  };

  if (!state.equipmentData || state.equipmentData.length === 0) {
    return <div className="card">No data available for charts. Please upload a CSV file first.</div>;
  }

  return (
    <div>
      <div className="card">
        <h2>Data Visualization</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '2rem' }}>
          <div className="chart-container">
            <h3>Equipment Type Distribution</h3>
            <div style={{ height: '300px' }}>
              <Doughnut data={typeDistributionData} options={doughnutOptions} />
            </div>
          </div>

          <div className="chart-container">
            <h3>Parameter Comparison</h3>
            <div style={{ height: '400px' }}>
              <Bar data={parameterComparisonData} options={chartOptions} />
            </div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '2rem' }}>
          {Object.entries(state.summary?.parameter_stats || {}).map(([parameter, stats]) => (
            <div key={parameter} className="chart-container">
              <h3 style={{ textTransform: 'capitalize' }}>{parameter} Statistics</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.9rem' }}>
                <div>Average:</div>
                <div style={{ fontWeight: 'bold' }}>{stats.mean?.toFixed(2)}</div>
                
                <div>Minimum:</div>
                <div style={{ fontWeight: 'bold' }}>{stats.min?.toFixed(2)}</div>
                
                <div>Maximum:</div>
                <div style={{ fontWeight: 'bold' }}>{stats.max?.toFixed(2)}</div>
                
                <div>Std Deviation:</div>
                <div style={{ fontWeight: 'bold' }}>{stats.std?.toFixed(2)}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Charts;