# Animal Shelter Management System

**Live Demo:** https://animal-shelter-app-project.streamlit.app/  

## Overview
This project implements an Animal Shelter Management System with a MySQL database back‑end and a Streamlit web front‑end. It supports two perspectives:

- **Guest View** – browse available animals with filters (species, status, shelter location).  
- **Staff View** – manage animals, vaccinations, and vaccine stock (read‑only in Streamlit Cloud).  

## Objective
To design and deploy a database‑driven system that streamlines animal shelter operations, enabling public browsing and staff management through a user‑friendly web interface.

## Features
- **Database Layer (MySQL)**  
  - Normalized schema with 5 tables (shelters, animals, employees, vaccines, vaccination_record)  
  - Primary/foreign keys, indexes, triggers, and views for automation and reporting  
  - Advanced SQL queries (joins, CTEs, window functions)  

- **Web Application (Streamlit)**  
  - Multi‑tab interface for guest and staff workflows  
  - Animal photo display with responsive layout  
  - CSV snapshots for cloud deployment compatibility  

## System Architecture
- **Database:** MySQL stores shelters, animals, employees, vaccines, and vaccination records.  
- **Application:** Streamlit loads CSV exports and provides guest/staff dashboards.  

## Entity‑Relationship Diagram
![EER Diagram](schema_diagram.png)

## Deployment
- Cloud deployment via Streamlit Cloud  
- Accessible demo link for grading
  
## Testing

- All SQL scripts were tested locally using MySQL Workbench to verify schema integrity, data relationships, and query correctness.  
- The Streamlit application was tested in both local and cloud environments to ensure UI functionality, CSV compatibility, and image rendering.

## Security

Basic security measures were implemented for the Streamlit app, including:
- Password-based login for staff mode (fixed password for demo purposes)
- Role separation between guest and staff views
- Cloud deployment with Streamlit’s built-in sandboxing

Note: For demonstration purposes, authentication is simplified for clarity. In a production system, role-based access control and secure credential storage would be required.

## Future Improvements
- Full CRUD integration with live MySQL  
- Role‑based staff authentication  
- File upload for animal photos  
- Automated notifications for overdue vaccinations  

## Author
Maria Savostianova  
University of Central Missouri
5200 Database Theory and Apps
Final Project

