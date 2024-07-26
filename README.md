# Software-Engineering-Project

In this project we aim to integrate an LLM into a learning platform to enhance the learning experience of students.
This project is part of the Software Engineering course of BS in Data Science at Indian Institute of Technology, Madras.

## Team Members

1. [Shivang Kumar](www.github.com/kumar-shivang)
2. [Durgesh Puri Goswami](www.github.com/Durgesh-prog)

## Technologies Used

1. Flask - Backend
2. React - Frontend
3. Huggingface - LLM
4. Docker - Containerization


## Installation Steps

Run Simulatenously
sh start.sh


Run Separately

Terminal 1 (For Backend)
python3 -m venv venv   
source venv/bin/activate 
pip install Flask       
pip install flask_sqlalchemy
cd backend/
python app.py

Terminal 2 (For Frontend)
cd frontend/
yarn (For installing dependencies once)
yarn start