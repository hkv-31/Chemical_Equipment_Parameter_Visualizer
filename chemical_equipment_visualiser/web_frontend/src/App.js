import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import DataSummary from './components/DataSummary';
import EquipmentTable from './components/EquipmentTable';
import Charts from './components/Charts';
import History from './components/History';
import { EquipmentProvider } from './services/EquipmentContext';

function App() {
  const [activeTab, setActiveTab] = useState('upload');

  return (
    <EquipmentProvider>
      <div className="App">
        <header className="app-header">
          <h1>Chemical Equipment Visualizer</h1>
          <nav className="nav-tabs">
            <button 
              className={activeTab === 'upload' ? 'active' : ''} 
              onClick={() => setActiveTab('upload')}
            >
              Upload CSV
            </button>
            <button 
              className={activeTab === 'summary' ? 'active' : ''} 
              onClick={() => setActiveTab('summary')}
            >
              Summary
            </button>
            <button 
              className={activeTab === 'table' ? 'active' : ''} 
              onClick={() => setActiveTab('table')}
            >
              Data Table
            </button>
            <button 
              className={activeTab === 'charts' ? 'active' : ''} 
              onClick={() => setActiveTab('charts')}
            >
              Charts
            </button>
            <button 
              className={activeTab === 'history' ? 'active' : ''} 
              onClick={() => setActiveTab('history')}
            >
              History
            </button>
          </nav>
        </header>

        <main className="app-main">
          {activeTab === 'upload' && <FileUpload />}
          {activeTab === 'summary' && <DataSummary />}
          {activeTab === 'table' && <EquipmentTable />}
          {activeTab === 'charts' && <Charts />}
          {activeTab === 'history' && <History />}
        </main>
      </div>
    </EquipmentProvider>
  );
}

export default App;