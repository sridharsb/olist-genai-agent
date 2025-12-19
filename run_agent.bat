@echo off
REM Run script for Olist GenAI Agent
echo Starting Olist GenAI Agent...
echo.

REM Activate virtual environment and run streamlit
call venv\Scripts\activate.bat
streamlit run streamlit_app.py

pause

