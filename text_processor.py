import os
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    
    # If text is shorter than chunk size, return as single chunk
    if len(text) <= chunk_size:
        return [text]
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings within the last 100 characters
            search_start = max(start + chunk_size - 100, start)
            sentence_end = text.rfind('.', search_start, end)
            if sentence_end > start + chunk_size // 2:  # Only break if we find a reasonable sentence end
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        # Move start position, accounting for overlap
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def process_travel_documents(data_dir: str = "travel_data", chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """Process all travel documents and split them into chunks."""
    
    documents = []
    
    if not os.path.exists(data_dir):
        print(f"❌ Data directory '{data_dir}' not found!")
        return documents
    
    # Process each text file
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract the actual title from the file content, not the filename
                lines = content.split('\n')
                title = "Unknown"
                source = "Unknown"
                
                # Look for the title in the first few lines
                for line in lines[:5]:
                    if line.startswith('Title: '):
                        title = line.replace('Title: ', '').strip()
                    elif line.startswith('Source: '):
                        source = line.replace('Source: ', '').strip()
                
                # Clean the content (remove the header lines)
                content_start = content.find('Content:')
                if content_start != -1:
                    actual_content = content[content_start + 8:].strip()  # Skip "Content:" and get the rest
                else:
                    actual_content = content
                
                # Clean the content
                cleaned_content = clean_text(actual_content)
                
                # Split into chunks
                chunks = split_into_chunks(cleaned_content, chunk_size, overlap)
                
                # Create document entries
                for i, chunk in enumerate(chunks):
                    doc = {
                        'id': f"{title}_{i}",
                        'title': title,
                        'source': source,
                        'content': chunk,
                        'chunk_index': i,
                        'source_file': filename
                    }
                    documents.append(doc)
                
                print(f"✅ Processed {filename}: {len(chunks)} chunks (Title: {title}, Source: {source})")
                
            except Exception as e:
                print(f"❌ Error processing {filename}: {str(e)}")
    
    print(f"\n✨ Total documents processed: {len(documents)}")
    return documents

if __name__ == "__main__":
    # Test the text processing
    docs = process_travel_documents()
    if docs:
        print(f"\nSample chunk from '{docs[0]['title']}':")
        print(f"Content: {docs[0]['content'][:200]}...")
