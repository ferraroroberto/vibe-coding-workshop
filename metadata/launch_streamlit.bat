@echo off
REM ==========================================================
REM  Survey Data Dashboard - Windows Launcher
REM ==========================================================
REM  Double-click this file to start the application.
REM  It locates a repo-local virtual environment (.venv) and
REM  launches the Streamlit app.
REM ==========================================================

title Survey Data Dashboard

REM -- Resolve the directory where this .bat file lives ------
cd /d "%~dp0"

REM -- Locate virtual environment -----------------------------
set "VENV_DIR="
if exist ".venv\Scripts\activate.bat" set "VENV_DIR=%cd%\.venv"
if not defined VENV_DIR if exist "..\.venv\Scripts\activate.bat" set "VENV_DIR=%cd%\..\.venv"

REM -- Check that .venv exists --------------------------------
if not defined VENV_DIR (
    echo.
    echo  [ERROR] Virtual environment not found.
    echo  Please create it first:
    echo.
    echo      cd /d "%cd%\.."
    echo      python -m venv .venv
    echo      .venv\Scripts\activate
    echo      pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM -- Activate the virtual environment -----------------------
call "%VENV_DIR%\Scripts\activate.bat"

REM -- Launch Streamlit ---------------------------------------
streamlit run "streamlit_app.py" --browser.gatherUsageStats=false

REM -- Keep the window open if Streamlit exits ----------------
pause
