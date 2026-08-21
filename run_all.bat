@echo off
setlocal
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python run_all.py
if errorlevel 1 (
  echo.
  echo HATA: Analizlerden biri tamamlanamadi.
  pause
  exit /b 1
)
echo.
echo Analizler tamamlandi.
pause
