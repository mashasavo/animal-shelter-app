# Animal Shelter Management System

**Live Demo:**  
https://animal-shelter-app-project.streamlit.app/

**GitHub Repository:**  
[ADD YOUR REPOSITORY LINK HERE]

---

## Objective

To design and implement a database-driven application that manages animals, shelters, employees, vaccines, and vaccination records. The system is built using a normalized MySQL database and a Streamlit web interface, with CSV snapshots exported from MySQL for cloud execution.

---

## Overview

This project demonstrates a complete Animal Shelter Management System with two main user perspectives:

### Guest View
- Browse animals  
- Filter by species, size, status, and shelter  
- View animal profiles and images  

### Staff View
- Manage animal records (add, update status, delete)  
- Review vaccine inventory and stock levels  
- View upcoming and overdue vaccinations  

Streamlit Cloud does not support direct database connectivity; therefore, the cloud demo utilizes CSV snapshots derived from the MySQL database. The intended production setup connects Streamlit directly to MySQL.

---

## Features

### Database Layer (MySQL)

- Five interconnected tables:  
  `shelters`, `animals`, `employees`, `vaccines`, `vaccination_record`
- Proper primary/foreign key relationships  
- ENUM validation for controlled fields  
- Indexes for filter-heavy queries  
- Trigger to automatically decrement vaccine stock  
- Stored view consolidating vaccination history  
- Advanced SQL, including:  
  - Window functions  
  - Recursive CTE  
  - Aggregation and grouping  
  - Join operations  
- All SQL scripts tested in MySQL Workbench

---

### Application Layer (Streamlit)

The Streamlit application mirrors real shelter workflows using a clean tab-based layout:

- Guest browsing with filters and animal images  
- Staff operations:
  - Add new animals  
  - Update status  
  - Delete animals  
  - View vaccine stock  
  - Review upcoming vaccinations  
- CSV-based data loading (`/data` folder) for cloud deployment  
- Card-style UI for animal profiles  
- Structured, readable layout designed for usability

---

### Images

- Stored in `data/images/.`  
- Mapped to animals by naming convention  
- Automatically displayed in the application

---

## Application Architecture

### Backend (MySQL)
- Normalized schema with constraints and relationships  
- Trigger for stock management  
- View for vaccination reporting  
- Intended to serve as the authoritative data source

### Data Pipeline
- MySQL data exported to CSV snapshots  
- CSVs stored under `data/.`  
- Streamlit Cloud loads CSVs due to cloud limitations on SQL connections  

### Frontend (Streamlit)
- Python-based UI served through Streamlit  
- Loads CSV files at runtime  
- Renders tables, cards, filters, and image components  
- Designed for both local and cloud execution

---

## Entity-Relationship Diagram

```md
![Schema Diagram](schema_diagram.png)

## Included SQL Scripts

final_forward_engineer.sql   # Schema creation, tables, relationships
queries_advanced.sql         # Trigger, view, analytical queries

## Repository Structure

data/                         # CSV exports used by Streamlit
    images/                   # Animal photos
.gitignore
README.md
app.py                        # Streamlit application
config.toml                   # Streamlit configuration
final_forward_engineer.sql
queries_advanced.sql
requirements.txt              # Python dependencies
schema_diagram.png            # EER diagram

## Testing and Security

- SQL scripts tested in MySQL Workbench
- Streamlit application tested locally and in Streamlit Cloud
- Basic guest vs staff separation in the UI
- Authentication simplified for academic demonstration
-- A production system would require:
- Secure credential storage
- Authentication
- Role-based access control

## Deployment
- Set up and populate MySQL using the provided scripts
- Install dependencies:
pip install -r requirements.txt
- Run the app:
streamlit run app.py

## Streamlit Cloud Deployment

- Uses CSVs from the data/ directory
- No database server required

## Future Enhancements

- Full CRUD integration with a live MySQL backend
- Staff login and authorization
- Direct image upload support
- Cloud image storage
- Automated vaccination reminders
- Advanced analytics

## Author

Maria Savostianova
University of Central Missouri
Database Theory and Applications — Final Project





