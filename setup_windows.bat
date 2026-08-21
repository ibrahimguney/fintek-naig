@echo off
setlocal
cd /d "%~dp0"
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo Kurulum tamamlandi. Analiz icin run_all.bat dosyasini calistirin.
pause
