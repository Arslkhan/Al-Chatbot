# 🚀 Deployment Guide - LegalEdge AI

Deploy your LegalEdge AI chatbot to Railway (backend) and Vercel (frontend).

---

## 📋 **Prerequisites**

### Required Accounts:
- ✅ **Railway Account**: https://railway.app (Free tier available)
- ✅ **Vercel Account**: https://vercel.com (Free tier available)
- ✅ **GitHub Account**: For code repository
- ✅ **OpenAI Account**: With API key and billing enabled

### Required Tools:
- ✅ **Git**: For version control
- ✅ **Node.js**: For frontend builds
- ✅ **Python**: For backend (handled by Railway)

---

## 🗄️ **Database Setup (Railway PostgreSQL)**

### Step 1: Create PostgreSQL Database on Railway
1. Go to https://railway.app
2. Click "New Project"
3. Choose "Provision PostgreSQL"
4. Wait for database to be created
5. Copy the **DATABASE_URL** from the Variables tab

### Step 2: Enable pgvector Extension
1. In Railway dashboard, go to your PostgreSQL service
2. Click "Query" tab
3. Run this SQL command:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## 🔧 **Backend Deployment (Railway)**

### Step 1: Prepare Repository
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/legaledge-ai.git
git push -u origin main
```

### Step 2: Deploy to Railway
1. Go to https://railway.app
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the backend folder

### Step 3: Configure Environment Variables
In Railway dashboard, add these environment variables:

```bash
DATABASE_URL=postgresql://postgres:password@hostname:port/database
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
PORT=8000
```

### Step 4: Deploy
1. Railway will automatically build and deploy
2. Wait for deployment to complete
3. Copy the generated URL (e.g., `https://your-app.railway.app`)

---

## 🎨 **Frontend Deployment (Vercel)**

### Step 1: Prepare Frontend Environment
Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

### Step 2: Deploy to Vercel
1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 3: Set Environment Variables
In Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Your Railway backend URL

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build to complete
3. Get your Vercel URL (e.g., `https://your-app.vercel.app`)

---

## 🔄 **Database Migration (Railway)**

### Step 1: Connect to Railway Database
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Connect to your project
railway link

# Connect to database
railway connect
```

### Step 2: Run Database Migrations
```bash
# In your local backend directory
cd backend

# Run Alembic migrations
alembic upgrade head

# Or create tables manually if needed
python -c "
from database import init_db
init_db()
print('Database initialized!')
"
```

### Step 3: Embed Documents
```bash
# Embed your PDF documents
python admin_embed_pdfs.py
```

---

## 🧪 **Testing Deployment**

### Test Backend (Railway):
```bash
curl https://your-railway-app.railway.app/health
curl -X POST https://your-railway-app.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is EJARI?"}'
```

### Test Frontend (Vercel):
1. Visit your Vercel URL
2. Try asking a question
3. Verify it connects to Railway backend

---

## 🔐 **Environment Variables Reference**

### Railway (Backend):
```bash
DATABASE_URL=postgresql://postgres:password@hostname:port/database
OPENAI_API_KEY=sk-proj-your-openai-api-key
PORT=8000
```

### Vercel (Frontend):
```bash
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

---

## 📊 **Monitoring & Maintenance**

### Railway Dashboard:
- Monitor backend logs
- Check database connections
- View deployment status

### Vercel Dashboard:
- Monitor frontend builds
- Check deployment logs
- View analytics

### Health Checks:
- Backend: `https://your-app.railway.app/health`
- Frontend: Your Vercel URL should load

---

## 🚨 **Troubleshooting**

### Common Issues:

#### 1. **Database Connection Error**
```bash
# Check DATABASE_URL format
# Ensure pgvector extension is installed
# Verify database is running
```

#### 2. **OpenAI API Errors**
```bash
# Check API key is valid
# Ensure billing is enabled
# Verify quota limits
```

#### 3. **CORS Issues**
```bash
# Backend CORS is configured for all origins
# Check if Railway URL is correct in frontend
```

#### 4. **Build Failures**
```bash
# Check Railway logs for Python errors
# Check Vercel logs for Node.js errors
# Verify all dependencies are in requirements.txt
```

---

## 💰 **Cost Estimation**

### Railway (Free Tier):
- ✅ **$0/month** for small apps
- ✅ **512MB RAM**, **1 CPU**
- ✅ **1GB PostgreSQL** database

### Vercel (Free Tier):
- ✅ **$0/month** for personal projects
- ✅ **100GB bandwidth**
- ✅ **Unlimited static deployments**

### OpenAI API:
- ✅ **~$5-15/month** for 1,000-3,000 queries
- ✅ **Pay-as-you-go** pricing

**Total Monthly Cost: ~$5-15** 💰

---

## 🎯 **Production Checklist**

### Before Going Live:
- [ ] ✅ OpenAI billing enabled
- [ ] ✅ Database migrations completed
- [ ] ✅ Documents embedded
- [ ] ✅ Environment variables set
- [ ] ✅ Custom domain configured (optional)
- [ ] ✅ SSL certificates working
- [ ] ✅ Health checks passing
- [ ] ✅ Error monitoring set up

### Post-Deployment:
- [ ] ✅ Test all endpoints
- [ ] ✅ Verify chat functionality
- [ ] ✅ Check error logs
- [ ] ✅ Monitor performance
- [ ] ✅ Set up analytics (optional)

---

## 🚀 **Quick Deploy Commands**

### Railway (Backend):
```bash
# Deploy backend
railway login
railway init
railway up
```

### Vercel (Frontend):
```bash
# Deploy frontend
cd frontend
vercel login
vercel --prod
```

---

## 📞 **Support**

### Railway Support:
- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway

### Vercel Support:
- Documentation: https://vercel.com/docs
- Discord: https://vercel.com/discord

---

## 🎉 **Success!**

Once deployed, your LegalEdge AI chatbot will be:
- ✅ **Live on the internet**
- ✅ **Accessible from anywhere**
- ✅ **Scalable and reliable**
- ✅ **Production-ready**

**Frontend URL**: https://your-app.vercel.app  
**Backend URL**: https://your-app.railway.app

---

**Happy Deploying!** 🚀✨
