# 🐳 LegalEdge AI - Docker Setup Guide

## Quick Fix for PostgreSQL Error

If you're seeing the error:
```
Database is uninitialized and superuser password is not specified.
```

Follow these steps:

---

## ✅ Solution 1: Use the Docker Start Script (Easiest)

### Step 1: Create .env.docker file
```bash
cd "/Users/arsalanahmadkhan/Documents/Legal Chatbot"

# Copy your API key
cp .env.docker .env.docker.backup 2>/dev/null || true
```

The `.env.docker` file already has your OpenAI API key!

### Step 2: Clean up old containers
```bash
# Stop and remove any existing containers
docker-compose down -v

# This removes old volumes that might be causing issues
```

### Step 3: Start with the script
```bash
./docker-start.sh
```

This script will:
- Check Docker is running
- Stop old containers
- Build fresh images
- Start all services
- Initialize the database

---

## ✅ Solution 2: Manual Docker Compose

### Step 1: Stop old containers
```bash
cd "/Users/arsalanahmadkhan/Documents/Legal Chatbot"
docker-compose down -v
```

### Step 2: Load environment variables
```bash
export $(cat .env.docker | grep -v '^#' | xargs)
```

### Step 3: Start services
```bash
docker-compose up -d --build
```

### Step 4: Check logs
```bash
docker-compose logs -f postgres
```

You should see:
```
PostgreSQL init process complete; ready for start up.
```

---

## ✅ Solution 3: Run PostgreSQL Only (Recommended for Development)

Instead of running everything in Docker, you can run PostgreSQL in Docker and the backend/frontend locally:

### Step 1: Start only PostgreSQL
```bash
docker-compose up -d postgres
```

### Step 2: Wait for it to be ready
```bash
docker-compose logs -f postgres
# Wait until you see "database system is ready to accept connections"
# Press Ctrl+C
```

### Step 3: Initialize database
```bash
# Connect and create extension
docker-compose exec postgres psql -U postgres -d legaledge -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Step 4: Run backend locally
```bash
cd backend
source venv/bin/activate
python -c "from database import init_db; init_db()"
uvicorn main:app --reload
```

### Step 5: Run frontend locally
```bash
# In another terminal
cd frontend
npm run dev
```

This hybrid approach is often easier for development!

---

## 🔍 Troubleshooting

### Check if Docker is running
```bash
docker info
```

If you see an error, start Docker Desktop.

### Check if containers are running
```bash
docker-compose ps
```

### View all logs
```bash
docker-compose logs -f
```

### View specific service logs
```bash
# PostgreSQL
docker-compose logs -f postgres

# Backend
docker-compose logs -f backend

# Frontend
docker-compose logs -f frontend
```

### Restart a specific service
```bash
docker-compose restart postgres
docker-compose restart backend
docker-compose restart frontend
```

### Complete reset (removes all data!)
```bash
# Stop everything
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Start fresh
docker-compose up -d --build
```

---

## 🗄️ Database Commands

### Connect to PostgreSQL
```bash
docker-compose exec postgres psql -U postgres -d legaledge
```

### Run SQL commands
```bash
# Check tables
docker-compose exec postgres psql -U postgres -d legaledge -c "\dt"

# Count documents
docker-compose exec postgres psql -U postgres -d legaledge -c "SELECT COUNT(*) FROM documents;"

# Check vector extension
docker-compose exec postgres psql -U postgres -d legaledge -c "SELECT * FROM pg_extension WHERE extname='vector';"
```

### Backup database
```bash
docker-compose exec postgres pg_dump -U postgres legaledge > backup.sql
```

### Restore database
```bash
docker-compose exec -T postgres psql -U postgres -d legaledge < backup.sql
```

---

## 📦 Build Issues

### Backend build fails
```bash
# Rebuild backend only
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Frontend build fails
```bash
# Rebuild frontend only
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Permission issues on macOS
```bash
# Give Docker access to your files
# Go to Docker Desktop → Settings → Resources → File Sharing
# Add: /Users/arsalanahmadkhan/Documents/Legal Chatbot
```

---

## 🎯 Recommended Approach

For **development**, I recommend the **hybrid approach** (Solution 3):

✅ **PostgreSQL in Docker** - Isolated, consistent  
✅ **Backend locally** - Fast reloading, easier debugging  
✅ **Frontend locally** - Fast hot-reload, better DX  

For **production**, use full Docker deployment or:
- Frontend on Vercel
- Backend on Railway/Render  
- PostgreSQL managed database

---

## 🚀 After Setup

Once everything is running:

### Test the backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"LegalEdge AI","timestamp":"..."}
```

### Open frontend
Open browser: http://localhost:3000

### Add documents
```bash
# If running locally
cd backend
source venv/bin/activate
python admin_embed_pdfs.py --pdf document.pdf --name "Name"

# If using Docker
docker-compose exec backend python admin_embed_pdfs.py --pdf /path/to/document.pdf --name "Name"
```

---

## 💡 Quick Commands Reference

| Action | Command |
|--------|---------|
| Start all | `./docker-start.sh` or `docker-compose up -d` |
| Stop all | `./docker-stop.sh` or `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Restart | `docker-compose restart` |
| Rebuild | `docker-compose up -d --build` |
| Clean slate | `docker-compose down -v && docker-compose up -d --build` |
| PostgreSQL shell | `docker-compose exec postgres psql -U postgres -d legaledge` |

---

## ✅ Success Checklist

After setup, verify:

- [ ] `docker-compose ps` shows all services as "Up"
- [ ] `curl http://localhost:8000/health` returns healthy status
- [ ] http://localhost:3000 shows the LegalEdge AI interface
- [ ] PostgreSQL has vector extension: `docker-compose exec postgres psql -U postgres -d legaledge -c "SELECT * FROM pg_extension WHERE extname='vector';"`
- [ ] No errors in logs: `docker-compose logs`

---

**Still having issues?** 

1. Make sure Docker Desktop is running
2. Try the **hybrid approach** (PostgreSQL in Docker, apps locally)
3. Check the main **SETUP_GUIDE.md** for local setup
4. Review logs: `docker-compose logs -f`

---

**Pro Tip:** For fastest development experience, use PostgreSQL in Docker but run backend/frontend locally with `./start.sh`!

