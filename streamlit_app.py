import streamlit as st
import os
from src.core.text_processor import process_travel_documents
from src.core.vector_store import create_vector_store, SimpleVectorStore
from src.core.rag_engine import create_rag_engine

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VECTOR_BASENAME = PROJECT_ROOT / "storage" / "travel_vector_store"  # no extension

# Simple page config
st.set_page_config(page_title="TravelRag Chatbot", page_icon="✈️")

# Simple styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def setup_rag():
    """Smart RAG setup with vector store caching for faster startup."""
    
    # Check if we have data
    if not os.path.exists("travel_data"):
        st.error("ERROR: No travel_data folder found!")
        return None
    
    # Try to load existing vector store first
    if VECTOR_BASENAME.with_suffix(".faiss").exists() and VECTOR_BASENAME.with_suffix(".pkl").exists():
        st.info("Loading existing vector store...")
        try:
            vs = SimpleVectorStore()
            vs.load(str(VECTOR_BASENAME))
            st.success("SUCCESS: Vector store loaded from cache!")
            return create_rag_engine(vs)
        except Exception as e:
            st.warning(f"⚠️ Failed to load cached vector store: {str(e)}")
            st.info("Creating new vector store...")
    
    # Process documents and create new vector store
    docs = process_travel_documents()
    if not docs:
        st.error("ERROR: No documents processed!")
        return None
    
    # Create vector store
    vs = create_vector_store(docs)
    
    # Save for future use
    try:
        VECTOR_BASENAME.parent.mkdir(parents=True, exist_ok=True)
        vs.save(str(VECTOR_BASENAME))
        st.success("SUCCESS: Vector store created and saved!")
    except Exception as e:
        st.warning(f"⚠️ Could not save vector store: {str(e)}")
    
    # Create RAG engine
    try:
        rag = create_rag_engine(vs)
        return rag
    except Exception as e:
        st.error(f"ERROR: RAG Error: {str(e)}")
        return None

def main():
    st.title("✈️ TravelRag Chatbot")
    st.write("Ask me anything about travel destinations!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Setup RAG system
    rag = setup_rag()
    if not rag:
        st.stop()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a travel question..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = rag.answer_question(prompt)
                    response = result['answer']
                    
                    # Display answer first
                    st.markdown(f"**Answer:** {response}")
                    
                    # Display sources separately with full details
                    if result['sources']:
                        st.subheader("Sources")
                        st.write(f"Found {len(result['sources'])} relevant sources:")
                        
                        for i, source in enumerate(result['sources']):
                            with st.expander(f"Source {i+1}: {source['title']} (Score: {source['score']})"):
                                st.write(f"**Content:** {source['content']}")
                                if 'source_file' in source:
                                    st.caption(f"File: {source['source_file']}")
                    else:
                        st.warning("No sources found for this question.")
                    
                    # Store complete response for chat history
                    full_response = response
                    if result['sources']:
                        full_response += f"\n\nSources: {len(result['sources'])} found"
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    full_response = error_msg
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Simple sidebar info
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("This chatbot uses RAG to answer travel questions based on Wikipedia travel articles.")
        
        # Show system status
        st.header("📊 Status")
        if os.path.exists("travel_data"):
            files = [f for f in os.listdir("travel_data") if f.endswith('.txt')]
            st.success(f"SUCCESS: {len(files)} travel articles loaded")
            
            # Show loaded articles list
            st.subheader("Loaded Articles")
            for file in sorted(files):
                # Clean up filename for display
                article_name = file.replace('.txt', '').replace('_', ' ').title()
                st.write(f"• {article_name}")
        else:
            st.error("ERROR: No travel data")
        
        # Show vector store status
        if VECTOR_BASENAME.with_suffix(".faiss").exists():
            st.success("SUCCESS: Vector store cached")
        else:
            st.info("ℹ️ Vector store will be created on first use")

if __name__ == "__main__":
    main()
