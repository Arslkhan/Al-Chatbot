# 🏗️ LegalEdge AI - Architecture Documentation

## System Overview

LegalEdge AI is a **bilingual RAG-powered legal chatbot** designed specifically for Dubai real estate and tenancy law. The system combines modern web technologies with AI to provide accurate, cited legal information.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                    (English / Arabic UI)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Next.js Frontend (Vercel)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • React Components (TypeScript)                      │  │
│  │  • Tailwind CSS (Bilingual RTL/LTR)                 │  │
│  │  • Real-time Chat Interface                          │  │
│  │  • Feedback & Analytics                              │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Railway/Render)               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • RAG Engine (Retrieval-Augmented Generation)       │  │
│  │  • Language Detection (Arabic/English)               │  │
│  │  • Conversation Management                           │  │
│  │  • Citation Generation                               │  │
│  │  • Confidence Scoring                                │  │
│  └──────────────────────────────────────────────────────┘  │
└───────┬──────────────────────┬──────────────────────────────┘
        │                      │
        ▼                      ▼
┌──────────────────┐    ┌──────────────────────────────────┐
│   OpenAI API     │    │  PostgreSQL + pgvector          │
│  GPT-4o-mini     │    │  ┌────────────────────────────┐ │
│  + Embeddings    │    │  │  • Conversations           │ │
│                  │    │  │  • Messages                │ │
│                  │    │  │  • Documents (Embeddings)  │ │
│                  │    │  │  • Feedback & Analytics    │ │
│                  │    │  └────────────────────────────┘ │
└──────────────────┘    └──────────────────────────────────┘
```

---

## Component Details

### 1. Frontend (Next.js + Tailwind)

**Location:** `/frontend`

**Key Components:**
- `app/page.tsx` - Main application entry point
- `components/ChatInterface.tsx` - Chat UI and message handling
- `components/MessageBubble.tsx` - Individual message rendering with citations
- `components/Header.tsx` - Navigation and language switcher
- `components/FeedbackWidget.tsx` - User feedback collection

**Features:**
- **Bilingual UI:** Seamless English ↔ Arabic switching with RTL support
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Real-time Chat:** Instant message updates with typing indicators
- **Citation Display:** Shows source documents and page numbers
- **Confidence Indicators:** Visual confidence scores (high/medium/low)

**Tech Stack:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Axios (API calls)
- React Markdown (message rendering)
- Lucide React (icons)

---

### 2. Backend (FastAPI)

**Location:** `/backend`

**Core Files:**
- `main.py` - API endpoints and business logic
- `rag_engine.py` - RAG retrieval and embeddings
- `database.py` - Database configuration
- `models.py` - SQLAlchemy models
- `language_detector.py` - Language detection utilities
- `admin_embed_pdfs.py` - PDF processing and embedding script

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Send message and get AI response |
| `/api/feedback` | POST | Submit user feedback |
| `/api/analytics` | GET | Get usage analytics |
| `/api/conversations/{id}` | GET | Retrieve conversation history |

**Tech Stack:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- pgvector (Vector similarity search)
- OpenAI Python SDK
- PyPDF2 (PDF processing)
- Pydantic (Data validation)

---

### 3. Database (PostgreSQL + pgvector)

**Schema:**

```sql
-- Conversations
conversations
  - id (PK)
  - language (en/ar)
  - created_at

-- Messages
messages
  - id (PK)
  - conversation_id (FK)
  - content (text)
  - is_user (boolean)
  - language (en/ar)
  - confidence (float)
  - created_at

-- Documents (Vector Store)
documents
  - id (PK)
  - source (document name)
  - page (integer)
  - chunk_index (integer)
  - content (text)
  - content_ar (text, optional)
  - embedding (vector[3072])
  - language (en/ar)
  - created_at

-- Citations
citations
  - id (PK)
  - message_id (FK)
  - source (document name)
  - page (integer)
  - excerpt (text)
  - relevance_score (float)

-- Feedback
feedbacks
  - id (PK)
  - message_id (FK)
  - rating (1-5)
  - comment (text, optional)
  - created_at
```

---

## Data Flow

### Chat Request Flow

```
1. User Types Message
   │
   ▼
2. Frontend sends POST /api/chat
   {
     "message": "What are tenant rights?",
     "conversation_id": "...",
     "language": "en"
   }
   │
   ▼
3. Backend: Language Detection
   │
   ▼
4. Backend: RAG Retrieval
   • Generate embedding for query
   • Search pgvector for top-K similar chunks
   • Calculate relevance scores
   │
   ▼
5. Backend: Build Context
   • Concatenate retrieved chunks
   • Select appropriate system prompt
   • Add conversation history
   │
   ▼
6. Backend: Call OpenAI API
   • GPT-4o-mini with context
   • Temperature: 0.3 (consistent legal info)
   │
   ▼
7. Backend: Post-processing
   • Calculate confidence score
   • Determine if lawyer needed
   • Format citations
   │
   ▼
8. Backend: Save to Database
   • Store user message
   • Store assistant response
   • Store citations
   │
   ▼
9. Frontend: Display Response
   • Render message with markdown
   • Show citations
   • Display confidence indicator
   • Show lawyer warning if needed
