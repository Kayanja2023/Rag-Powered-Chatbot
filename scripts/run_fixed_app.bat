@echo off
echo Starting Fixed Clickatell AI Assistant...
echo ========================================

echo Running tests first...
py test_fixed.py

if errorlevel 1 (
    echo Tests failed! Check implementation.
    pause
    exit /b 1
)

echo.
echo Tests passed! Starting application...
py -m streamlit run streamlit_app_fixed.py --theme.primaryColor "#667eea"

pause