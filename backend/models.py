"""
SQLAlchemy models for LegalEdge AI
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from database import Base


class Conversation(Base):
    """Conversation/Session model"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    language = Column(String(2), nullable=False)  # 'en' or 'ar'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Chat message model"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_user = Column(Boolean, nullable=False)
    language = Column(String(2), nullable=False)
    confidence = Column(Float, nullable=True)  # For assistant messages
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("Citation", back_populates="message", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="message", cascade="all, delete-orphan")


class Citation(Base):
    """Citation/Source reference model"""
    __tablename__ = "citations"
    
    id = Column(String, primary_key=True)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    source = Column(String, nullable=False)  # Document name
    page = Column(Integer, nullable=True)
    excerpt = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=False)
    
    # Relationships
    message = relationship("Message", back_populates="citations")


class Feedback(Base):
    """User feedback model"""
    __tablename__ = "feedbacks"
    
    id = Column(String, primary_key=True)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    message = relationship("Message", back_populates="feedbacks")


class Document(Base):
    """Embedded document chunks for RAG"""
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)  # PDF filename
    page = Column(Integer, nullable=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    content_ar = Column(Text, nullable=True)  # Arabic translation if available
    embedding = Column(Vector(3072), nullable=False)  # text-embedding-3-large dimension
    language = Column(String(2), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Additional metadata
    meta_data = Column(Text, nullable=True)  # JSON string for additional info

