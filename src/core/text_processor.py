import os
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def chunk_by_sections(text: str, min_size: int = 100, max_size: int = 1200) -> List[str]:
    """Simple chunking based on all Wikivoyage header levels."""
    
    # Split text by all header levels (==, ===, ====)
    # This keeps the headers with their content
    # Split before any line that starts with 2 or more equals
    # Handle both cases: newline before header and header at start of text
    parts = re.split(r"(={2,3}\s*[^=]+?\s*={2,3})", text)
    chunks = []
    
    # Handle the first part (content before any headers)
    if parts[0].strip():
        chunks.append(parts[0].strip())
    
    # Process the parts to create proper chunks
    for i in range(1, len(parts), 2):  
        heading = parts[i].strip()
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        chunk = heading + "\n" + content if content else heading
        
        if len(chunk) > max_size:
            # Split into approximately equal chunks at sentence boundaries
            
            # Split into sentences (ending with . ! ?)
            sentences = re.split(r'(?<=[.!?])\s+', chunk)
            
            chunk_count = (len(chunk) + max_size - 1) // max_size  # Ceiling division
            sentences_per_chunk = len(sentences) // chunk_count
            remainder = len(sentences) % chunk_count  # Extra sentences to distribute
            
            for i in range(chunk_count):
                start_idx = i * sentences_per_chunk + min(i, remainder)
                end_idx = start_idx + sentences_per_chunk + (1 if i < remainder else 0)
                
                sub_chunk = ' '.join(sentences[start_idx:end_idx])
                
                # Only add if it's not too small
                if len(sub_chunk) >= min_size:
                    chunks.append(sub_chunk.strip())
        else:
            chunks.append(chunk)
    # Filter out chunks that are too small
    chunks = [chunk for chunk in chunks if len(chunk) >= min_size]
    
    return chunks

def process_travel_documents(data_dir: str = "travel_data", min_chunk_size: int = 100, max_chunk_size: int = 1200) -> List[Dict]:
    """Process all travel documents and split them into section-based chunks."""
    
    documents = []
    
    if not os.path.exists(data_dir):
        print(f"[ERROR] Data directory '{data_dir}' not found!")
        return documents
    
    # Process each text file
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract metadata from file content
                lines = content.split('\n')
                title = "Unknown"
                source = "Unknown"
                
                # Look for title and source in header
                for line in lines[:5]:
                    if line.startswith('Title: '):
                        title = line.replace('Title: ', '').strip()
                    elif line.startswith('Source: '):
                        source = line.replace('Source: ', '').strip()
                    elif title != "Unknown" and source != "Unknown":
                        break
                
                # Extract actual content (skip header)
                content_start = content.find('Content:')
                if content_start != -1:
                    actual_content = content[content_start + 8:].strip()
                else:
                    actual_content = content
                
                # Clean the content
                cleaned_content = clean_text(actual_content)
                
                # Split into section-based chunks
                chunks = chunk_by_sections(cleaned_content, min_chunk_size, max_chunk_size)
                
                # Create document entries
                for i, chunk in enumerate(chunks):
                    doc = {
                        'id': f"{title}_{i}",
                        'title': title,
                        'source': source,
                        'content': chunk,
                        'chunk_index': i,
                        'source_file': filename,
                        'chunk_size': len(chunk)
                    }
                    documents.append(doc)
                
                print(f"[SUCCESS] Processed {filename}: {len(chunks)} chunks (Title: {title}, Source: {source})")
                
            except Exception as e:
                print(f"[ERROR] Error processing {filename}: {str(e)}")
    
    print(f"\n[COMPLETE] Total documents processed: {len(documents)}")
    return documents

if __name__ == "__main__":
    # Test the text processing
    docs = process_travel_documents()
    if docs:
        print(f"\nSample chunk from '{docs[0]['title']}':")
        print(f"Content: {docs[0]['content'][:200]}...")
        print(f"Chunk size: {docs[0]['chunk_size']} characters")
        
        # Show chunk size distribution
        sizes = [doc['chunk_size'] for doc in docs]
        print(f"\nChunk size statistics:")
        print(f"  Average: {sum(sizes) / len(sizes):.0f} characters")
        print(f"  Min: {min(sizes)} characters")
        print(f"  Max: {max(sizes)} characters")
