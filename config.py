# Configuration file for TravelRag
# Paste your OpenAI API key here
OPENAI_API_KEY = ""

# Model settings
EMBEDDING_MODEL = "all-mpnet-base-v2"  # More accurate embedding model
CHUNK_SIZE = 500  # Number of characters per text chunk
CHUNK_OVERLAP = 50  # Overlap between chunks

# Retrieval settings
TOP_K_CHUNKS = 3  # Number of chunks to retrieve for each query
