ct Banner](https://github.com/prinsterlizzy-jpg/Fullstack/blob/main/Images/IMG_5654.jpeg?raw=true)

---

## 🔰 Badges

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-07405E?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![UI/UX](https://img.shields.io/badge/Design-Figma-orange?logo=figma)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Overview

This is a **Computer-Based Test (CBT)** system built using **Python (Flask)** for the backend and **HTML/CSS** for the frontend.  
The dashboard UI is inspired by a clean Figma design with focus on simplicity, structure, and easy navigation.

This project includes authentication (login/signup), a functional dashboard, and placeholder pages for exams and results.

### 📸 Dashboard Screenshot  
![CBT Dashboard Screenshot](https://github.com/prinsterlizzy-jpg/Fullstack/blob/main/CBT%20dashboard%20project/F4AA42AB-BEEE-4C6B-BCFB-9AB9FD4B06A0.png?raw=true)

---

## ✅ Features

- 🔐 User Signup & Login (Authentication)
- 🖥️ Responsive Dashboard UI
- 🧭 Navigation Cards:
  - Take Exam
  - Exams
  - Results
  - Logout
- 🗄️ SQLite database support
- 🔗 Page-to-page routing
- 🎨 Clean UI/UX design structure
- 🧱 Easy to extend (exam logic, admin panel, score calculation)

---

## 📂 Project Structure

- User signup and login (authentication)  
- Dashboard UI with navigation cards (Take Exam, Exams, Results, Logout)  
- Page routing: login → dashboard → take exam / exams / results → logout  
- Simple SQLite database for storing user accounts  
- Clean and responsive UI layout (sidebar, header, cards)  
- Easy to extend: exam logic, result tracking, admin panel, etc.

---

## 📂 Project Structure
cbt_system/
│
├── app.py                # Flask backend application
├── database.db           # SQLite database file
├── templates/            # HTML templates
│     ├── login.html
│     ├── signup.html
│     ├── dashboard.html
│     ├── exam.html
│     ├── results.html
│
└── static/
└── style.css       # CSS styling for the UI
---

## 🛠️ Setup & Installation

1. Clone this repository  
   ```bash
   git clone https://github.com/prinsterlizzy-jpg/Fullstack.git
   cd Fullstack/cbt_system
2.	Install dependencies
   pip install flask
3.	Run the application
     python app.py
4.	Open in your browse
     http://127.0.0.1:5000
5.	You can now signup, login, and navigate the dashboard.

🔄 How it Works

✔ Frontend

Built using HTML + CSS to match Figma’s layout.
Includes:
	•	header
	•	sidebar
	•	cards
	•	login/signup forms

✔ Backend

Powered by Flask:
	•	route handling
	•	login/session management
	•	database operations

✔ Database

Uses SQLite with automatic table creation:
	•	users
(will add more tables later)

✔ UX Flow

Signup → Login → Dashboard → (Take Exam / Exams / Results) → Logout

  🚀 Future Improvements (Roadmap)
	•	⏳ Add exam questions & choices
	•	⏳ Add timer-based exam system
	•	⏳ Auto-score calculation
	•	⏳ Store student results
	•	⏳ Results history page
	•	⏳ Admin panel to upload questions
	•	⏳ Email notifications
	•	⏳ Better UI animation and transitions

👤 Author
Prinsterlizzy — Fullstack Developer & UI/UX Enthusiast

👍 License & Contribution

Feel free to fork and extend the project.
Please give credit if you reuse the code or UI.
Pull requests and improvements are welcome!
