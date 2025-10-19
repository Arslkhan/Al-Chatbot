# ⚡ LegalEdge AI - Quick Reference

## 🚀 Quick Start Commands

### Start Everything (Easiest)
```bash
./start.sh
```
- Installs dependencies
- Starts PostgreSQL
- Starts backend on :8000
- Starts frontend on :3000

### Stop Everything
```bash
./stop.sh
```
or press `Ctrl+C` in the terminal running `start.sh`

---

## 🔧 Manual Commands

### Backend

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload

# Alternative: Run with Python
python main.py
```

### Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Database

```bash
# Start PostgreSQL
brew services start postgresql@14

# Stop PostgreSQL
brew services stop postgresql@14

# Connect to database
psql -d legaledge

# Check database status
brew services list | grep postgresql
```

---

## 📚 Document Management

### Embed a PDF

```bash
cd backend
source venv/bin/activate

python admin_embed_pdfs.py \
  --pdf path/to/document.pdf \
  --name "Document Name" \
  --language en
```

### Options
- `--pdf`: Path to PDF file (required)
- `--name`: Display name for document (required)
- `--language`: `en` or `ar` (default: `en`)
- `--init-db`: Initialize database first time only

### Example
```bash
# English document
python admin_embed_pdfs.py \
  --pdf ~/Documents/dubai_tenancy_law.pdf \
  --name "Dubai Tenancy Law No. 26 of 2007" \
  --language en

# Arabic document
python admin_embed_pdfs.py \
  --pdf ~/Documents/rera_guidelines_ar.pdf \
  --name "RERA Guidelines" \
  --language ar
```

---

## 🗄️ Database Commands

### Check Document Count
```bash
psql -d legaledge -c "SELECT COUNT(*) FROM documents;"
```

### Check Conversation Count
```bash
psql -d legaledge -c "SELECT COUNT(*) FROM conversations;"
```

### View Recent Messages
```bash
psql -d legaledge -c "SELECT * FROM messages ORDER BY created_at DESC LIMIT 10;"
```

### Clear All Data (⚠️ Dangerous!)
```bash
psql -d legaledge -c "TRUNCATE conversations, messages, citations, feedbacks, documents CASCADE;"
```

### Backup Database
```bash
pg_dump legaledge > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql -d legaledge < backup_20251018.sql
```

---

## 🔍 Testing & Debugging

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are tenant rights in Dubai?", "language": "en"}'
```

### View Analytics
```bash
curl http://localhost:8000/api/analytics
```

### View Backend Logs
```bash
tail -f backend.log
```

### View Frontend Logs
```bash
tail -f frontend.log
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Check Python dependencies
cd backend
source venv/bin/activate
pip list
```

### Frontend won't start
```bash
# Check if port 3000 is in use
lsof -i :3000

# Kill process on port 3000
kill -9 $(lsof -t -i:3000)

# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database connection error
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Restart PostgreSQL
brew services restart postgresql@14

# Check database exists
psql -l | grep legaledge
```

### OpenAI API error
```bash
# Check API key in .env
cat backend/.env | grep OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 📦 Docker Commands (Optional)

### Start with Docker Compose
```bash
docker-compose up -d
```

### Stop Docker services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Rebuild containers
```bash
docker-compose up -d --build
```

---

## 🔑 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user@localhost:5432/legaledge
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Useful URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Redoc | http://localhost:8000/redoc | Alternative API docs |
| Health | http://localhost:8000/health | Health check endpoint |

---

## 🎯 Common Tasks

### Add new legal document
1. Get PDF file
2. Run embed script: `python admin_embed_pdfs.py --pdf file.pdf --name "Name"`
3. Test with related question in chat

### Update system prompt
1. Edit `backend/main.py`
2. Find `SYSTEM_PROMPT_EN` or `SYSTEM_PROMPT_AR`
3. Modify text
4. Restart backend

### Change UI colors
1. Edit `frontend/tailwind.config.ts`
2. Modify colors in `theme.extend.colors`
3. Save (Next.js will auto-reload)

### View conversation history
```bash
# Via API
curl http://localhost:8000/api/conversations/CONVERSATION_ID

# Via database
psql -d legaledge -c "SELECT * FROM messages WHERE conversation_id='ID';"
```

---

## 🚀 Deployment Checklist

### Before Deploying
- [ ] Test locally with real documents
- [ ] Check all environment variables
- [ ] Run production build: `npm run build`
- [ ] Test production build: `npm start`
- [ ] Backup database
- [ ] Update CORS origins in backend

### Vercel (Frontend)
1. Connect GitHub repo
2. Add environment variables
3. Deploy

### Railway (Backend)
1. Create project
2. Add PostgreSQL
3. Connect GitHub
4. Add environment variables
5. Run: `alembic upgrade head`

---

## 📝 Git Commands

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote
git remote add origin https://github.com/username/legaledge-ai.git

# Push
git push -u origin main
```

---

## 💡 Tips & Tricks

### Speed up embeddings
- Process PDFs in batches
- Use smaller chunk sizes for faster processing
- Consider caching embeddings

### Improve response quality
- Add more relevant documents
- Tune system prompts
- Adjust temperature (lower = more consistent)
- Increase top-k for more context

### Reduce costs
- Use GPT-4o-mini (already configured)
- Cache frequent queries
- Optimize chunk sizes
- Batch embed requests

### Better UX
- Add loading states
- Show progress for long operations
- Add error boundaries
- Implement retry logic

---

## 🆘 Getting Help

1. **Check logs:** `tail -f backend.log frontend.log`
2. **Review README.md:** Comprehensive setup guide
3. **Check SETUP_GUIDE.md:** Step-by-step instructions
4. **Review ARCHITECTURE.md:** System design details
5. **API Docs:** http://localhost:8000/docs
6. **PostgreSQL docs:** https://www.postgresql.org/docs/
7. **FastAPI docs:** https://fastapi.tiangolo.com/
8. **Next.js docs:** https://nextjs.org/docs

---

## 🎓 Key Concepts

**RAG:** Retrieval-Augmented Generation - AI with custom knowledge base  
**Embedding:** Vector representation of text for similarity search  
**pgvector:** PostgreSQL extension for vector similarity search  
**Cosine Similarity:** Measure of document relevance  
**Confidence Score:** How sure the AI is about its answer  
**Citation:** Source document reference for transparency  

---

**Quick Reference Version:** 1.0  
**Last Updated:** October 2025

---

**💪 You've got this! If stuck, start with `./start.sh` and check the logs.**

