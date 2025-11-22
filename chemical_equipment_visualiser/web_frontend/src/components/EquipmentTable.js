import React, { useEffect, useState } from 'react';
import { equipmentAPI } from '../services/api';
import { useEquipment } from '../services/EquipmentContext';

function EquipmentTable() {
  const { state, dispatch } = useEquipment();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEquipment();
  }, []);

  const fetchEquipment = async () => {
    setLoading(true);
    try {
      const equipment = await equipmentAPI.getEquipment();
      dispatch({ type: 'SET_EQUIPMENT_DATA', payload: equipment });
    } catch (error) {
      console.error('Error fetching equipment:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading equipment data...</div>;
  if (!state.equipmentData || state.equipmentData.length === 0) {
    return <div className="card">No equipment data available. Please upload a CSV file first.</div>;
  }

  return (
    <div className="card">
      <h2>Equipment Data Table</h2>
      <p>Showing {state.equipmentData.length} equipment records</p>
      
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {state.equipmentData.map((equipment, index) => (
              <tr key={index}>
                <td>{equipment.equipment_name}</td>
                <td style={{ textTransform: 'capitalize' }}>{equipment.equipment_type}</td>
                <td>{equipment.flowrate}</td>
                <td>{equipment.pressure}</td>
                <td>{equipment.temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EquipmentTable;