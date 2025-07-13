@echo off
echo Starting Clickatell AI Assistant...
echo ================================

echo Checking if Streamlit is installed...
py -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing Streamlit...
    pip install streamlit
)

echo Launching application...
py -m streamlit run streamlit_app.py --theme.primaryColor "#667eea"

pause