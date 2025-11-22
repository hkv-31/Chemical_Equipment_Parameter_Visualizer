import React, { createContext, useContext, useReducer } from 'react';

const EquipmentContext = createContext();

const initialState = {
  equipmentData: [],
  summary: null,
  history: [],
  loading: false,
  error: null,
  currentDataset: null
};

function equipmentReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'SET_EQUIPMENT_DATA':
      return { ...state, equipmentData: action.payload, error: null, loading: false };
    case 'SET_SUMMARY':
      return { ...state, summary: action.payload, error: null, loading: false };
    case 'SET_HISTORY':
      return { ...state, history: action.payload, error: null, loading: false };
    case 'SET_CURRENT_DATASET':
      return { ...state, currentDataset: action.payload };
    default:
      return state;
  }
}

export function EquipmentProvider({ children }) {
  const [state, dispatch] = useReducer(equipmentReducer, initialState);

  return (
    <EquipmentContext.Provider value={{ state, dispatch }}>
      {children}
    </EquipmentContext.Provider>
  );
}

export function useEquipment() {
  const context = useContext(EquipmentContext);
  if (!context) {
    throw new Error('useEquipment must be used within an EquipmentProvider');
  }
  return context;
}