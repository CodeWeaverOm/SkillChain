🌐 SkillChain – Peer-to-Peer Skill Validation Platform

A community-driven platform for validating real-world skills through micro-projects, video proofs, and peer endorsements.

🧑‍💻 Team – PIBM CodeClan

Members:

Om Nimmalwar

Abdulhnan Shaikh

Devki Salvi

Sahil Sawant

College: Pratibha Institute of Business Management

Event: Scitech Innovation Hackathon 2025

📘 Project Overview

SkillChain introduces a peer-to-peer skill validation system that replaces traditional certifications with practical, performance-based proofs.
Users submit micro-projects, tasks, or video demonstrations, and peers validate them through endorsements.
Validated skills earn Digital Badges, stored in a secure Skill Bank, showcasing verified abilities to employers.

🎯 Objective

Build a transparent skill validation system.

Enable users to showcase authentic, verified skills.

Foster peer recognition, trust, and collaboration.

Improve employability with credible digital credentials.

🧩 Problem Statement

Traditional assessment systems prioritize theory over skills.
Millions of talented individuals—students, freelancers, and self-learners—struggle to prove their true abilities.

SkillChain bridges this gap using community verification instead of institutional certification.

💡 Key Features

👤 User Profiles – Skills, badges, portfolio

🎥 Skill Demonstration – Upload video proofs or micro-projects

🤝 Peer Validation – Community-driven endorsements

🏅 Digital Badges – Stored in a Skill Bank

🔐 Fraud Detection – Moderation to maintain fairness

🎮 Leaderboard – Gamified reward system

📊 Admin Panel – Review submissions, manage users

🚀 Proposed Solution

SkillChain provides a practical and inclusive method for validating capabilities.
Instead of exams, users demonstrate skills through real tasks, verified by real people.

👥 Target Users

Students & Graduates

Freelancers & Creatives

Job Seekers

Recruiters

Educational Institutions

🌍 Impact
🏛 Social

Brings recognition to hidden talents

Encourages collaborative learning

💻 Technical

Secure, scalable Django backend

Gamified, interactive platform

💼 Commercial

Helps job seekers stand out

Enables partnerships with colleges and companies

🛠 Technology Stack
Frontend:

HTML, CSS, JavaScript

(Optional) React.js

Backend:

Django / Django REST Framework

Node.js (Optional alternative)

Database:

MySQL / MongoDB / SQLite

Tools Used:

Figma / Canva

Git & GitHub

Python virtual environments

🧠 Innovation & Uniqueness

✔ Peer-to-peer validation instead of certificates
✔ Video/micro-project based skill demonstration
✔ Fraud prevention & moderation
✔ Gamified leaderboard & badges
✔ Digital Skill Bank for verified credentials

📊 Future Scope

LinkedIn & Job Portal Integration

Blockchain-based credential verification

AI-powered fraud detection

Mobile App (Android + iOS)

Auto-evaluation with AI analysis

📽️ Deliverables

Fully functional prototype

Demonstration video

Documentation & Report

Hackathon Presentation (PPT)

🛠️ Configuration & Installation Guide

Below are the steps to set up and run the SkillChain Django Project.

1️⃣ Install Python

Download the latest version:

🔗 https://www.python.org/downloads/

✔ Check “Add Python to PATH” during installation

2️⃣ Create Virtual Environment

Create venv:

python -m venv venv


Activate venv:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Install Dependencies
pip install django
pip install djangorestframework
pip install pillow
pip install python-dotenv
pip install mysqlclient     # for MySQL users


(Optional dependencies vary by project)

4️⃣ Database Setup
✔ Default SQLite

Works automatically. No config needed.

✔ MySQL Configuration

Update settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skillchain',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Admin User
python manage.py createsuperuser

7️⃣ Run the Development Server
python manage.py runserver


Open the app:
👉 http://127.0.0.1:8000/

📁 Recommended Project Structure
SkillChain/
│
├── skillchain/           # Main project settings
├── accounts/             # User & authentication
├── skills/               # Skill verification system
├── static/               # CSS, JS, Images
├── templates/            # HTML templates
├── media/                # Uploaded videos/files
├── venv/                 # Virtual environment
└── manage.py

🏁 Conclusion

SkillChain provides a modern, inclusive, and practical approach to validating real abilities.
By empowering users to demonstrate and verify skills directly, we build a more transparent and trustworthy talent ecosystem.

📚 License

This project is developed for SciTech Innovation Hackathon 2025 by PIBM CodeClan.
All rights reserved for academic purposes.

⭐ “Validate Skills, Empower Talent.”