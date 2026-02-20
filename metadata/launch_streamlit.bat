@echo off
cd /d "%~dp0"
"C:\Mis Datos en Local\python\workshop\.venv\Scripts\python.exe" -m streamlit run "streamlit_app.py" --browser.gatherUsageStats=false
pause