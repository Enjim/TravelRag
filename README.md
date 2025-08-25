# TravelRag - Simple Travel Information RAG System

A clean, simple Retrieval-Augmented Generation (RAG) system that answers travel questions using Wikipedia travel articles and OpenAI's GPT API.

## What It Does

- **Takes travel questions** from users
- **Searches through travel articles** to find relevant information
- **Generates intelligent answers** using OpenAI's GPT
- **Provides source citations** so you know where information comes from
- **Simple web interface** built with Streamlit

## Quick Setup (Windows & Mac)

### 1. Install Dependencies
```bash
python setup.py
```

This will:
- Check Python version (3.8+ required)
- Install all required packages
- Create config.py template
- Download sample travel data

### 2. Add Your OpenAI API Key
Edit `config.py` and replace `"your-api-key-here"` with your actual OpenAI API key.

### 3. Run the App
```bash
streamlit run streamlit_app.py
```

## Testing

Test the system step by step:
```bash
python test.py
```

## Project Structure

```
TravelRag/
├── setup.py              # Cross-platform setup script
├── requirements.txt      # Single requirements file
├── config.py            # API configuration
├── text_processor.py    # Document processing
├── vector_store.py      # Vector storage (scikit-learn based)
├── rag_engine.py        # RAG logic
├── data_collector.py    # Download travel articles
├── streamlit_app.py     # Web interface
├── test.py              # Test script
└── travel_data/         # Travel articles (created after setup)
```

## Dependencies

- **sentence-transformers**: Text embeddings
- **scikit-learn**: Vector similarity search
- **openai**: GPT API access
- **streamlit**: Web interface
- **wikipediaapi**: Travel article downloads

## Why This Approach?

- **No FAISS**: Avoids compatibility issues with Python 3.13+ and Mac
- **scikit-learn**: Works everywhere, reliable, well-maintained
- **Single setup script**: Works on Windows and Mac
- **Minimal dependencies**: Faster installation, fewer conflicts

## Troubleshooting

### Python Version Issues
- Requires Python 3.8 - 3.12
- Python 3.13+ has compatibility issues with some packages

### Installation Issues
- Try: `pip install --upgrade pip`
- Then: `pip install -r requirements.txt`

### API Key Issues
- Make sure you have an OpenAI API key
- Edit `config.py` and add your key

## License

MIT License - feel free to use and modify!
