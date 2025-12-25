# 🚀 Docker Images Push Guide (GHCR + Docker Hub)

> **Author:** Ritesh Sharma  
> **Level:** Beginner → Advanced (DevOps Ready)  
> **Goal:** Docker images ko **GitHub Container Registry (GHCR)** aur **Docker Hub** dono me **A to Z** push karna – bilkul *tod‑tod kar, khol‑khol kar* 😄

---

## 📌 Table of Contents
1. Docker Registry kya hota hai?
2. Dockerfile ka role (important concept)
3. GitHub Container Registry (GHCR) – Deep Dive
4. GHCR me Docker image push (A to Z)
5. Access, Roles & Security samjho
6. Docker Hub – Deep Dive
7. Docker Hub me Docker image push (A to Z)
8. Versioning & Best Practices
9. Common Errors & Fixes
10. Final DevOps Architecture

---

# 🧠 1. Docker Registry kya hota hai?

Docker Registry ek **central store** hota hai jahan hum:
- Docker images **upload (push)** karte hain
- Docker images **download (pull)** karte hain

### Popular Registries:
- 🟢 Docker Hub (default & public)
- 🟣 GitHub Container Registry (GHCR)
- 🔵 Azure Container Registry (ACR)

---

# 🍳 2. Dockerfile ka role (MOST IMPORTANT)

👉 **Dockerfile = Recipe**  
👉 **Docker Image = Cooked Food**  
👉 **Registry = Fridge**

📌 **Registry change karne se Dockerfile kabhi change nahi hoti**

```text
Dockerfile → docker build → Image → docker tag → docker push
```

---

# 🟣 3. GitHub Container Registry (GHCR) – Deep Dive

### GHCR kya hai?
- GitHub ka **official container registry**
- URL format:

```text
ghcr.io/<github-username>/<image-name>:<tag>
```

### Important baat:
- Images **repo ke andar save nahi hoti**
- Images **GitHub account level → Packages** me hoti hain
- Repo se **link** ki ja sakti hain (best practice)

---

# 🚀 4. GHCR me Docker Image Push – A to Z

## ✅ Step 1: GitHub Personal Access Token (PAT)

GitHub → Settings → Developer Settings → Personal Access Tokens (Classic)

### Required Scopes:
- ✅ `write:packages`
- ✅ `read:packages`
- ✅ `repo`

> ⚠️ Token ko safe rakhna – ye password jaisa hota hai

---

## ✅ Step 2: GHCR Login

```bash
docker login ghcr.io
```

- **Username:** GitHub username
- **Password:** PAT

Expected Output:
```text
Login Succeeded
```

---

## ✅ Step 3: Docker Image Build

```bash
docker build -t resource-management-backend:v1 .
```

Check:
```bash
docker images
```

---

## ✅ Step 4: Image Tag (MOST IMPORTANT)

```bash
docker tag resource-management-backend:v1 \
  ghcr.io/<username>/resource-management-backend:v1
```

Example:
```bash
docker tag resource-management-backend:v1 \
  ghcr.io/riteshatri/resource-management-backend:v1
```

---

## ✅ Step 5: Push to GHCR

```bash
docker push ghcr.io/riteshatri/resource-management-backend:v1
```

🎉 Image GHCR me chali gayi

---

# 🔐 5. GHCR Access & Roles (Very Important)

### Actions Repository Access Roles:

| Role | Use Case |
|----|----|
| Read | Sirf pull |
| ✅ Write | CI/CD build + push |
| Admin | Delete / restore images |

👉 **Always use WRITE for CI/CD**

---

# 🟠 6. Docker Hub – Deep Dive

### Docker Hub kya hai?
- Default public registry
- URL format:

```text
docker.io/<dockerhub-username>/<image-name>:<tag>
```

---

# 🚀 7. Docker Hub me Image Push – A to Z

## ✅ Step 1: Docker Hub Account

- https://hub.docker.com
- Username & password create karo

---

## ✅ Step 2: Docker Hub Login

```bash
docker login
```

OR

```bash
docker login docker.io
```

---

## ✅ Step 3: Image Tag for Docker Hub

```bash
docker tag resource-management-backend:v1 \
  dockerhubusername/resource-management-backend:v1
```

Example:
```bash
docker tag resource-management-backend:v1 \
  Riteshatrikumar/resource-management-backend:v1
```

---

## ✅ Step 4: Push to Docker Hub

```bash
docker push Riteshatrikumar/resource-management-backend:v1
```

🎉 Image Docker Hub pe live

---

# 🧪 8. Versioning & Best Practices

### ❌ Galat
```text
latest
```

### ✅ Sahi
```text
v1.0.0
v1.0.1
build-101
```

---

# ❗ 9. Common Errors & Fixes

### ❌ permission denied
✔ Token scopes missing

### ❌ denied: write access
✔ GHCR package → Actions access = WRITE

### ❌ unauthorized
✔ docker login sahi se nahi hua

---

# 🏁 10. Final DevOps Architecture

```text
Developer
   ↓
Dockerfile
   ↓
docker build
   ↓
docker tag
   ↓
GHCR / Docker Hub
   ↓
VM / K8s / AKS
```

---

## 🎯 Final Verdict

✔ Dockerfile same rehti hai  
✔ Registry sirf storage hoti hai  
✔ GHCR & Docker Hub dono industry ready  
✔ WRITE access = must

---

🔥 **Next Level (Optional)**
- GitHub Actions CI/CD
- docker-compose with GHCR images
- Kubernetes deployment

> **Happy DevOps 🚀**

