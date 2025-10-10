@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════╗
echo ║           PORTAL BOT - Instalacja Zależności            ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] Sprawdzanie Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ BŁĄD: Python nie jest zainstalowany!
    echo.
    echo Pobierz Python 3.8+ z:
    echo https://www.python.org/downloads/
    echo.
    echo Zaznacz "Add Python to PATH" podczas instalacji!
    pause
    exit /b 1
) else (
    python --version
    echo ✓ Python jest zainstalowany
)

echo.
echo [2/3] Sprawdzanie pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ BŁĄD: pip nie jest zainstalowany!
    pause
    exit /b 1
) else (
    echo ✓ pip jest zainstalowany
)

echo.
echo [3/3] Instalowanie zależności...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ✗ Instalacja nie powiodła się!
    pause
    exit /b 1
) else (
    echo.
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║              ✓ INSTALACJA ZAKOŃCZONA!                   ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    echo Możesz teraz uruchomić bota:
    echo   - Kliknij na: start_bot.bat
    echo   - Lub uruchom: python main_bot.py
    echo.
    echo Aby przetestować instalację:
    echo   - Uruchom: python test_bot.py
    echo.
)

pause

