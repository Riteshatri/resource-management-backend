# 🔧 Environment Configuration Guide

## 📌 Dual Support - Choose Your Method

This backend supports **TWO flexible ways** to configure environment variables:

---

## 🎯 Method 1: `.env` File (Recommended for VM Deployment)

Perfect for **Azure VM** or any **traditional server deployment**.

### Steps:

1. **Copy the example file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env` with your actual values:**
   ```bash
   nano .env
   ```

3. **Update these critical values:**
   ```bash
   # Azure SQL Database
   AZURE_SQL_SERVER=your-server.database.windows.net
   AZURE_SQL_DATABASE=your-database-name
   AZURE_SQL_USERNAME=your-username
   AZURE_SQL_PASSWORD=your-password
   
   # Security
   SECRET_KEY=generate-random-32-chars-minimum
   
   # CORS (Frontend URL)
   CORS_ALLOW_ORIGINS=http://your-frontend-ip:5000
   ```

4. **Run the backend:**
   ```bash
   python run.py
   ```

✅ **The app will automatically load from `.env` file**

---

## 🎯 Method 2: Environment Variables (Secrets)

Perfect for  **Docker**, or **cloud platforms**.

### Steps:

1. **No `.env` file needed** - Delete it if exists:
   ```bash
   rm backend/.env  # Optional
   ```

2. **Set environment variables** in your platform:



   **Terminal/Shell:**
   ```bash
   export AZURE_SQL_SERVER=your-server.database.windows.net
   export AZURE_SQL_DATABASE=your-database-name
   export AZURE_SQL_USERNAME=your-username
   export AZURE_SQL_PASSWORD=your-password
   export SECRET_KEY=your-secret-key
   export CORS_ALLOW_ORIGINS=http://frontend:5000
   export APP_ENV=production
   ```

   **Docker/Systemd:**
   ```bash
   # In systemd service file
   Environment="AZURE_SQL_SERVER=your-server.database.windows.net"
   Environment="SECRET_KEY=your-secret-key"
   ```

3. **Run the backend:**
   ```bash
   python run.py
   ```

✅ **The app will automatically use environment variables**

---

## 🔄 Priority Order

The application loads configuration in this priority:

```
1. .env file (if exists)
   ↓ (if not found)
2. Environment Variables
   ↓ (if not set)
3. Default Values (from code)
```

### Example:

```bash
# If you have BOTH:
.env file has: AZURE_SQL_SERVER=vm-server.database.windows.net
Environment var: AZURE_SQL_SERVER=ritesh-server.database.windows.net

# Result: Uses .env file value (vm-server.database.windows.net)
```

**Note:** The code uses `override=True` in `load_dotenv()`, which means `.env` file values will **override** environment variables. This ensures your VM-specific configuration takes precedence.

---

## 🧪 Test Your Configuration

### Check if .env is loaded:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ .env loaded' if os.path.exists('.env') else '⚠️ Using env vars')"
```

### Verify database connection:

```bash
cd backend
python -c "from app.core.config import settings; print(f'Server: {settings.AZURE_SQL_SERVER}')"
```

Expected output:
```
✅ Server configured for: your-server.database.windows.net
Server: your-server.database.windows.net
```

### Test backend startup:

```bash
python run.py
```

Look for:
```
✅ Server configured for: your-server.database.windows.net
🔗 Connecting to: your-server.database.windows.net
📊 Database: your-database-name
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 📝 Required Variables

### Minimum for Development (SQLite):
```bash
APP_ENV=development
SECRET_KEY=your-secret-key
CORS_ALLOW_ORIGINS=*
```

### Required for Production (Azure SQL):
```bash
APP_ENV=production
PORT=8000
UVICORN_WORKERS=4
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=your-database-name
AZURE_SQL_USERNAME=your-username
AZURE_SQL_PASSWORD=your-password
SECRET_KEY=your-secret-key-minimum-32-chars
CORS_ALLOW_ORIGINS=http://frontend-ip:5000
FRONTEND_URL=http://frontend-ip:5000
```

---

## 🚨 Troubleshooting

### Problem: "Database credentials not configured"

**Solution:** Check if variables are loaded:
```bash
# If using .env:
cat backend/.env | grep AZURE_SQL_SERVER

# If using env vars:
echo $AZURE_SQL_SERVER
```

### Problem: "Connection refused" from frontend

**Solution:** Update CORS:
```bash
# In .env or environment variable:
CORS_ALLOW_ORIGINS=http://actual-frontend-ip:5000,https://yourdomain.com
```

### Problem: .env file not loading

**Solution:** Verify file location:
```bash
# Should be in backend/ folder:
ls -la backend/.env

# Check if python-dotenv is installed:
pip list | grep dotenv
```

---

## 🎯 Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use strong SECRET_KEY** - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
3. **Production CORS** - Never use `*` in production, use specific domains
4. **Azure SQL Password** - Use complex passwords with special characters
5. **Backup `.env`** - Keep a secure backup of your production `.env` file

---

## 📦 Quick Start Commands

### For VM Deployment:
```bash
# 1. Copy example
cp .env.example .env

# 2. Edit values
nano .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python run.py
```

---

**You're all set! 🚀** Choose the method that works best for your deployment environment.
