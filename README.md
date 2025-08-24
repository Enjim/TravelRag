# ✈️ TravelRag - AI Travel Assistant

A simple but powerful Retrieval-Augmented Generation (RAG) system that answers travel questions using Wikipedia travel articles and OpenAI's GPT API.

## 🎯 What It Does

- **Takes travel questions** from users
- **Retrieves relevant information** from a curated travel knowledge base
- **Generates intelligent answers** using OpenAI's GPT models
- **Shows sources** so you know where the information comes from
- **Simple web interface** built with Streamlit

## 🏗️ Architecture

```
User Question → Vector Search → Retrieve Relevant Chunks → GPT API → Answer + Sources
```

1. **Data Collection**: Wikipedia travel articles downloaded automatically
2. **Text Processing**: Documents split into searchable chunks
3. **Vector Storage**: FAISS index for fast similarity search
4. **Retrieval**: Find most relevant document chunks
5. **Generation**: OpenAI GPT creates answers from retrieved context
6. **Interface**: Clean Streamlit web app

## 🚀 Quick Start

### 1. Install Dependencies

**For Windows users (recommended):**
```bash
# Option 1: Use the Windows batch file
install_windows.bat

# Option 2: Use alternative requirements (if FAISS fails)
pip install -r requirements_alternative.txt
```

**For Mac/Linux users:**
```bash
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key

Edit `config.py` and replace `"your-api-key-here"` with your actual OpenAI API key:

```python
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

### 3. Download Travel Data

```bash
python data_collector.py
```

This will download travel articles from Wikipedia and save them in a `travel_data/` folder.

### 4. Run the Web App

```bash
streamlit run streamlit_app.py
```

Open your browser to the URL shown (usually `http://localhost:8501`)

## 📁 Project Structure

```
TravelRag/
├── config.py              # Configuration settings
├── data_collector.py      # Downloads Wikipedia travel articles
├── text_processor.py      # Splits documents into chunks
├── vector_store.py        # FAISS vector database
├── rag_engine.py          # Main RAG logic
├── streamlit_app.py       # Web interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 How It Works

### Data Preparation
- **`data_collector.py`**: Downloads travel articles from Wikipedia
- **`text_processor.py`**: Cleans text and splits into 500-character chunks with 50-character overlap

### Vector Search
- **`vector_store.py`**: Uses sentence-transformers to create embeddings
- **Model**: `all-mpnet-base-v2` (more accurate than smaller models)
- **Storage**: FAISS index for fast similarity search

### RAG Engine
- **`rag_engine.py`**: Combines retrieval with GPT generation
- **Retrieval**: Finds top 3 most relevant document chunks
- **Generation**: Sends chunks + question to OpenAI GPT-3.5-turbo

### Web Interface
- **`streamlit_app.py`**: Clean, responsive web app
- **Features**: Question input, answer display, source citations, system status

## 🎛️ Configuration

Edit `config.py` to customize:

```python
OPENAI_API_KEY = "your-key-here"
EMBEDDING_MODEL = "all-mpnet-base-v2"  # More accurate model
CHUNK_SIZE = 500                        # Characters per chunk
CHUNK_OVERLAP = 50                      # Overlap between chunks
TOP_K_CHUNKS = 3                        # Number of chunks to retrieve
```

## 🔄 Switching Between Regional and General

**Easy!** Just change the articles in `data_collector.py`:

```python
# For general travel (current)
articles = ["Travel", "Tourism", "Paris", "Tokyo", "New_York_City", ...]

# For regional focus (e.g., Europe)
articles = ["Paris", "Rome", "Barcelona", "Amsterdam", "European_travel", ...]

# For city-specific (e.g., Paris only)
articles = ["Paris", "Paris_attractions", "Paris_culture", "Paris_food", ...]
```

## 🧪 Testing Individual Components

Test each part separately:

```bash
# Test data collection
python data_collector.py

# Test text processing
python text_processor.py

# Test vector store
python vector_store.py

# Test RAG engine
python rag_engine.py
```

## 💡 Example Questions

Try asking:
- "What are the best places to visit in Paris?"
- "How should I plan a solo trip?"
- "What are some travel tips for beginners?"
- "What should I know about backpacking?"
- "How do I stay safe while traveling?"

## 🚨 Troubleshooting

### Common Issues

1. **"No travel data found"**
   - Run `python data_collector.py` first

2. **"OpenAI API key not configured"**
   - Edit `config.py` and add your API key

3. **"Module not found"**
   - Install dependencies: `pip install -r requirements.txt`

4. **FAISS installation fails on Windows**
   - Use `install_windows.bat` for automatic installation
   - Or use `pip install -r requirements_alternative.txt` for scikit-learn alternative
   - Install Anaconda and run: `conda install -c conda-forge faiss-cpu`

5. **Slow first run**
   - First time creates embeddings (can take a few minutes)
   - Subsequent runs load from disk

### Performance Tips

- **Smaller chunks** = faster retrieval, less context
- **Larger chunks** = more context, slower retrieval
- **Fewer chunks** = faster, less comprehensive
- **More chunks** = comprehensive, slower

## 🔮 Future Enhancements

Easy to add:
- **More data sources** (travel blogs, guidebooks)
- **Different embedding models** (switch in config)
- **Caching** for faster responses
- **User feedback** collection
- **Export answers** to PDF/email

## 📚 Dependencies

- **sentence-transformers**: Text embeddings
- **faiss-cpu**: Vector similarity search
- **openai**: GPT API integration
- **streamlit**: Web interface
- **requests**: HTTP requests
- **beautifulsoup4**: Web scraping (if needed)

## 🤝 Contributing

This is designed to be simple and educational. Feel free to:
- Add more travel articles
- Experiment with different models
- Improve the UI
- Add new features

## 📄 License

MIT License - feel free to use and modify!

---

**Happy Traveling! ✈️🌍**
