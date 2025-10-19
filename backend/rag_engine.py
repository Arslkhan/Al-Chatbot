"""
RAG (Retrieval-Augmented Generation) Engine
Handles document retrieval using pgvector
"""
import os
from typing import List, Dict, Any
import openai
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models import Document

load_dotenv()


class RAGEngine:
    """RAG engine for retrieving relevant legal documents"""
    
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/legaledge"
        )
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI's text-embedding-3-large"""
        response = openai.Embedding.create(
            model="text-embedding-3-large",
            input=text
        )
        return response['data'][0]['embedding']
    
    def retrieve_context(
        self, 
        query: str, 
        language: str = 'en',
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve top-k most relevant document chunks
        
        Args:
            query: User's question
            language: 'en' or 'ar'
            top_k: Number of results to return
            
        Returns:
            List of dicts with keys: source, page, text, score
        """
        try:
            # Try to generate embedding for query
            try:
                query_embedding = self.get_embedding(query)
                use_vector_search = True
            except Exception as embed_error:
                # If embedding fails (quota issue), fall back to keyword search
                print(f"Embedding failed, using keyword search: {embed_error}")
                use_vector_search = False
            
            # Use pgvector for similarity search
            session = self.SessionLocal()
            
            if use_vector_search:
                # Convert embedding to PostgreSQL vector format
                embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
                
                # Query using cosine similarity
                query_sql = text("""
                    SELECT 
                        id,
                        source,
                        page,
                        content,
                        content_ar,
                        language,
                        1 - (embedding <=> :query_embedding::vector) as similarity
                    FROM documents
                    WHERE language = :language OR language = 'both'
                    ORDER BY embedding <=> :query_embedding::vector
                    LIMIT :top_k
                """)
                
                results = session.execute(
                    query_sql,
                    {
                        "query_embedding": embedding_str,
                        "language": language,
                        "top_k": top_k
                    }
                ).fetchall()
            else:
                # TESTING MODE: Fallback to keyword-based search
                # Extract keywords from query (simple approach)
                keywords = query.lower().split()
                # Filter out common words
                stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'can', 'how', 'when', 'where', 'who', 'why'}
                keywords = [k for k in keywords if k not in stop_words and len(k) > 2]
                
                if keywords:
                    # Use simple LIKE search with main keyword
                    main_keyword = keywords[0]
                    search_pattern = f"%{main_keyword}%"
                    
                    query_sql = text("""
                        SELECT 
                            id,
                            source,
                            page,
                            content,
                            content_ar,
                            language,
                            0.7 as similarity
                        FROM documents
                        WHERE LOWER(content) LIKE LOWER(:search_pattern) 
                        AND (language = :language OR language = 'both')
                        LIMIT :top_k
                    """)
                    
                    results = session.execute(
                        query_sql,
                        {
                            "search_pattern": search_pattern,
                            "language": language,
                            "top_k": top_k
                        }
                    ).fetchall()
                    
                    # If no results with first keyword, try returning any documents
                    if not results:
                        query_sql = text("""
                            SELECT 
                                id,
                                source,
                                page,
                                content,
                                content_ar,
                                language,
                                0.5 as similarity
                            FROM documents
                            WHERE language = :language OR language = 'both'
                            ORDER BY created_at DESC
                            LIMIT :top_k
                        """)
                        
                        results = session.execute(
                            query_sql,
                            {
                                "language": language,
                                "top_k": top_k
                            }
                        ).fetchall()
                else:
                    # No keywords, return recent documents
                    query_sql = text("""
                        SELECT 
                            id,
                            source,
                            page,
                            content,
                            content_ar,
                            language,
                            0.5 as similarity
                        FROM documents
                        WHERE language = :language OR language = 'both'
                        ORDER BY created_at DESC
                        LIMIT :top_k
                    """)
                    
                    results = session.execute(
                        query_sql,
                        {
                            "language": language,
                            "top_k": top_k
                        }
                    ).fetchall()
            
            session.close()
            
            # Format results
            formatted_results = []
            for row in results:
                content = row.content_ar if (language == 'ar' and row.content_ar) else row.content
                formatted_results.append({
                    "id": row.id,
                    "source": row.source,
                    "page": row.page,
                    "text": content,
                    "score": float(row.similarity)
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def add_document_chunk(
        self,
        source: str,
        page: int,
        chunk_index: int,
        content: str,
        content_ar: str = None,
        language: str = 'en',
        meta_data: str = None
    ) -> str:
        """
        Add a document chunk to the vector database
        
        Returns:
            Document ID
        """
        from uuid import uuid4
        from datetime import datetime
        
        try:
            # Generate embedding
            embedding = self.get_embedding(content)
            
            # Create document entry
            session = self.SessionLocal()
            doc = Document(
                id=str(uuid4()),
                source=source,
                page=page,
                chunk_index=chunk_index,
                content=content,
                content_ar=content_ar,
                embedding=embedding,
                language=language,
                meta_data=meta_data,
                created_at=datetime.utcnow()
            )
            
            session.add(doc)
            session.commit()
            doc_id = doc.id
            session.close()
            
            return doc_id
            
        except Exception as e:
            print(f"Error adding document chunk: {e}")
            session.rollback()
            session.close()
            raise
    
    def add_document_chunks(
        self,
        source: str,
        text: str,
        language: str = 'en',
        document_id: str = None,
        meta_data: dict = None
    ) -> List[str]:
        """
        Add document chunks from text (new API method)
        
        Args:
            source: Document title
            text: Full document text
            language: Language code
            document_id: Optional document ID
            meta_data: Optional metadata dict
            
        Returns:
            List of chunk IDs
        """
        import json
        from uuid import uuid4
        from datetime import datetime
        
        try:
            # Split text into chunks (simple approach)
            chunk_size = 500  # characters
            chunks = []
            
            for i in range(0, len(text), chunk_size):
                chunk_text = text[i:i + chunk_size]
                if chunk_text.strip():  # Skip empty chunks
                    chunks.append(chunk_text.strip())
            
            chunk_ids = []
            session = self.SessionLocal()
            
            for i, chunk_content in enumerate(chunks):
                try:
                    # Generate embedding
                    embedding = self.get_embedding(chunk_content)
                except Exception as e:
                    print(f"Error generating embedding for chunk {i}: {e}")
                    # Use zero vector as fallback
                    embedding = [0.0] * 3072
                
                # Create document entry
                doc = Document(
                    id=str(uuid4()),
                    source=source,
                    page=i + 1,  # Use chunk index as page
                    chunk_index=i,
                    content=chunk_content,
                    content_ar=None,  # Could be translated later
                    embedding=embedding,
                    language=language,
                    meta_data=json.dumps(meta_data) if meta_data else None,
                    created_at=datetime.utcnow()
                )
                
                session.add(doc)
                chunk_ids.append(doc.id)
            
            session.commit()
            session.close()
            
            return chunk_ids
            
        except Exception as e:
            print(f"Error adding document chunks: {e}")
            if 'session' in locals():
                session.rollback()
                session.close()
            raise

