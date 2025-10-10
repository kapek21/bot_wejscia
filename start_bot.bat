@echo off
chcp 65001 >nul
echo ====================================
echo      PORTAL BOT - Uruchamianie
echo ====================================
echo.

cd /d "%~dp0"

echo Sprawdzanie instalacji Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo BŁĄD: Python nie jest zainstalowany!
    echo Pobierz Python z https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Sprawdzanie zależności...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Instalowanie zależności...
    pip install -r requirements.txt
)

echo.
echo ====================================
echo      BOT ZOSTANIE URUCHOMIONY
echo ====================================
echo Aby zatrzymać bota naciśnij Ctrl+C
echo.
echo Uruchamianie...
echo.

python main_bot.py

pause

