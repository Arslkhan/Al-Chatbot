# 🚀 LegalEdge AI - Complete Setup Guide

This guide will walk you through setting up LegalEdge AI from scratch.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **macOS** (you're on macOS 24.6.0)
- [ ] **Node.js 18+** - [Download](https://nodejs.org/)
- [ ] **Python 3.11+** - [Download](https://www.python.org/)
- [ ] **PostgreSQL 14+** - Install via Homebrew
- [ ] **OpenAI API Key** - [Get one](https://platform.openai.com/api-keys)
- [ ] **Code editor** (VS Code, Cursor, etc.)

---

## 🔧 Step 1: Install PostgreSQL with pgvector

```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create database
psql postgres
CREATE DATABASE legaledge;

# Enable pgvector extension
\c legaledge
CREATE EXTENSION vector;
\q
```

**Verify installation:**
```bash
psql -U $USER -d legaledge -c "SELECT version();"
```

---

## 🐍 Step 2: Backend Setup

### 2.1 Navigate to backend directory

```bash
cd "/Users/arsalanahmadkhan/Documents/Legal Chatbot/backend"
```

### 2.2 Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Configure environment variables

```bash
# Copy example env file
cp env.example .env

# Edit .env file
nano .env
```

**Update these values in `.env`:**
```env
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/legaledge
```

Replace `YOUR_USERNAME` with your Mac username (run `whoami` to find it).

### 2.5 Initialize database

```bash
# Create tables
python -c "from database import init_db; init_db()"
```

### 2.6 Test backend

```bash
# Start server
uvicorn main:app --reload

# In another terminal, test health endpoint
curl http://localhost:8000/health
```

You should see:
```json
{"status":"healthy","service":"LegalEdge AI","timestamp":"..."}
```

**Keep backend running!** ✅

---

## 🎨 Step 3: Frontend Setup

Open a **new terminal window**.

### 3.1 Navigate to frontend directory

```bash
cd "/Users/arsalanahmadkhan/Documents/Legal Chatbot/frontend"
```

### 3.2 Install Node dependencies

```bash
npm install
```

This may take a few minutes. Go grab a coffee! ☕

### 3.3 Configure environment variables

```bash
# Copy example env file
cp env.local.example .env.local
```

The default values should work for local development:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3.4 Start frontend

```bash
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## 🎉 Step 4: Test the Application

1. **Open browser:** http://localhost:3000

2. **You should see:**
   - LegalEdge AI header
   - Legal disclaimer (amber warning box)
   - Welcome screen with features list

3. **Try chatting:**
   - Type: "What are tenant rights in Dubai?"
   - Click Send or press Enter

4. **Expected behavior:**
   - Message appears in chat
   - AI responds (may take a few seconds)
   - Response includes confidence score
   - Since there are no documents yet, confidence will be low

**If you see this, congratulations! 🎊 The basic setup is working.**

---

## 📚 Step 5: Add Legal Documents (Important!)

Without documents, the chatbot can't provide accurate, cited information.

### 5.1 Prepare PDF documents

Gather Dubai real estate legal documents:
- Dubai Tenancy Law No. 26 of 2007
- RERA circulars and guidelines
- Dubai Land Department regulations

Save them in a folder, e.g., `~/Documents/Legal_PDFs/`

### 5.2 Embed documents

```bash
# Navigate to backend (if not already there)
cd "/Users/arsalanahmadkhan/Documents/Legal Chatbot/backend"

# Activate virtual environment
source venv/bin/activate

# Embed a document
python admin_embed_pdfs.py \
  --pdf ~/Documents/Legal_PDFs/dubai_tenancy_law.pdf \
  --name "Dubai Tenancy Law No. 26 of 2007" \
  --language en
```

**This will:**
- Extract text from PDF
- Split into chunks
- Generate embeddings using OpenAI
- Store in PostgreSQL with pgvector

**Repeat for each document:**
```bash
# Arabic document example
python admin_embed_pdfs.py \
  --pdf ~/Documents/Legal_PDFs/rera_guidelines_ar.pdf \
  --name "RERA Guidelines (Arabic)" \
  --language ar
```

**💡 Tip:** Each document will cost ~$0.01-0.10 in OpenAI API fees depending on size.

---

## 🔍 Step 6: Verify Everything Works

### 6.1 Test with embedded documents

1. Go back to http://localhost:3000
2. Clear chat (click "Clear Chat" button)
3. Ask: "What are the notice requirements for lease termination in Dubai?"
4. You should now see:
   - Higher confidence score (>70%)
   - Citations from your embedded documents
   - Source names and page numbers

### 6.2 Test bilingual support

1. Click the language toggle (العربية)
2. UI should flip to RTL (right-to-left)
3. Ask in Arabic: "ما هي حقوق المستأجر في دبي؟"
4. AI should respond in Arabic

### 6.3 Test feedback system

1. After receiving a response, click 👍 or 👎
2. If you click 👎, a comment box should appear
3. Submit feedback
4. Check backend logs to confirm it was saved

---

## 🐛 Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# If not running:
brew services start postgresql@14
```

### Frontend won't start

**Error:** `Module not found: Can't resolve 'lucide-react'`
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Can't connect to backend from frontend

**Error in browser console:** `Network Error`
```bash
# Check backend is running on port 8000
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
# Make sure http://localhost:3000 is in allow_origins
```

### Embedding script fails

**Error:** `openai.error.AuthenticationError`
```bash
# Check your API key in backend/.env
# Make sure it's valid and has credits
```

**Error:** `psycopg2.errors.UndefinedTable: relation "documents" does not exist`
```bash
# Initialize database
cd backend
source venv/bin/activate
python -c "from database import init_db; init_db()"
```

---

## 🚀 Next Steps

Now that everything is working locally:

1. **Add more documents** - The more legal documents you embed, the better the chatbot will be

2. **Customize prompts** - Edit system prompts in `backend/main.py` to match your use case

3. **Test thoroughly** - Try various questions in both English and Arabic

4. **Deploy to production** - Follow deployment instructions in main README.md

5. **Add analytics** - Set up PostHog for user tracking (optional)

6. **Add payments** - Integrate Stripe or Tap Payments (optional)

---

## 📊 Monitoring

### Check database contents

```bash
psql -d legaledge -c "SELECT COUNT(*) FROM documents;"
psql -d legaledge -c "SELECT COUNT(*) FROM conversations;"
psql -d legaledge -c "SELECT COUNT(*) FROM messages;"
```

### View backend logs

Backend logs will show:
- API requests
- Embedding generation
- Database queries
- Errors

### View analytics

```bash
curl http://localhost:8000/api/analytics
```

---

## 🎓 Learning Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Next.js Docs:** https://nextjs.org/docs
- **OpenAI API Docs:** https://platform.openai.com/docs
- **pgvector GitHub:** https://github.com/pgvector/pgvector
- **Dubai Land Department:** https://dubailand.gov.ae/

---

## ✅ Setup Complete!

You now have a fully functional LegalEdge AI chatbot running locally!

**What you've accomplished:**
- ✅ Backend API with RAG
- ✅ PostgreSQL with pgvector
- ✅ Beautiful bilingual frontend
- ✅ Document embedding system
- ✅ Feedback and analytics

**Next:** Start building your knowledge base by embedding legal documents!

---

**Questions?** Review the main README.md or check the troubleshooting section above.

**Happy coding! 🚀**

