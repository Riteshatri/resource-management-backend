# ===============================
# 1️⃣ BUILDER STAGE
# ===============================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Build dependencies (ONLY for building wheels)
RUN apt-get update && apt-get install -y \
    build-essential \
    unixodbc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements
COPY requirements.txt .

# Upgrade pip & build wheels
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ===============================
# 2️⃣ RUNTIME STAGE
# ===============================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Runtime-only dependencies (LIGHT)
RUN apt-get update && apt-get install -y \
    unixodbc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m backenduser

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache-dir /wheels/* \
    && pip install gunicorn \
    && rm -rf /wheels

# Copy application code
COPY . .

# Permissions
RUN chown -R backenduser:backenduser /app
USER backenduser

EXPOSE 8000

CMD ["gunicorn", "app.main:app", \
     "--workers", "3", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120"]


#  docker build -t resource-management-backend .
#  docker run -d --name resource-management-backend --env-file .env   -p 8000:8000 resource-management-backend