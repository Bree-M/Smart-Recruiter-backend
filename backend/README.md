# Smart-Recruiter

***Smart Recruiter*** is a full-stack platform designed to streamline technical interviews for software developers. Inspired by tools like Coderbyte, it empowers recruiters to create tailored assessments, invite candidates, provide feedback, and analyze performance with detailed insights. Interviewees can practice, complete tests, and receive feedback in a seamless environment.



## Tech Stack
**Backend:** Python Flask
**Frontend:** ReactJs & Redux Toolkit(state management)
**Testing framework:** Jest & Minitests
**Database:** PostgreSQL

## Problem Statement
This is a software platform much like coderbyte, which could be used to assess the technical skills of software development interviewees. Basically, it automates the in-person technical interview.

## Features
### Recruiter capabilities 
-  Create & customize assessments (MCQs, text, coding)
- Send invites to candidates (single or bulk)
- Set a test deadline and time limit
- Review candidate answers with inline feedback
- View rankings, scores & analytics
- Publish and release grades

### Interviewer capabilites
- Accept assessment invitations
- View time & date of upcoming tests
- Practice with sample assessments
- Complete full whiteboard questions (BDD, pseudocode, code)
- See test feedback after submission

## Getting started 

***clone the repo***
https://github.com/Bree-M/Smart-Recruiter.git
cd Smart-Recruiter

###  Installation
**Backend-setup**
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**Creating an .env file**
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/smart_recruiter
JWT_SECRET_KEY=your-secure-jwt-secret-key
CODEWARS_API_KEY=your-codewars-api-key

**Initialize and migrate the database**
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/smart_recruiter
JWT_SECRET_KEY=your-secure-jwt-secret-key
CODEWARS_API_KEY=your-codewars-api-key


**Running the database migrations**
flask db init
flask db migrate
flask db upgrade


#### Frontend set-up(React)
cd frontend
npm install

 **Creating an .env file**
 REACT_APP_API_URL=http://localhost:5000

 #### Running the application
 **Start the server**
 psql -U username -d smart_recruiter -c "\l"

 **Running backend**
 cd backend
 source venv/bin/activate
 flask run

 **Running frontend**
 cd frontend
 npm start
 
 #### Testing Framework
 Jest & Minitest

 ### API Overview

 ### Contributing
 - Fork the repo
 - Create your feature branch
 - Commit your changes in your branch
 - Push the changes

### LICENSE 
MIT



