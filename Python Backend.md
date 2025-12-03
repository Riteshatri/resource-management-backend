# Python Backend - Resource Management System

## Tech Stack
- **Framework**: FastAPI
- **Database**: Azure SQL Database
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: passlib with bcrypt

## Project Structure
```
backend/
├── app/
│   ├── api/           # API endpoints
│   │   ├── auth.py    # Authentication routes
│   │   ├── users.py   # User management routes
│   │   ├── theme.py   # Theme configuration routes
│   │   └── deps.py    # Dependencies (auth middleware)
│   ├── core/          # Core functionality
│   │   ├── config.py  # Settings and configuration
│   │   └── security.py # Security utilities (JWT, password hashing)
│   ├── db/            # Database configuration
│   │   └── database.py # SQLAlchemy setup
│   ├── models/        # SQLAlchemy models
│   │   └── user.py    # User and ThemeConfig models
│   ├── schemas/       # Pydantic schemas
│   │   └── user.py    # Request/Response models
│   └── main.py        # FastAPI application
├── requirements.txt   # Python dependencies
├── run.py            # Development server runner
├── azure_sql_schema.sql # Database schema
└── .env.example      # Environment variables template
```

## Setup Instructions

### 1. Install Python Dependencies
```bash
cd backend

sudo apt install python3-pip -y


pip install -r requirements.txt
```

### 2. Configure Azure SQL Database
1. Create an Azure SQL Database in Azure Portal
2. Get connection details (server, database name, username, password)
3. Run `azure_sql_schema.sql` on your Azure SQL Database

### 3. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your Azure SQL credentials
```

Required environment variables:
```
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=your-database-name
AZURE_SQL_USERNAME=your-username
AZURE_SQL_PASSWORD=your-password
SECRET_KEY=generate-a-secure-random-key
FRONTEND_URL=http://your-frontend-url
```

### 4. Run the Application

#### Development Mode
```bash
python run.py
```

#### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/me` - Get current user profile
- `PATCH /api/users/me` - Update current user profile
- `GET /api/users/` - Get all users (Admin only)
- `GET /api/users/{user_id}` - Get user by ID (Admin only)

### Theme Configuration
- `GET /api/theme/` - Get all theme configurations
- `PATCH /api/theme/{config_key}` - Update theme config (Admin only)

## Deployment on Azure VM

### Prerequisites
- Ubuntu/Debian VM on Azure
- Python 3.9+ installed
- Azure SQL Database configured
- Allow 8000 inbound port in Backend VM, if necessary

### Steps
1. SSH into your Azure VM
2. Clone your repository
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables in `.env`
5. Install and configure systemd service:

```bash
sudo nano /etc/systemd/system/resource-api.service
```

```ini
[Unit]
Description=Resource Management API
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/backend
Environment="PATH=/home/azureuser/.local/bin"
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

6. Enable and start the service:
```bash
sudo systemctl enable resource-api
sudo systemctl start resource-api
sudo systemctl status resource-api
```

7. Configure nginx as reverse proxy (optional but recommended)

## Security Notes
- Always use HTTPS in production
- Keep SECRET_KEY secure and random
- Use environment variables for sensitive data
- Enable Azure SQL firewall rules for your VM's IP
- Consider using Azure Key Vault for secrets in production

```
1. Backend folder me jao
cd /home/ritesh/backend

sudo apt install python3-pip -y

sudo apt install python3.12-venv -y

2. Virtual environment banao
python3 -m venv venv

3. Activate karo (prompt change hoga - (venv) dikhaiga)
source venv/bin/activate

4. Pip upgrade karo
pip install --upgrade pip

5. Requirements install karo
pip install -r requirements.txt

6. Backend run karo
python run.py
```
  
  
  
  

# 🚀 Python Virtual Environment Setup (with Full Explanation)

This document explains **every command**, why we run it, and what effect it has.  
Perfect for beginners and for troubleshooting issues like the *externally-managed-environment* error.

---

## ✅ 1. Install Required Python Tools

### Command:
```bash
apt update
```
**Explanation:**  
Refreshes Ubuntu’s package list so the system knows the latest available software versions.

---

### Command:
```bash
sudo apt install -y python3-venv python3-pip python3-full
```
**Explanation:**  
Installs everything needed to manage Python projects:
- `python3-venv` → creates virtual environments  
- `python3-pip` → installs Python packages  
- `python3-full` → ensures standard libraries are present  
- `-y` → auto‑approves installation  

---

## 📁 2. Go to Your Project Directory

### Command:
```bash
cd /home/ritesh/backend
```
**Explanation:**  
Moves you into the folder containing project files and `requirements.txt`.

---

## 🧪 3. Create a Virtual Environment

### Command:
```bash
sudo python3 -m venv .venv
```
**Explanation:**  
Creates an isolated Python environment inside `.venv/`.  
This prevents conflicts with system-installed packages.

---

## 🔥 4. Activate the Virtual Environment

### Command:
```bash
source .venv/bin/activate
```
**Explanation:**  
Switches your terminal to use the virtual environment’s Python.  
After activation, installed packages affect only this project.

---

## 📦 5. Upgrade pip (Recommended)

### Command:
```bash
pip install --upgrade pip
```
**Explanation:**  
Updates pip to the latest version to avoid dependency installation issues.

---

## 📥 6. Install Project Dependencies

### Command:
```bash
pip install -r requirements.txt
```
**Explanation:**  
Reads `requirements.txt` and installs all required Python packages inside the venv.

---

## ▶️ 7. Run Your Application

### Commands:

#### 1. Development Mode
```bash
python app.py
```
**Explanation:**  
Starts the backend using the virtual environment’s Python.

#### 2. Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```


### You can also run with full path:
```bash
./.venv/bin/python app.py
```

---

## ❎ 8. Deactivate the Virtual Environment

### Command:
```bash
deactivate
```
**Explanation:**  
Returns your terminal back to system Python.

---

## 📝 9. Add .venv to .gitignore

```
.venv/
```

**Explanation:**  
Virtual environments are large and machine‑specific.  
Never commit them to Git.

---


## 🎯 Summary

You now have a clean and isolated Python setup that avoids Ubuntu’s *externally-managed-environment* issues and keeps your backend stable.



