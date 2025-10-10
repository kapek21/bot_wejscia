# Portal Bot - PowerShell Launcher
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "     PORTAL BOT - Uruchamianie     " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Przejdź do katalogu skryptu
Set-Location $PSScriptRoot

# Sprawdź Python
Write-Host "Sprawdzanie instalacji Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python zainstalowany: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ BŁĄD: Python nie jest zainstalowany!" -ForegroundColor Red
    Write-Host "Pobierz Python z https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "Naciśnij Enter aby zakończyć"
    exit 1
}

# Sprawdź zależności
Write-Host "Sprawdzanie zależności..." -ForegroundColor Yellow
$seleniumInstalled = pip show selenium 2>&1 | Select-String "Name: selenium"
if (-not $seleniumInstalled) {
    Write-Host "Instalowanie zależności..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "✓ Zależności zainstalowane" -ForegroundColor Green
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "     BOT ZOSTANIE URUCHOMIONY      " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Aby zatrzymać bota naciśnij Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "Uruchamianie..." -ForegroundColor Green
Write-Host ""

# Uruchom bota
python main_bot.py

Read-Host "Naciśnij Enter aby zakończyć"

