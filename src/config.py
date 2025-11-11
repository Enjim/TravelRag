# # Configuration file for TravelRag


from pydantic import BaseModel, Field
from pathlib import Path
import json

class Config(BaseModel):
    openai_api_key: str = Field(..., description="Your OpenAI API key")
    embedding_model: str = Field("all-mpnet-base-v2", description="Embedding model to use")
    chunk_size: int = Field(500, description="Number of characters per text chunk")
    chunk_overlap: int = Field(50, description="Overlap between chunks")
    top_k_chunks: int = Field(3, description="Number of chunks to retrieve for each query")

    @classmethod
    def load_from_file(cls, path: str = "config.json"):
        """Load config from JSON file."""
        config_path = Path(__file__).parent.parent / path
        with open(config_path) as f:
            data = json.load(f)
        return cls(**data)  # Pydantic validates here!

_config = Config.load_from_file()

OPENAI_API_KEY = _config.openai_api_key
EMBEDDING_MODEL = _config.embedding_model
CHUNK_SIZE = _config.chunk_size
CHUNK_OVERLAP = _config.chunk_overlap
TOP_K_CHUNKS = _config.top_k_chunks






