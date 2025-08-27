# CodeSphere – AI-Powered Online Code Execution Platform 🚀

CodeSphere is an *AI-powered online code execution and review platform* that allows users to write, execute, and validate code securely within isolated Docker containers.  
It is built with *Django* and integrates *Google Gemini AI* for intelligent, real-time code review and feedback.  

Live Website 🌍: [https://mysite.ojhub.online](https://mysite.ojhub.online)  

---

## 🚀 Features

- *Code Execution in Docker*  
  - Each user’s code is executed inside an isolated Docker container.  
  - Input and output are handled via mounted volumes for secure interaction.  
  - Supports multiple programming languages (Python, C++, etc.).  

- *AI-Powered Code Review* (via *Google Gemini*)  
  - After execution, Gemini analyzes the user’s code.  
  - Provides constructive feedback, optimizations, and error explanations.  
  - Helps users understand and improve their code quality.  

- *Django Backend*  
  - Problem management, code submission, and results tracking.  
  - API endpoints for compiler integration.  

- *Nginx with SSL*  
  - Hosted on *AWS EC2*.  
  - SSL termination with Nginx for secure HTTPS access.  

---

## 🛠 Tech Stack

- *Backend*: Django (Python)  
- *Code Execution*: Docker (containers for compiler app)  
- *AI Review*: Google Gemini API  
- *Deployment*: AWS EC2 with Nginx (SSL)  
- *Database*: SQLite/PostgreSQL (depending on environment)  

---

## ⚙ System Architecture

1. User writes and submits code.  
2. Django saves the submission and forwards it to the *compiler app*.  
3. The compiler app runs the submitted code inside a *Docker container* with mounted input/output volumes.  
4. Execution results are returned to Django.  
5. If execution is complete, Gemini is triggered to provide *AI feedback* on the code.  
6. Results and feedback are displayed to the user.  

---

## 📦 Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/yourusername/codesphere.git
cd codesphere
```



### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a .env file in the root directory:
```
DEBUG=True
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
```

Gemini API Key
```
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run Database Migrations
```
python manage.py migrate
```

### 5. Run the Django Development Server
```
python manage.py runserver 0.0.0.0:8000
```
---

## 🐳 Code Execution with Docker

The compiler app runs user code inside Docker:
```
docker run --rm
-v /path/to/code:/app/codes
-v /path/to/input:/app/inputs
-v /path/to/output:/app/outputs
code-runner bash -c "python3 /app/codes/main.py < /app/inputs/input.txt > /app/outputs/output.txt"
```

This ensures:  
- Isolation – No direct access to host machine.  
- Security – Prevents malicious code from escaping the container.  
- Reproducibility – Same environment for all executions.  

---

## 🤖 AI-Powered Code Review with Gemini

After successful execution:  
- The submitted code is passed to Google Gemini API.  
- Gemini analyzes the logic, detects inefficiencies, and suggests improvements.  
- Feedback is displayed alongside the execution results.  

Example feedback Gemini can provide:  
- Explaining runtime errors in simple terms.  
- Suggesting more efficient algorithms.  
- Warning about potential security issues.  

---

## 🌍 Deployment on AWS EC2

The project is deployed on AWS EC2.  
Nginx is used as a reverse proxy and for SSL termination.  
Project files are directly cloned and run inside the EC2 instance.  

Deployment Steps:
Clone project inside EC2
```
git clone https://github.com/yourusername/codesphere.git
cd codesphere
```

Install dependencies
```
pip install -r requirements.txt
```

Collect static files
```
python manage.py collectstatic
```

Setup Nginx for reverse proxy + SSL
```
sudo nano /etc/nginx/sites-available/codesphere
```

---

## 🔒 Security Considerations

- Code execution happens in isolated Docker containers.  
- No sensitive data is exposed to user code.  
- SSL ensures secure communication over HTTPS.  

CodeSphere – AI-Powered Online Code Execution Platform 🚀
CodeSphere is an AI-powered online code execution and review platform that allows users to write, execute, and validate code securely within isolated Docker containers.
It is built with Django and integrates Google Gemini AI for intelligent, real-time code review and feedback.

Live Website 🌍: https://your-domain.com
