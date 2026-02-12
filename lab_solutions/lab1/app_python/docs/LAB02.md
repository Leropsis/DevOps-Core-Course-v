# LAB02 - Docker Containerization

## Docker Best Practices Applied

### 1. Non-Root User
**Implementation:**
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

**Non-Root User motivation:** Running containers as root is a security risk. If an attacker compromises the application, they gain root privileges inside the container, which can be escalated to host-level access in some scenarios. Non-root users limit the damage potential.

### 2. Specific Base Image Version
**Implementation:**
```dockerfile
FROM python:3.13-slim
```

**Why it matters:** Using a specific version (not `latest`) ensures reproducible builds. The `slim` variant reduces image size by excluding unnecessary packages, reducing attack surface and download time.

### 3. Layer Caching Optimization
**Implementation:**
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
```

**Why it matters:** Docker caches layers. By copying `requirements.txt` before application code, dependency installation is only re-run when dependencies change. Since code changes more often than dependencies, this speeds up rebuilds significantly.

### 4. .dockerignore File
**Implementation:** Excluded unnecessary files like `venv/`, `__pycache__/`, `.git/`, `docs/`, `tests/`

**Why it matters:** Reduces build context size sent to Docker daemon, speeding up builds. Also prevents accidentally copying sensitive files or development artifacts into the image.

### 5. Minimal File Copying
**Implementation:** Only copied essential files (`requirements.txt` and `app.py`)

**Why it matters:** Smaller images mean faster deployments, less storage, and reduced attack surface. Each file copied is a potential security or bloat issue.

### 6. No Cache for pip
**Implementation:**
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

**Why it matters:** pip cache is useless in a container (build-time only) and wastes space in the final image.

---

## Image Information & Decisions

### Base Image: `python:3.13-slim`
**Justification:** 
- **Slim variant:** Balances size and functionality - includes what Python apps need, excludes build tools and docs
- **Version 3.13:** Latest stable Python, matches development environment
- **Alternative considered:** `alpine` is smaller but uses `musl` instead of `glibc`, causing compatibility issues with some Python packages

### Final Image Size
164MB

### Layer Structure
1. Base image (`python:3.13-slim`)
2. User creation
3. Working directory setup
4. Dependency installation (cached layer)
5. Application code (changes frequently)
6. Permission changes
7. User switch

### Optimization Choices
- Separated dependency installation from code copy for caching
- Used `--no-cache-dir` to avoid storing pip cache
- Created non-root user before copying files to ensure proper ownership

---

## Build & Run Process

### Build Output
```bash
# Build command
docker build -t chupapupa/devops-info-service:latest .

```

### Run Output
```bash
# Run command
docker run -p 5000:5000 chupapupa/devops-info-service:latest

```

### Testing Endpoints
```bash

curl http://localhost:5000/


curl http://localhost:5000/health
```

### Docker Hub Repository
URL: `https://hub.docker.com/r/chupapupa/devops-info-service`

---

## Technical Analysis

### Why Does This Dockerfile Work?

1. **Layer Order:** Dependencies are installed before code is copied, leveraging Docker's layer caching. If only `app.py` changes, Docker reuses the cached dependency layer.

2. **User Permissions:** Files are copied as root, then ownership is changed to `appuser`. This ensures the non-root user can read application files while maintaining security.

3. **Working Directory:** `WORKDIR /app` creates the directory if it doesn't exist and sets it as the context for subsequent commands.

### What Would Happen If Layer Order Changed?

If we copied `app.py` before `requirements.txt`:
- Every code change would invalidate the dependency installation layer
- Builds would take much longer (re-installing packages every time)
- No functional difference, just slower workflow

### Security Considerations

1. **Non-root user:** Limits privilege escalation potential
2. **Slim base image:** Reduces attack surface (fewer packages = fewer vulnerabilities)
3. **Specific versions:** Prevents supply chain attacks via `latest` tag changes
4. **Minimal file copying:** Reduces risk of exposing sensitive files

### .dockerignore Benefits

1. **Build Speed:** Smaller build context = faster uploads to Docker daemon
2. **Security:** Prevents accidentally copying `.git`, `.env`, or credentials
3. **Image Size:** Excludes unnecessary files like `venv/` or `__pycache__/`

---

## Challenges & Solutions

### Challenge 1: Permission Denied When Running as Non-Root
**Problem:** Initially tried switching to non-root user before copying files, which caused permission errors.

**Solution:** Copy files as root first, then use `chown` to change ownership, then switch user. Order matters!

### Challenge 2: Understanding Layer Caching
**Problem:** Initial builds took a long time even with minor code changes.

**Solution:** Researched Docker layer caching and restructured Dockerfile to copy dependencies before code. Dramatically improved rebuild times.

---

## What I Learned

1. **Security by default:** Non-root users should be standard, not optional
2. **Layer order impacts build speed:** Docker's caching can save significant time
3. **Base image choice matters:** Balance between size, compatibility, and security
4. **Documentation is understanding:** Writing this doc helped solidify my Docker knowledge
