# 🏛️ LegalEdge AI - Dubai Real Estate Legal Chatbot

> **Bilingual (Arabic + English) AI chatbot providing accurate, law-grounded answers for Dubai real estate & tenancy laws with citations, confidence levels, and legal disclaimers.**

Built for launch within 4–5 weeks by a solo developer with a budget < AED 10k. This MVP focuses on speed, accuracy, and reliability.

---

## 🎯 Features

✅ **Bilingual Chat** (English / Arabic with auto-detect)  
✅ **RAG (Retrieval-Augmented Generation)** with document citations  
✅ **Dubai-only jurisdiction** (expandable to other emirates)  
✅ **"I'm not sure" fallback** + handoff suggestion  
✅ **Legal disclaimer** visible in UI  
✅ **Admin script** to embed PDFs (tenancy law, RERA circulars)  
✅ **Analytics logging & feedback**  
✅ **Stripe/Tap Payments** integration (optional)

---

## 🛠️ Tech Stack

| Layer | Tool / Framework | Reason |
|-------|------------------|--------|
| **Frontend** | Next.js + Tailwind | Fast, modern, SSR ready |
| **Backend** | FastAPI (Python) | Easy OpenAI + vector DB integration |
| **Database** | Postgres + pgvector | Store embeddings, documents, logs |
| **Embeddings** | text-embedding-3-large | Multilingual (Arabic + English) |
| **LLM API** | GPT-4o-mini | Great quality-cost balance |
| **Hosting** | Vercel (frontend) + Railway/Render (backend) | Free-tier friendly |
| **Analytics** | PostHog (optional) | Session & feedback tracking |

---

## 📁 Project Structure

```
Legal Chatbot/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main API endpoints
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy models
│   ├── rag_engine.py          # RAG retrieval engine
│   ├── language_detector.py   # Language detection
│   ├── admin_embed_pdfs.py    # PDF embedding script
│   ├── requirements.txt       # Python dependencies
│   ├── env.example            # Environment variables template
│   ├── Dockerfile             # Docker configuration
│   └── alembic/               # Database migrations
│
├── frontend/                   # Next.js frontend
│   ├── app/
│   │   ├── page.tsx           # Main page
│   │   ├── layout.tsx         # Layout component
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── ChatInterface.tsx  # Main chat interface
│   │   ├── MessageBubble.tsx  # Message display
│   │   ├── Header.tsx         # App header
│   │   ├── Disclaimer.tsx     # Legal disclaimer
│   │   ├── WelcomeScreen.tsx  # Welcome screen
│   │   └── FeedbackWidget.tsx # Feedback component
│   ├── package.json           # Node dependencies
│   ├── env.local.example      # Environment variables template
│   └── Dockerfile             # Docker configuration
│
├── docker-compose.yml         # Docker Compose setup
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and **npm**
- **Python** 3.11+
- **PostgreSQL** 14+ with **pgvector** extension
- **OpenAI API Key**

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd "Legal Chatbot"
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/env.example backend/.env
   # Edit backend/.env and add your OPENAI_API_KEY
   
   # Frontend
   cp frontend/env.local.example frontend/.env.local
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL with pgvector**
   ```bash
   # Install PostgreSQL (if not installed)
   # macOS: brew install postgresql@14
   # Ubuntu: sudo apt-get install postgresql-14
   
   # Start PostgreSQL
   # macOS: brew services start postgresql@14
   # Ubuntu: sudo systemctl start postgresql
   
   # Create database
   psql -U postgres
   CREATE DATABASE legaledge;
   CREATE EXTENSION vector;
   \q
   ```

5. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your credentials
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the backend**
   ```bash
   python main.py
   # Or: uvicorn main:app --reload
   ```

   Backend will be available at: http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp env.local.example .env.local
   # Edit .env.local if needed
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

---

## 📚 Embedding Legal Documents

To add legal documents (PDFs) to the knowledge base:

1. **Navigate to backend directory**
   ```bash
   cd backend
   source venv/bin/activate  # Activate virtual environment
   ```

2. **Embed a PDF document**
   ```bash
   python admin_embed_pdfs.py \
     --pdf path/to/document.pdf \
     --name "Dubai Tenancy Law No. 26 of 2007" \
     --language en \
     --init-db  # Only needed first time
   ```

3. **Example documents to embed:**
   - Dubai Tenancy Law No. 26 of 2007
   - RERA Circulars and Guidelines
   - Dubai Land Department Regulations
   - Real Estate Regulatory Authority (RERA) Rules

---

## 🔧 Configuration

### Backend Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legaledge

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app

# Analytics (Optional)
POSTHOG_API_KEY=your-posthog-key
POSTHOG_HOST=https://app.posthog.com

# Payment Processing (Optional)
STRIPE_SECRET_KEY=sk_test_your-stripe-key
TAP_PAYMENTS_API_KEY=your-tap-payments-key

# Environment
ENVIRONMENT=development
DEBUG=True
```

