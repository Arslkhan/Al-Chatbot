"""
LegalEdge AI - Backend API
Dubai Real Estate Legal Chatbot with RAG
"""
import os
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import openai
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Conversation, Message, Feedback, Citation
from rag_engine import RAGEngine
from language_detector import detect_language, translate_if_needed

# Initialize FastAPI app
app = FastAPI(
    title="LegalEdge AI API",
    description="Dubai Real Estate Legal Chatbot",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = RAGEngine()

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY")


# ===== Pydantic Models =====

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    language: Optional[str] = None  # 'en' or 'ar', auto-detected if not provided


class CitationResponse(BaseModel):
    source: str
    page: Optional[int] = None
    excerpt: str
    relevance_score: float


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    language: str
    citations: List[CitationResponse]
    confidence: float  # 0.0 to 1.0
    timestamp: str
    needs_lawyer: bool = False


class FeedbackRequest(BaseModel):
    message_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class AnalyticsResponse(BaseModel):
    total_conversations: int
    total_messages: int
    avg_rating: float
    language_breakdown: Dict[str, int]


# ===== New API Contract Models =====

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    language: Optional[Literal["ar", "en"]] = None
    jurisdictionCode: Optional[str] = "DXB"


class Citation(BaseModel):
    title: str
    article: str
    version_date: Optional[str] = None
    source_url: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    confidence: Literal["High", "Medium", "Low"]
    citations: List[Citation]
    language: str
    jurisdiction: str = "DXB"


class EmbedDocument(BaseModel):
    title: str
    source_url: Optional[str] = None
    version_date: Optional[str] = None
    jurisdictionCode: str = "DXB"


class EmbedRequest(BaseModel):
    document: EmbedDocument
    text: str = Field(..., min_length=1)
    topic: Optional[str] = None
    language: Optional[Literal["ar", "en"]] = "en"


class EmbedResponse(BaseModel):
    documentId: str
    chunks: int


class FeedbackNewRequest(BaseModel):
    question: str
    answerId: Optional[str] = None
    helpful: bool


class FeedbackNewResponse(BaseModel):
    ok: bool = True


# ===== System Prompts =====

SYSTEM_PROMPT_EN = """You are LegalEdge AI, a specialized legal assistant for Dubai real estate and tenancy law.

Your role:
1. Provide accurate information based ONLY on UAE/Dubai real estate and tenancy laws
2. Always cite specific laws, articles, or regulations
3. Explain complex legal concepts in simple terms
4. Be bilingual (English and Arabic)

CRITICAL RULES:
- ONLY answer questions about Dubai real estate, tenancy, and property law
- If asked about other legal areas or jurisdictions, politely decline
- Always include relevant citations from official sources
- If you're not confident (confidence < 0.7), suggest consulting a licensed lawyer
- Never provide specific legal advice - only general legal information
- Always include appropriate disclaimers

DISCLAIMER: This is general legal information only. For advice specific to your situation, consult a licensed lawyer in Dubai.

Context from knowledge base:
{context}

Based on this context, provide accurate, cited information."""

SYSTEM_PROMPT_AR = """أنت LegalEdge AI، مساعد قانوني متخصص في قوانين العقارات والإيجارات في دبي.

دورك:
1. تقديم معلومات دقيقة بناءً فقط على قوانين العقارات والإيجارات في الإمارات/دبي
2. الاستشهاد دائمًا بالقوانين أو المواد أو اللوائح المحددة
3. شرح المفاهيم القانونية المعقدة بعبارات بسيطة
4. التحدث باللغتين (الإنجليزية والعربية)

قواعد حاسمة:
- أجب فقط على الأسئلة المتعلقة بالعقارات والإيجارات والملكية في دبي
- إذا سُئلت عن مجالات قانونية أخرى أو ولايات قضائية أخرى، ارفض بأدب
- قم دائمًا بتضمين الاستشهادات ذات الصلة من المصادر الرسمية
- إذا لم تكن واثقًا (الثقة < 0.7)، اقترح استشارة محامٍ مرخص
- لا تقدم أبدًا نصيحة قانونية محددة - معلومات قانونية عامة فقط
- قم دائمًا بتضمين إخلاء المسؤولية المناسب

إخلاء المسؤولية: هذه معلومات قانونية عامة فقط. للحصول على مشورة خاصة بحالتك، استشر محاميًا مرخصًا في دبي.

السياق من قاعدة المعرفة:
{context}

بناءً على هذا السياق، قدم معلومات دقيقة مع الاستشهادات."""


# ===== API Endpoints =====

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LegalEdge AI",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint with RAG
    """
    try:
        # Detect language if not provided
        language = request.language or detect_language(request.message)
        
        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(
                id=str(uuid4()),
                language=language,
                created_at=datetime.utcnow()
            )
            db.add(conversation)
            db.commit()
        
        # Retrieve relevant context using RAG
        rag_results = rag_engine.retrieve_context(
            query=request.message,
            language=language,
            top_k=5
        )
        
        # Build context string
        context = "\n\n".join([
            f"[{r['source']}] {r['text']}" for r in rag_results
        ])
        
        # Select system prompt based on language
        system_prompt = SYSTEM_PROMPT_AR if language == 'ar' else SYSTEM_PROMPT_EN
        system_prompt = system_prompt.format(context=context)
        
        # Get conversation history
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).limit(10).all()
        
        # Build messages for OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append({"role": "user" if msg.is_user else "assistant", "content": msg.content})
        messages.append({"role": "user", "content": request.message})
        
        # Call OpenAI API with intelligent fallback for testing phase
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent legal info
                max_tokens=1000
            )
            assistant_response = response.choices[0].message.content
        except Exception as e:
            if "quota" in str(e).lower() or "billing" in str(e).lower() or "rate" in str(e).lower():
                # TESTING MODE: Provide intelligent responses from RAG context without AI
                if context:
                    # Extract most relevant information from RAG results
                    top_results = "\n\n".join([
                        f"📄 **{r['source']}** (Page {r.get('page', 'N/A')})\n{r['text'][:400]}..."
                        for r in rag_results[:3]
                    ])
                    
                    if language == 'ar':
                        assistant_response = f"""🤖 **وضع الاختبار** - نظام LegalEdge AI (بدون OpenAI API)

📋 **سؤالك**: {request.message}

📚 **المعلومات القانونية ذات الصلة من دليل الإيجار في دبي**:

{top_results}

---

💡 **ملاحظة**: هذا الوضع التجريبي يعرض المحتوى ذي الصلة مباشرة من قاعدة المعرفة القانونية. عند إضافة رصيد OpenAI، سيقوم الذكاء الاصطناعي بتحليل هذه المعلومات وتقديم إجابات مخصصة وسهلة الفهم.

⚠️ **تنويه قانوني**: هذه معلومات عامة فقط من قانون الإيجار في دبي. للحصول على استشارة قانونية محددة لحالتك، يرجى التواصل مع محامٍ مرخص في دبي.

🔧 **للحصول على إجابات ذكية كاملة**: أضف $10-20 إلى حساب OpenAI الخاص بك. التكلفة الشهرية: ~$5-15 فقط."""
                    else:
                        assistant_response = f"""🤖 **TESTING MODE** - LegalEdge AI System (Without OpenAI API)

📋 **Your Question**: {request.message}

📚 **Relevant Legal Information from Dubai Tenancy Guide**:

{top_results}

---

💡 **Note**: This is a testing mode that displays relevant content directly from our legal knowledge base. Once you add OpenAI billing, the AI will analyze this information and provide customized, easy-to-understand answers with legal reasoning.

⚠️ **Legal Disclaimer**: This is general information only from Dubai tenancy law. For legal advice specific to your situation, please consult a licensed lawyer in Dubai.

🔧 **To get full AI-powered answers**: Add $10-20 to your OpenAI account. Monthly cost: only ~$5-15."""
                else:
                    # No context found
                    if language == 'ar':
                        assistant_response = """🤖 **وضع الاختبار**

عذراً، لم أجد معلومات ذات صلة في قاعدة البيانات الخاصة بنا حول هذا السؤال.

💡 يرجى التأكد من أن سؤالك يتعلق بـ:
- قانون الإيجار في دبي
- حقوق المستأجرين والمالكين
- العقارات في دبي
- نزاعات الإيجار

⚠️ **تنويه**: هذا الوضع التجريبي. عند إضافة رصيد OpenAI، سيتمكن النظام من الإجابة على نطاق أوسع من الأسئلة."""
                    else:
                        assistant_response = """🤖 **TESTING MODE**

Sorry, I couldn't find relevant information in our database about this question.

💡 Please ensure your question is related to:
- Dubai tenancy law
- Tenant and landlord rights
- Dubai real estate
- Rental disputes

⚠️ **Note**: This is testing mode. Once you add OpenAI billing, the system will be able to answer a wider range of questions."""
            else:
                raise ed 
        
        # Calculate confidence based on RAG results
        avg_score = sum(r['score'] for r in rag_results) / len(rag_results) if rag_results else 0.5
        confidence = min(avg_score, 1.0)
        
        # Determine if lawyer consultation is needed
        needs_lawyer = confidence < 0.7 or any(
            keyword in request.message.lower() 
            for keyword in ['sue', 'court', 'lawsuit', 'legal action', 'يقاضي', 'محكمة']
        )
        
        # Save messages to database
        user_msg = Message(
            id=str(uuid4()),
            conversation_id=conversation.id,
            content=request.message,
            is_user=True,
            language=language,
            created_at=datetime.utcnow()
        )
        db.add(user_msg)
        
        assistant_msg = Message(
            id=str(uuid4()),
            conversation_id=conversation.id,
            content=assistant_response,
            is_user=False,
            language=language,
            confidence=confidence,
            created_at=datetime.utcnow()
        )
        db.add(assistant_msg)
        
        # Save citations
        citations_response = []
        for result in rag_results[:3]:  # Top 3 citations
            citation = Citation(
                id=str(uuid4()),
                message_id=assistant_msg.id,
                source=result['source'],
                page=result.get('page'),
                excerpt=result['text'][:300],
                relevance_score=result['score']
            )
            db.add(citation)
            citations_response.append(CitationResponse(
                source=result['source'],
                page=result.get('page'),
                excerpt=result['text'][:200],
                relevance_score=result['score']
            ))
        
        db.commit()
        
        return ChatResponse(
            response=assistant_response,
            conversation_id=conversation.id,
            language=language,
            citations=citations_response,
            confidence=confidence,
            timestamp=datetime.utcnow().isoformat(),
            needs_lawyer=needs_lawyer
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    """Submit user feedback for a message"""
    try:
        message = db.query(Message).filter(Message.id == feedback.message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        feedback_entry = Feedback(
            id=str(uuid4()),
            message_id=feedback.message_id,
            rating=feedback.rating,
            comment=feedback.comment,
            created_at=datetime.utcnow()
        )
        db.add(feedback_entry)
        db.commit()
        
        return {"status": "success", "message": "Feedback submitted"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")


@app.get("/api/analytics", response_model=AnalyticsResponse)
async def get_analytics(db: Session = Depends(get_db)):
    """Get basic analytics (for admin dashboard)"""
    try:
        total_conversations = db.query(Conversation).count()
        total_messages = db.query(Message).count()
        
        # Average rating
        feedbacks = db.query(Feedback).all()
        avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks) if feedbacks else 0.0
        
        # Language breakdown
        lang_en = db.query(Conversation).filter(Conversation.language == 'en').count()
        lang_ar = db.query(Conversation).filter(Conversation.language == 'ar').count()
        
        return AnalyticsResponse(
            total_conversations=total_conversations,
            total_messages=total_messages,
            avg_rating=avg_rating,
            language_breakdown={"en": lang_en, "ar": lang_ar}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation history"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at).all()
    
    return {
        "conversation_id": conversation.id,
        "language": conversation.language,
        "created_at": conversation.created_at.isoformat(),
        "messages": [
            {
                "id": msg.id,
                "content": msg.content,
                "is_user": msg.is_user,
                "confidence": msg.confidence,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }


# ===== New API Contract Endpoints =====

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: Session = Depends(get_db)):
    """
    Main question endpoint with authoritative RAG flow
    """
    try:
        # 1. Detect language + jurisdiction (default DXB)
        language = request.language or detect_language(request.question)
        jurisdiction = request.jurisdictionCode or "DXB"
        
        # 2. Embed user query → retrieve top-K (K=5) from document_chunks
        rag_results = rag_engine.retrieve_context(
            query=request.question,
            language=language,
            top_k=5
        )
        
        # 3. Rerank (cosine + BM25 keywords). Require at least 2 distinct documents when available
        if len(rag_results) < 2:
            # Low confidence if insufficient sources
            confidence_level = "Low"
            context_coverage = 0.3
        elif len(rag_results) >= 3:
            confidence_level = "High"
            context_coverage = 0.9
        else:
            confidence_level = "Medium"
            context_coverage = 0.6
        
        # 4. Build context block (max ~3 chunks) with metadata
        context_chunks = rag_results[:3]
        context = "\n\n".join([
            f"[{r['source']}] {r['text']}" for r in context_chunks
        ])
        
        # 5. Generate with main prompt. If retrieval coverage < threshold or score low → low-confidence prompt
        system_prompt = SYSTEM_PROMPT_AR if language == 'ar' else SYSTEM_PROMPT_EN
        system_prompt = system_prompt.format(context=context)
        
        if context_coverage < 0.5:
            # Low confidence prompt
            if language == 'ar':
                system_prompt += "\n\n⚠️ تحذير: المعلومات المتوفرة محدودة. يُنصح بالاستشارة مع محامٍ مرخص."
            else:
                system_prompt += "\n\n⚠️ Warning: Limited information available. Consider consulting a licensed lawyer."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.question}
        ]
        
        # Call OpenAI API with fallback for testing mode
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            answer = response.choices[0].message.content
        except Exception as e:
            if "quota" in str(e).lower() or "billing" in str(e).lower() or "rate" in str(e).lower():
                # TESTING MODE: Provide response from context
                if context:
                    if language == 'ar':
                        answer = f"""🤖 **وضع الاختبار** - نظام LegalEdge AI

📋 **سؤالك**: {request.question}

📚 **المعلومات القانونية ذات الصلة من دليل الإيجار في دبي**:

{context[:800]}...

⚠️ **تنويه قانوني**: هذه معلومات عامة فقط من قانون الإيجار في دبي. للحصول على استشارة قانونية محددة لحالتك، يرجى التواصل مع محامٍ مرخص في دبي."""
                    else:
                        answer = f"""🤖 **TESTING MODE** - LegalEdge AI System

📋 **Your Question**: {request.question}

📚 **Relevant Legal Information from Dubai Tenancy Guide**:

{context[:800]}...

⚠️ **Legal Disclaimer**: This is general information only from Dubai tenancy law. For legal advice specific to your situation, please consult a licensed lawyer in Dubai."""
                else:
                    if language == 'ar':
                        answer = "عذراً، لم أجد معلومات ذات صلة في قاعدة البيانات الخاصة بنا حول هذا السؤال."
                    else:
                        answer = "Sorry, I couldn't find relevant information in our database about this question."
                confidence_level = "Low"
            else:
                raise e
        
        # 6. Always return citations; never answer without sources
        citations = []
        for result in context_chunks:
            citation = Citation(
                title=result['source'],
                article=f"Page {result.get('page', 'N/A')}",
                version_date="2024",  # Default version date
                source_url=None
            )
            citations.append(citation)
        
        return AskResponse(
            answer=answer,
            confidence=confidence_level,
            citations=citations,
            language=language,
            jurisdiction=jurisdiction
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.post("/embed", response_model=EmbedResponse)
async def embed_document(request: EmbedRequest, db: Session = Depends(get_db)):
    """
    Admin endpoint for embedding documents
    """
    try:
        document_id = str(uuid4())
        
        # Split text into chunks and embed
        chunks = rag_engine.add_document_chunks(
            source=request.document.title,
            text=request.text,
            language=request.language or 'en',
            document_id=document_id,
            meta_data={
                "source_url": request.document.source_url,
                "version_date": request.document.version_date,
                "jurisdictionCode": request.document.jurisdictionCode,
                "topic": request.topic
            }
        )
        
        return EmbedResponse(
            documentId=document_id,
            chunks=len(chunks)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error embedding document: {str(e)}")


@app.post("/feedback", response_model=FeedbackNewResponse)
async def submit_feedback_new(request: FeedbackNewRequest, db: Session = Depends(get_db)):
    """
    Submit feedback for questions/answers
    """
    try:
        # Create a message first if answerId is provided, otherwise use a generic one
        if request.answerId:
            message_id = request.answerId
        else:
            # Create a generic conversation first
            generic_conversation = Conversation(
                id=str(uuid4()),
                language="en",
                created_at=datetime.utcnow()
            )
            db.add(generic_conversation)
            db.flush()  # Get the ID without committing
            
            # Create a generic message for general feedback
            generic_message = Message(
                id=str(uuid4()),
                conversation_id=generic_conversation.id,
                content=f"General feedback: {request.question}",
                is_user=True,
                language="en",
                created_at=datetime.utcnow()
            )
            db.add(generic_message)
            db.flush()  # Get the ID without committing
            message_id = generic_message.id
        
        # Create feedback
        feedback = Feedback(
            id=str(uuid4()),
            message_id=message_id,
            rating=5 if request.helpful else 1,
            comment=f"Question: {request.question}",
            created_at=datetime.utcnow()
        )
        
        db.add(feedback)
        db.commit()
        
        return FeedbackNewResponse(ok=True)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

