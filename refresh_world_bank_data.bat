@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PYTHON=.venv\Scripts\python.exe"
) else (
  set "PYTHON=python"
)

echo Refreshing World Bank WDI and WGI 2021 snapshots...
%PYTHON% analysis\08_fetch_wdi_wgi.py --force
if errorlevel 1 (
  echo.
  echo World Bank data refresh FAILED.
  pause
  exit /b 1
)

echo.
echo WDI and WGI snapshots refreshed successfully.
pause