```

---

## RAG (Retrieval-Augmented Generation)

### How It Works

1. **Document Ingestion:**
   ```
   PDF → Text Extraction → Chunking (1000 chars) → Embedding → pgvector
   ```

2. **Query Processing:**
   ```
   User Query → Embedding → Cosine Similarity Search → Top-K Chunks
   ```

3. **Response Generation:**
   ```
   Context (chunks) + System Prompt + Query → GPT-4o-mini → Response
   ```

### Embedding Model

- **Model:** `text-embedding-3-large`
- **Dimensions:** 3072
- **Language Support:** Multilingual (English + Arabic)
- **Cost:** ~$0.00013 per 1K tokens

### Similarity Search

- **Method:** Cosine similarity (pgvector `<=>` operator)
- **Index:** IVFFlat or HNSW for fast search
- **Top-K:** 5 most relevant chunks per query

---

## Bilingual Support

### Language Detection

```python
def detect_language(text: str) -> str:
    arabic_chars = count(arabic_unicode_range)
    if arabic_chars / total_chars > 0.3:
        return 'ar'
    return 'en'
```

### System Prompts

- **English:** Optimized for legal clarity and precision
- **Arabic:** Native Arabic legal terminology and phrasing
- Both include:
  - Scope limitations (Dubai only)
  - Legal disclaimers
  - Citation requirements

### UI Adaptation

- **RTL (Right-to-Left):** Automatic for Arabic
- **Fonts:** 
  - English: Inter
  - Arabic: Noto Sans Arabic
- **Layout:** Flex-direction reversals for RTL

---

## Security Considerations

### 1. API Security
- **CORS:** Restricted to known frontends
- **Rate Limiting:** Prevent abuse (TODO)
- **Input Validation:** Pydantic models
- **SQL Injection:** Protected by SQLAlchemy ORM

### 2. Data Privacy
- **No PII Collection:** Only chat content stored
- **Conversations:** Isolated by session ID
- **HTTPS Only:** In production
- **API Keys:** Environment variables only

### 3. Legal Compliance
- **Disclaimers:** Every response
- **Confidence Scores:** Transparency
- **Lawyer Warnings:** For complex cases
- **No Legal Advice:** Information only

---

## Performance Optimization

### Frontend
- **Code Splitting:** Automatic with Next.js
- **Image Optimization:** Next.js Image component
- **Lazy Loading:** Components loaded on demand
- **Caching:** Static assets cached

### Backend
- **Connection Pooling:** SQLAlchemy
- **Async I/O:** FastAPI async endpoints
- **Vector Index:** Fast similarity search
- **Response Caching:** TODO (Redis)

### Database
- **Indexes:** On conversation_id, message_id
- **Vector Index:** IVFFlat/HNSW for pgvector
- **Query Optimization:** Limit conversation history

---

## Scalability

### Current (MVP)
- **Users:** ~100 concurrent
- **Requests:** ~1000/day
- **Database:** Single PostgreSQL instance
- **Hosting:** Free/hobby tiers

### Future Scaling
- **Horizontal Scaling:** Multiple backend instances
- **Load Balancer:** Distribute traffic
- **Database Replicas:** Read replicas for analytics
- **CDN:** Static assets on Cloudflare
- **Cache Layer:** Redis for hot data
- **Queue System:** Celery for async tasks

---

## Cost Analysis

### Per 1000 Conversations

| Component | Usage | Cost |
|-----------|-------|------|
| GPT-4o-mini | ~500 tokens/response | $0.15 |
| Embeddings | ~100 tokens/query | $0.013 |
| Hosting | Backend + DB | $0.10 |
| **Total** | | **~$0.26** |

### Monthly (1000 conversations)

- **OpenAI:** ~$160
- **Hosting:** ~$20
- **Total:** **~$180/month** (~AED 660)

---

## Monitoring & Analytics

### Metrics Tracked
- Total conversations
- Total messages
- Average response time
- Average confidence score
- User ratings (1-5)
- Language breakdown (EN/AR)

### Logging
- API requests/responses
- Error logs
- Embedding generation
- Database queries

### Future Analytics
- **PostHog:** User behavior tracking
- **Sentry:** Error monitoring
- **Prometheus + Grafana:** System metrics

---

## Development Workflow

### Local Development
```bash
# Start PostgreSQL
brew services start postgresql@14

# Start backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Start frontend
cd frontend
npm run dev
```

### Adding Documents
```bash
cd backend
python admin_embed_pdfs.py \
  --pdf path/to/doc.pdf \
  --name "Document Name" \
  --language en
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## Deployment

### Frontend (Vercel)
1. Connect GitHub repo
2. Set environment variables
3. Auto-deploy on push to main

### Backend (Railway)
1. Create new project
2. Add PostgreSQL plugin
3. Deploy from GitHub
4. Set environment variables
5. Run migrations

### Database
- **Development:** Local PostgreSQL
- **Production:** Railway/Render managed PostgreSQL
- **Backup:** Daily automated backups

---

## Testing Strategy

### Unit Tests
- RAG engine functions
- Language detection
- Database operations

### Integration Tests
- API endpoints
- Database queries
- OpenAI API calls

### E2E Tests
- Full chat flow
- Bilingual support
- Citation display

### Load Tests
- Concurrent users
- API response times
- Database performance

---

## Future Enhancements

### Phase 2 (Weeks 6-12)
- [ ] Advanced analytics dashboard
- [ ] Document upload for contract review
- [ ] Multi-emirate support
- [ ] Payment integration (Stripe/Tap)

### Phase 3 (Months 4-6)
- [ ] Voice input/output (Arabic + English)
- [ ] Mobile app (React Native)
- [ ] Lawyer marketplace
- [ ] WhatsApp/Telegram bot

### Phase 4 (6+ months)
- [ ] Multi-tenant SaaS
- [ ] Enterprise features
- [ ] Advanced NLP (entity extraction)
- [ ] Predictive analytics

---

## References

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Next.js Docs:** https://nextjs.org/docs
- **OpenAI API:** https://platform.openai.com/docs
- **pgvector:** https://github.com/pgvector/pgvector
- **Tailwind CSS:** https://tailwindcss.com/docs

---

**Last Updated:** October 2025  
**Version:** 1.0.0 (MVP)

