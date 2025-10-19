"""
Admin Script: Embed PDFs into Vector Database
Usage: python admin_embed_pdfs.py --pdf path/to/document.pdf --name "Document Name"
"""
import argparse
import os
from pathlib import Path
from typing import List, Dict
import PyPDF2
from dotenv import load_dotenv

from rag_engine import RAGEngine
from database import init_db

load_dotenv()


class PDFEmbedder:
    """Handles PDF processing and embedding"""
    
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.chunk_size = 1000  # Characters per chunk
        self.chunk_overlap = 200  # Overlap between chunks
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Extract text from PDF with page numbers
        
        Returns:
            List of dicts with keys: page, text
        """
        pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    text = page.extract_text()
                    if text.strip():
                        pages.append({
                            'page': page_num,
                            'text': text
                        })
            
            print(f"✓ Extracted {len(pages)} pages from PDF")
            return pages
            
        except Exception as e:
            print(f"✗ Error extracting PDF: {e}")
            return []
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size * 0.5:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return chunks
    
    def embed_pdf(
        self, 
        pdf_path: str, 
        document_name: str,
        language: str = 'en'
    ):
        """
        Process and embed a PDF into the vector database
        """
        print(f"\n📄 Processing: {document_name}")
        print(f"   File: {pdf_path}")
        print(f"   Language: {language}")
        
        # Extract text
        pages = self.extract_text_from_pdf(pdf_path)
        
        if not pages:
            print("✗ No text extracted. Aborting.")
            return
        
        # Process each page
        total_chunks = 0
        
        for page_data in pages:
            page_num = page_data['page']
            page_text = page_data['text']
            
            # Chunk the page text
            chunks = self.chunk_text(page_text)
            
            # Embed each chunk
            for chunk_idx, chunk in enumerate(chunks):
                if len(chunk.strip()) < 50:  # Skip very small chunks
                    continue
                
                try:
                    doc_id = self.rag_engine.add_document_chunk(
                        source=document_name,
                        page=page_num,
                        chunk_index=chunk_idx,
                        content=chunk,
                        language=language
                    )
                    total_chunks += 1
                    print(f"   ✓ Embedded: Page {page_num}, Chunk {chunk_idx} (ID: {doc_id[:8]}...)")
                    
                except Exception as e:
                    print(f"   ✗ Error embedding chunk: {e}")
        
        print(f"\n✓ Successfully embedded {total_chunks} chunks from {document_name}")


def main():
    """Main function for CLI"""
    parser = argparse.ArgumentParser(
        description="Embed PDF documents into LegalEdge AI vector database"
    )
    parser.add_argument(
        '--pdf',
        type=str,
        required=True,
        help='Path to PDF file'
    )
    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='Document name (e.g., "Dubai Tenancy Law No. 26 of 2007")'
    )
    parser.add_argument(
        '--language',
        type=str,
        default='en',
        choices=['en', 'ar'],
        help='Document language (en or ar)'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database before embedding'
    )
    
    args = parser.parse_args()
    
    # Validate PDF exists
    if not os.path.exists(args.pdf):
        print(f"✗ Error: PDF file not found: {args.pdf}")
        return
    
    # Initialize database if requested
    if args.init_db:
        print("Initializing database...")
        init_db()
        print("✓ Database initialized")
    
    # Embed PDF
    embedder = PDFEmbedder()
    embedder.embed_pdf(
        pdf_path=args.pdf,
        document_name=args.name,
        language=args.language
    )
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()

