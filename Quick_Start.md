## 🚀 Backend Deployment on Ubuntu VM

### Step 1: Connect to Backend VM

```bash
# SSH into your Ubuntu VM
ssh user@your-backend-vm-ip

# Example:
# ssh ritesh@20.123.45.67
```

### Step 2: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y build-essential python3.12 python3.12-venv python3-pip unixodbc-dev git

# Verify Python version
python3.12 --version
# Should show: Python 3.12.x
```

### Step 3: Transfer Backend Code to VM

**Option A: Using SCP (from Windows PowerShell)**
```powershell
# From your Windows machine
scp -r "E:\path\to\backend" user@vm-ip:"~/"
```

**Option B: Using Git (on Ubuntu VM)**
```bash
# On Ubuntu VM
cd /home/user
git clone <your-repo-url>
cd your-repo/backend
```

### Step 4: Create Virtual Environment

```bash
# Navigate to backend folder
cd /home/user/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in prompt
```

### Step 5: Install Python Dependencies

```bash
# Make sure (venv) is active!
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed fastapi uvicorn sqlalchemy pymssql ...
```

### Step 6: Create Environment Configuration

```bash
# Create environment file
sudo nano .env
```

**Add this content:**
```env
AZURE_SQL_SERVER=ritserver.database.windows.net
AZURE_SQL_DATABASE=ritserver
AZURE_SQL_USERNAME=ritserver
AZURE_SQL_PASSWORD=Ritesh@12345
SECRET_KEY=1f7abb32c57632c35cbf57657f20ca104d88e18dd3cb17050649b10664cd743f
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["*"]
FRONTEND_URL=http://4.245.193.71:5000
```
 For example:-  
    SECRET_KEY=1f7abb32c57632c35cbf57657f20ca104d88e18dd3cb17050649b10664cd743f  
### Want to see full guide how to use Environment Variables -> Read Environment Configuration Guide.md  
### Step 7: Test Backend Manually First

```bash
# Make sure you're in backend folder with venv active
source venv/bin/activate
python run.py
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/home/ritesh']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [5630] using WatchFiles
✅ Server configured for: ritserver.database.windows.net
✅ Using Azure SQL: ritserver.database.windows.net
INFO:     Started server process [5632]
INFO:     Waiting for application startup.
✅ Protected admin user created: ritesh@apka.bhai
INFO:     Application startup complete.
```

**Test it:**
```bash
# In another backend vm's terminal
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

If working, press `Ctrl+C` to stop. Now create systemd service!

### Step 8: Create Systemd Service (Auto-start)

```bash
# Create service file
sudo nano /etc/systemd/system/resource-backend.service
```

**Add this content:**
```ini
[Unit]
Description=Resource Management Backend API
After=network.target

[Service]
Type=notify
User=ritesh
WorkingDirectory=/home/ritesh/            # path where your all backend code is
Environment="PATH=/home/ritesh/venv/bin"  # your virtual environment's bin folder path
EnvironmentFile=/home/rites/.env        # path where your environment(.env) file is.
ExecStart=/home/ritesh/venv/bin/gunicorn app.main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `ritesh` with your actual username!

**Save:** `Ctrl+S` and then `Ctrl+X`  

# Why we need this, Systemd Service ?
### 🔥 Systemd Service = Your backend app running permanently in the background
```bash
Just like Windows has “Services” (Service Manager → keeps apps running even when no user is logged in, restarts automatically, survives reboots)…
✅ Linux uses systemd services to do the same job.

❓💡 Why do you need a systemd service?

If you run your backend manually like this:
   👉 uvicorn app.main:app --host 0.0.0.0 --port 8000
        or like this 
   👉 python run.py


Then:
    Closing SSH → the app stops ❌
    Closing the terminal → the app stops ❌
    VM reboot → the app stops ❌
    App crashes → the app stops ❌

This is not acceptable in a production environment.

Your backend must always be running, even if you log out or the VM restarts.

✔ What systemd gives you ❓❓❓

A systemd service ensures:
    ✔ Your app runs in the background (daemon mode)
    ✔ App starts automatically at boot
    ✔ If the app crashes, systemd restarts it
    ✔ You get proper logs using journalctl
    ✔ You can start/stop/restart the app like any Linux service

It works exactly like Windows “Services”.

🧠 How a systemd service looks
To run your backend as a service, you create a file:
/etc/systemd/system/resource-backend.service    # Here we can use any service name..  

sudo systemctl start resource-backend
sudo systemctl stop resource-backend
sudo systemctl restart resource-backend
sudo systemctl status resource-backend

This is the Linux equivalent of Windows Services — simple and powerful.
``` 
### Step 9: Install Gunicorn

```bash
# Activate venv and install gunicorn
# source /home/ritesh/backend/venv/bin/activate
source venv/bin/activate
pip install gunicorn
```

### Step 10: Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable resource-backend

# Start service
sudo systemctl start resource-backend

# Check status
sudo systemctl status resource-backend

# Some extra usefull commands
        # sudo systemctl restart resource-backend.service

```

**Expected Output:**
```
● resource-backend.service - Resource Management Backend API
   Loaded: loaded (/etc/systemd/system/resource-backend.service; enabled)
   Active: active (running) since ...
```

### Step 11 (OPTIONAL) : Configure Firewall

```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Check firewall status
sudo ufw status
```

### Step 12: Test External Access

**From your Windows laptop:**
```powershell
# Test health endpoint
http://YOUR-BACKEND-VM-IP:8000/health

# Should return: {"status":"healthy"}
```

✅ **Backend Deployment Complete!**

---
