# Health and Fitness Club Management System

## COMP 3005 - Winter 2024 Project
Instructors: Ahmed El-Roby and Abdelghny Orogat  
Due: April 13, 2024 (11:59 PM)
By: Abdullah Soboh (101220742)
    Imann Brar (101225891)


### Overview
This project implements a comprehensive Health and Fitness Club Management System designed to cater to the needs of club members, trainers, and administrative staff. The system allows members to manage their profiles, set fitness goals, track their health statistics, and schedule training sessions. Trainers can manage their schedules and view member profiles, while administrative staff can handle room bookings, equipment maintenance, class schedules, and process billing.

### Features
- **Member Functions:**
  - Register Member
  - View Member Dashboard
  - Book Training
  - Register for class
  - Update Profile
  
- **Trainer Functions:**
  - Schedule Management
  - Member Profile Viewing
  
- **Administrative Staff Functions:**
  - Room Booking Management
  - Equipment Maintenance Monitoring
  - Class Schedule Updating
  - Billing and Payment Processing

### Technical Implementation
- **Database**: PostgreSQL
- **Backend**: Python with `psycopg2`
- **Frontend**: React, implemented with Axios for API calls and React Router for navigation.

### Repository Structure
- `/SQL`: Contains DDL and DML SQL files for database setup and sample data insertion.
- `Backend_Functions.py`: The main application script for the command-line interface.

### Usage
1. **Database Setup**: Execute the DDL script (`/SQL/ddl.sql`) in PostgreSQL to set up the database schema.
2. **Insert Sample Data**: Run the DML script (`/SQL/dml.sql`) to populate the database with sample data.
3. **Run Application**: Start the backend server using python app.py in the backend directory.
   Then, in the frontend directory, run npm start to launch the React application.

### Bonus Features Added
- Complete frontend added using React, styled with Bootstrap for a responsive design and better user experience.
- Extensive Member Achievments, and Health Stats added

### Video Demonstration
- The video demonstrates each functionality and the code structure. Find the video at [[YouTube link](https://youtu.be/y7CT8O9qvMs)].


### Contributions
- Abdullah: Backend
- Member 2: Frontend
- Remainder of work was shared.

### Contact
- Abdullah Soboh - abdullahsoboh@cmail.carleton.ca
- Imann Brar - Imannbrar@cmail.carleton.ca

