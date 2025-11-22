# Chemical Equipment Parameter Visualizer

A hybrid web + desktop application for visualizing and analyzing chemical equipment data. Built with Django REST API, React.js web frontend, and PyQt5 desktop frontend.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![React](https://img.shields.io/badge/React-18-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green)

## Features

### Core Functionality
- **CSV Data Upload** - Process chemical equipment data from CSV files
- **Real-time Analytics** - Calculate statistics (mean, min, max, standard deviation)
- **Data Visualization** - Interactive charts and graphs
- **Multi-Platform** - Web and desktop interfaces from single backend
- **PDF Report Generation** - Export comprehensive analysis reports
- **Data History** - Store and manage last 5 uploaded datasets

### Web Application (React.js)
- Responsive design with Chart.js visualizations
- Tab-based navigation for different data views
- Real-time data updates
- Modern UI with dark theme support

### Desktop Application (PyQt5)
- Native desktop experience with dark theme
- Matplotlib-based charts and visualizations
- File system integration
- Threaded API calls for responsive UI

## Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (easily switchable to PostgreSQL)
- **ReportLab** - PDF generation
- **Basic Authentication** - API security

### Web Frontend
- **React 18** - UI library
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **CSS3** - Styling with modern features

### Desktop Frontend
- **PyQt5** - Desktop application framework
- **Matplotlib** - Scientific plotting
- **Requests** - HTTP library

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Backend Setup

# Clone repository
git clone <repository-url>
cd chemical_equipment_visualizer/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (for API access)
python manage.py createsuperuser

# Start development server
python manage.py runserver

### Web Frontend Setup
cd ../web-frontend

# Install dependencies
npm install

# Start development server
npm start

### Desktop Application Setup
cd ../desktop-frontend

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py

### Usage
Web Application
1. Access at http://localhost:3000
2. Upload CSV file with equipment data
3. Navigate through tabs to view:
4. Summary: Statistical overview
5. Data Table: Raw equipment data
6. Charts: Interactive visualizations
7. History: Previous uploads

## Desktop Application
1. Run python main.py from desktop-frontend
2. Login with Django credentials
3. Use tab-based interface similar to web app
4. Generate PDF reports with one click
