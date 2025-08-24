import streamlit as st
import os
from text_processor import process_travel_documents
from vector_store import create_vector_store, SimpleVectorStore
from rag_engine import create_rag_engine
import config

# Page configuration
st.set_page_config(
    page_title="TravelRag - Your AI Travel Assistant",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .answer-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag_system():
    """Load the RAG system with caching."""
    
    # Check if vector store exists
    if os.path.exists("travel_vector_store.faiss") and os.path.exists("travel_vector_store.pkl"):
        st.info("🔄 Loading existing vector store...")
        vector_store = SimpleVectorStore(config.EMBEDDING_MODEL)
        vector_store.load("travel_vector_store")
        return create_rag_engine(vector_store)
    
    # Check if we have travel data
    if not os.path.exists("travel_data"):
        st.error("❌ No travel data found! Please run data_collector.py first.")
        return None
    
    # Process documents and create vector store
    st.info("🔄 Processing travel documents and creating vector store...")
    documents = process_travel_documents()
    
    if not documents:
        st.error("❌ No documents processed! Check your data files.")
        return None
    
    # Create vector store
    vector_store = create_vector_store(documents, config.EMBEDDING_MODEL)
    
    # Save for future use
    vector_store.save("travel_vector_store")
    
    return create_rag_engine(vector_store)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">✈️ TravelRag</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI Travel Assistant powered by RAG")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Check API key
        if config.OPENAI_API_KEY == "your-api-key-here":
            st.error("⚠️ Please set your OpenAI API key in config.py")
            st.stop()
        else:
            st.success("✅ OpenAI API key configured")
        
        st.markdown("---")
        st.markdown("**About TravelRag**")
        st.markdown("""
        This system uses:
        - **RAG** (Retrieval-Augmented Generation)
        - **Wikipedia travel articles** as knowledge base
        - **OpenAI GPT** for answer generation
        
        Ask any travel question and get informed answers with sources!
        """)
    
    # Main content
    tab1, tab2 = st.tabs(["🤖 Ask Questions", "📊 System Status"])
    
    with tab1:
        st.header("Ask Your Travel Question")
        
        # Load RAG system
        rag_system = load_rag_system()
        
        if rag_system is None:
            st.error("❌ Failed to load RAG system. Please check the console for errors.")
            return
        
        # Question input
        question = st.text_input(
            "What would you like to know about travel?",
            placeholder="e.g., What are the best places to visit in Paris?",
            help="Ask any travel-related question and get an AI-generated answer based on our travel knowledge base."
        )
        
        # Submit button
        if st.button("🚀 Get Answer", type="primary"):
            if question.strip():
                with st.spinner("🔍 Searching for relevant information..."):
                    # Get answer
                    result = rag_system.answer_question(question)
                    
                    # Display answer
                    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                    st.markdown(f"**Answer:** {result['answer']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display sources
                    if result['sources']:
                        st.subheader("📚 Sources")
                        st.markdown("Here are the sources used to generate this answer:")
                        
                        for i, source in enumerate(result['sources']):
                            with st.expander(f"Source {i+1}: {source['title']} (Relevance: {source['score']})"):
                                st.markdown(f"**Content:** {source['content']}")
                                st.caption(f"File: {source['source_file']}")
                    else:
                        st.warning("No sources found for this question.")
            else:
                st.warning("Please enter a question!")
    
    with tab2:
        st.header("System Status")
        
        # Check data directory
        if os.path.exists("travel_data"):
            files = os.listdir("travel_data")
            st.success(f"✅ Travel data directory found with {len(files)} files")
            
            if files:
                st.subheader("📁 Available Travel Articles")
                for file in files:
                    if file.endswith('.txt'):
                        st.write(f"• {file.replace('.txt', '').replace('_', ' ')}")
        else:
            st.error("❌ Travel data directory not found")
        
        # Check vector store
        if os.path.exists("travel_vector_store.faiss"):
            st.success("✅ Vector store index found")
        else:
            st.warning("⚠️ Vector store index not found - will be created on first use")
        
        # Check config
        st.subheader("⚙️ Configuration")
        st.write(f"**Embedding Model:** {config.EMBEDDING_MODEL}")
        st.write(f"**Chunk Size:** {config.CHUNK_SIZE} characters")
        st.write(f"**Top K Chunks:** {config.TOP_K_CHUNKS}")

if __name__ == "__main__":
    main()
