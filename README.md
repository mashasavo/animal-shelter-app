# Animal Shelter Management System

**Live Demo:** [Streamlit App](https://animal-shelter-app-project.streamlit.app/)  

## Overview
This project implements an Animal Shelter Management System with a **MySQL database back‑end** and a **Streamlit web front‑end**.  

It supports two perspectives:
- **Guest View** – browse available animals with filters such as species, status, and shelter location.  
- **Staff View** – view animals, vaccinations, and vaccine stock levels (read‑only in Streamlit Cloud).  

The Streamlit app uses **CSV snapshots** exported from the MySQL database to ensure compatibility with cloud deployment.

## Objective
Design and deploy a database‑driven system that streamlines animal shelter operations by combining structured relational data with a user‑friendly web interface.

## Features

### Database (MySQL)
- Normalized relational schema  
- Five main tables: `shelters`, `animals`, `employees`, `vaccines`, `vaccination_record.`  
- Primary and foreign keys ensuring referential integrity  
- ENUM constraints for controlled fields  
- Indexes for commonly queried attributes  
- Trigger for automatic stock updates  
- Reporting view for vaccination history  
- Advanced SQL queries (CTE, window functions, aggregations)  

### Web Application (Streamlit + Python/Pandas)
- Multi‑tab interface for guests and staff  
- Card‑style animal browsing with search and filtering  
- Vaccination and stock summaries  
- Data loaded from CSV exports  
- Responsive layout for clarity and presentation  

### Images
- Animal photographs stored in `data/images/` and mapped to each animal by name  
- Future versions could store filenames in the database for upload support  

## Entity‑Relationship Diagram
(Insert your EER image here once uploaded to the repository.)

Example:

![EER Diagram](eer_diagram.png)

## Database Design
The schema models real shelter operations using the following entities:

1. **shelters** – locations and contact information  
2. **animals** – dogs and cats housed by shelters  
3. **employees** – staff members assigned to shelters  
4. **vaccines** – catalog of vaccines and stock levels  
5. **vaccination_record** – tracks vaccinations by employee and animal  

This design supports reporting, inventory management, multi‑shelter operations, and automation.

## SQL Scripts Included
All SQL files are located in `/sql` and include:

- **Schema & Table Creation** – tables, constraints, keys, ENUM validation, indexes  
- **Data Population** – insert statements with AUTO_INCREMENT IDs  
- **Advanced Queries** – shelter ranking, vaccination calendar, overdue reports, aggregations, joins, subqueries  
- **Views & Triggers** – `vw_animal_vaccinations`, `trg_decrement_vaccine_stock`  

All scripts were executed and verified using **MySQL Workbench**.

## Application Architecture

### Data Layer
The MySQL database contains the authoritative version of all shelter data.

### Application Layer
Streamlit loads static CSV exports from MySQL:

- `data/animals.csv`  
- `data/shelters.csv`  
- `data/employees.csv`  
- `data/vaccines.csv`  
- `data/vaccination_record.csv`  
- `data/images/.`  

This enables the hosted application to run without requiring a live database connection.

### UI Structure
The UI provides three tabs:
- **Guest – Browse Animals**: filters (species, status, shelter), animal cards with photos  
- **Staff – Animals Overview**: total animals, grouped by shelter, full table snapshot  
- **Staff – Vaccinations & Stock**: vaccine stock table, overdue vaccination report, totals by species  

## Deployment
- Deployed on **Streamlit Cloud**  
- Dependencies listed in `requirements.txt.`  
- Static data (CSV + images) versioned in the repository  

## Testing & Security
- SQL scripts tested in **MySQL Workbench**  
- Streamlit app tested **locally and in cloud** deployments  
- Basic role separation (guest vs staff) implemented in UI layout  
- Authentication simplified for demonstration purposes  
- ⚠️ Production version would require secure credential storage and role‑based access control  

## Future Improvements
- Full CRUD operations connected to live MySQL  
- Staff authentication and permissions  
- Real‑time database syncing  
- Upload feature for animal images  
- Automated notifications for overdue vaccinations  
- Cloud‑based image storage (e.g., S3)  

## Author
Maria Savostianova  
University of Central Missouri  
Database Theory and Applications – Final Project