### Frontend Environment Variables

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Stripe (Optional)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-key

# PostHog Analytics (Optional)
NEXT_PUBLIC_POSTHOG_KEY=your-posthog-key
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
```

---

## 📊 API Endpoints

### Health Check
```
GET /health
```

### Chat
```
POST /api/chat
Body: {
  "message": "What are tenant rights in Dubai?",
  "conversation_id": "optional-session-id",
  "language": "en"  // or "ar"
}

Response: {
  "response": "...",
  "conversation_id": "...",
  "language": "en",
  "citations": [...],
  "confidence": 0.85,
  "needs_lawyer": false,
  "timestamp": "..."
}
```

### Feedback
```
POST /api/feedback
Body: {
  "message_id": "...",
  "rating": 5,
  "comment": "Very helpful!"
}
```

### Get Conversation History
```
GET /api/conversations/{conversation_id}
```

### Analytics (Admin)
```
GET /api/analytics
```

Full API documentation available at: http://localhost:8000/docs

---

## 🚢 Deployment

### Frontend (Vercel)

1. **Push code to GitHub**
2. **Import project in Vercel**
3. **Set environment variables:**
   - `NEXT_PUBLIC_API_URL=https://your-backend-url.com`
4. **Deploy!**

### Backend (Railway / Render)

#### Railway

1. **Create new project**
2. **Add PostgreSQL plugin** (automatically provisions database with pgvector)
3. **Deploy from GitHub**
4. **Set environment variables** (especially `OPENAI_API_KEY`)
5. **Run migration:** `alembic upgrade head`

#### Render

1. **Create new Web Service**
2. **Add PostgreSQL database**
3. **Connect GitHub repository**
4. **Set environment variables**
5. **Build command:** `pip install -r requirements.txt`
6. **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 💰 Cost Estimation

### MVP Budget (< AED 10k / ~$2,700)

| Service | Cost (Monthly) | Notes |
|---------|----------------|-------|
| **OpenAI API** | ~$50-200 | GPT-4o-mini + embeddings |
| **Vercel** | $0 | Free tier (hobby) |
| **Railway/Render** | $5-20 | Hobby/Starter plan |
| **PostgreSQL** | $0-7 | Included or starter DB |
| **Domain** | $10-15/year | .ae or .com domain |
| **PostHog** | $0 | Free tier (1M events/mo) |
| **Total** | **~$55-235/mo** | **~AED 200-860/mo** |

**Total 5-week MVP cost: ~AED 1,000-4,300** (well under budget!)

---

## 🎨 Features in Detail

### 1. Bilingual Support (Arabic + English)
- Auto-detects language from user input
- Separate system prompts for each language
- Arabic-optimized fonts and RTL text direction

### 2. RAG with Citations
- Embeds legal documents using OpenAI's `text-embedding-3-large`
- Retrieves top-K relevant chunks using pgvector similarity search
- Displays source citations with page numbers

### 3. Confidence Scoring
- Calculates confidence based on retrieval scores
- Visual indicators (high/medium/low confidence)
- Suggests lawyer consultation for low confidence or complex issues

### 4. User Feedback
- Thumbs up/down rating system
- Optional comment collection
- Stored for analytics and improvement

### 5. Analytics Dashboard
- Total conversations and messages
- Average user rating
- Language breakdown (English vs Arabic)

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📈 Future Enhancements

- [ ] Multi-emirate support (Abu Dhabi, Sharjah, etc.)
- [ ] Voice input/output in both languages
- [ ] Document upload for contract review
- [ ] Lawyer marketplace integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant SaaS version
- [ ] WhatsApp/Telegram bot integration

---

## 🔐 Security & Compliance

- ⚠️ **Important:** This is general legal information only
- Always include disclaimers in all responses
- Never provide specific legal advice
- Recommend licensed lawyers for complex matters
- Store user data securely (GDPR-compliant if applicable)
- Use HTTPS in production
- Sanitize all user inputs
- Rate limiting to prevent abuse

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 🤝 Contributing

This is a private MVP project. For inquiries, contact the project owner.

---

## 📧 Support

For issues or questions:
- Backend API: Check logs in `backend/` directory
- Frontend: Check browser console
- Database: Check PostgreSQL logs
- General: Review this README or API docs at `/docs`

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4o-mini and embeddings
- **FastAPI** for excellent Python API framework
- **Next.js** for modern React framework
- **pgvector** for vector similarity search
- **Dubai Land Department** and **RERA** for legal resources

---

**Built with ❤️ for the UAE legal tech community**

*LegalEdge AI - Making legal information accessible to everyone*

