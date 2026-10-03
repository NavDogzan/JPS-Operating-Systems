@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
	echo Project virtual environment not found at ".venv\Scripts\python.exe".
	pause
	exit /b 1
)

".venv\Scripts\python.exe" "JPS Operating System.py"
endlocal
