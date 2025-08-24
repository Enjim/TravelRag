@echo off
echo 🚀 TravelRag Windows Installation Script
echo ========================================

echo.
echo 📦 Installing Python dependencies...
echo.

REM Install everything except faiss-cpu first
pip install sentence-transformers==2.2.2
pip install openai==1.3.0
pip install streamlit==1.28.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install lxml==4.9.3

echo.
echo 🔧 Installing FAISS for Windows...
echo.

REM Try to install faiss-cpu with pre-built wheels
pip install faiss-cpu==1.7.4 --only-binary=all

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  FAISS installation failed. Trying alternative approach...
    echo.
    
    REM Try installing from conda-forge if available
    pip install faiss-cpu --no-deps --force-reinstall --index-url https://pypi.org/simple/
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ FAISS installation still failed. 
        echo.
        echo 💡 Alternative solutions:
        echo    1. Install Anaconda/Miniconda and run: conda install -c conda-forge faiss-cpu
        echo    2. Use the alternative vector store option (see README)
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ All dependencies installed successfully!
echo.
echo 🚀 Next steps:
echo    1. Edit config.py with your OpenAI API key
echo    2. Run: python data_collector.py
echo    3. Run: streamlit run streamlit_app.py
echo.
pause
