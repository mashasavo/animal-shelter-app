# Animal Shelter Management System

**Live Demo:** https://animal-shelter-app-project.streamlit.app/  

## Overview
This project implements an Animal Shelter Management System with a MySQL database back‑end and a Streamlit web front‑end. It supports two perspectives:

- **Guest View** – browse available animals with filters (species, status, shelter location).  
- **Staff View** – manage animals, vaccinations, and vaccine stock (read‑only in Streamlit Cloud).  

## Objective
To design and deploy a database‑driven system that streamlines animal shelter operations, enabling public browsing and staff management through a user‑friendly web interface.

## Features
- **Database (MySQL)** – normalized schema with 5 tables, keys, triggers, views, and advanced SQL queries  
- **Web App (Streamlit + Python/Pandas)** – guest/staff dashboards, animal photo display, CSV snapshots for cloud deployment  
- **Architecture** – MySQL stores shelters, animals, employees, vaccines, and vaccination records; Streamlit loads CSV exports  

## Entity‑Relationship Diagram
![EER Diagram](schema_diagram.png)

## Deployment
- Cloud deployment via Streamlit Cloud  
- Accessible demo link for grading  

## Testing & Security
- SQL scripts tested in MySQL Workbench; Streamlit tested locally and in the cloud  
- Basic security: staff login with fixed password, guest/staff role separation  
- Note: Authentication simplified for demo; production would require role‑based access and secure credential storage  

## Future Improvements
- Full CRUD integration with live MySQL  
- Role‑based staff authentication  
- File upload for animal photos  
- Automated notifications for overdue vaccinations  

## Author
Maria Savostianova  
University of Central Missouri – Database Theory and Apps Final Project

