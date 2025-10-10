# Portal Bot - Zaawansowany Generator Ruchu

Bot do automatycznego generowania ruchu na portalach z zaawansowanymi fingerprintami i realistycznym zachowaniem użytkownika.

## 🎯 Funkcje

### 🔒 Proxy iproxy.online (KRYTYCZNE!)
- **Obowiązkowe proxy**: Bot nie może działać bez proxy
- **Automatyczna zmiana IP**: Po każdej sesji (16 portali)
- **60 sekund przerwy**: Między sesjami dla pewności zmiany IP
- **Monitoring IP**: Sprawdzanie aktualnego IP przez proxy
- **Test przy starcie**: Automatyczny test proxy przed uruchomieniem

### Zaawansowane Fingerprinting
- **User Agent**: Losowy, realistyczny User Agent (Chrome)
- **Rozdzielczość ekranu**: Popularne rozdzielczości (1920x1080, 1366x768, itp.)
- **WebGL**: Realistic vendor i renderer (Intel, NVIDIA, AMD)
- **Canvas & Audio fingerprints**: Unikalne dla każdej sesji
- **Hardware Concurrency**: Liczba rdzeni CPU (4, 6, 8, 12, 16)
- **Device Memory**: Pamięć RAM (4, 8, 16, 32 GB)
- **Język i strefa czasowa**: Polski (Europe/Warsaw)
- **Cookies**: Realistyczne cookies (Google Analytics, session, consent)

### Realistyczne Zachowanie
- **Ludzkie scrollowanie**: Płynne przewijanie z losowymi pauzami i cofaniem
- **Randomowe czasy**: Strona główna 12-18s, artykuł 14-20s
- **Direct traffic**: Ruch wygląda jak bezpośrednie wejścia
- **Imitacja użytkownika**: Easing scrolling, losowe przerwy, naturalne ruchy

### 16 Równoległych Przeglądarek
- **Jednoczesne sesje**: Wszystkie 16 portali odwiedzane równolegle
- **Wspólny fingerprint**: Jedna sesja = jeden fingerprint dla wszystkich portali
- **Chrome Headless**: Niewidoczne przeglądarki, minimalne zużycie zasobów

### System Monitorowania
- **Licznik sesji**: Udane i nieudane sesje
- **Licznik wejść**: Suma wszystkich odwiedzonych stron
- **Aktualny IP**: Automatyczne sprawdzanie IP
- **Czas działania**: Uptime bota
- **Wykrywanie zawieszenia**: Auto-restart po 60s bezczynności
- **Statystyki w czasie rzeczywistym**: Co 30 sekund
- **Persistent storage**: Statystyki zapisywane do pliku JSON

### Analytics Tracking
- **Pełne odtworzenie**: Kod analytics jest w pełni wykonywany
- **Direct traffic**: Ruch klasyfikowany jako bezpośrednie wejścia
- **Session tracking**: Realistyczne sesje z cookies

## 📋 Wymagania

- **Python 3.8+**
- **Google Chrome** (zainstalowany w systemie)
- **System operacyjny**: Windows 10/11, Linux, macOS
- **Proxy iproxy.online** (skonfigurowane, dane w `proxy_manager.py`)

## 🚀 Instalacja

### Krok 1: Sklonuj lub pobierz repozytorium

```bash
git clone <repository>
cd portale_bot
```

### Krok 2: Zainstaluj zależności

**Windows (PowerShell):**
```powershell
pip install -r requirements.txt
```

**Linux/macOS:**
```bash
pip3 install -r requirements.txt
```

### Krok 3: Test proxy (WAŻNE!)

```bash
python test_proxy.py
```

Ten test sprawdzi czy proxy działa poprawnie. **Bez działającego proxy bot się nie uruchomi!**

### Krok 4: Przygotuj plik portale.xlsx

Upewnij się że plik `portale.xlsx` jest w katalogu głównym projektu (`E:\gminy2\portale.xlsx`).

Struktura pliku:
- **Kolumna A**: Domena portalu (np. `newszachodniopomorskie.pl`)
- **Kolumna B**: Województwo (np. `zachodniopomorskie`)

## 💻 Uruchomienie

### Windows

**Opcja 1: Batch Script**
```batch
start_bot.bat
```

**Opcja 2: PowerShell**
```powershell
.\start_bot.ps1
```

**Opcja 3: Bezpośrednio Python**
```bash
python main_bot.py
```

### Linux/macOS

```bash
python3 main_bot.py
```

## ⚙️ Jak to działa

### Przebieg jednej sesji:

1. **Generowanie fingerprinta** - Bot generuje jeden zestaw fingerprintów dla całej sesji
2. **Uruchomienie 16 przeglądarek** - Wszystkie portale odwiedzane równolegle (przez proxy!)
3. **Dla każdego portalu**:
   - Wejście na stronę główną
   - Scrollowanie przez 12-18 sekund
   - Wejście w losowy artykuł
   - Scrollowanie przez 14-20 sekund
   - Zamknięcie przeglądarki
4. **Zmiana IP** - Automatyczna zmiana IP przez API iproxy.online
5. **Pauza 60 sekund** - Aby mieć pewność że IP się zmieniło
6. **Powtórzenie** - Nowa sesja z nowym fingerprintem i IP

### Monitoring:

Bot wyświetla statystyki co 30 sekund:
```
============================================================
                    STATYSTYKI BOTA
============================================================
IP: 123.45.67.89
Uruchomiony: 2025-10-10 12:00:00
Czas działania: 1:23:45
Ostatnia aktywność: 2.3s temu
------------------------------------------------------------
Sesje zakończone sukcesem: 42
Sesje nieudane: 1
Wszystkie sesje: 43
Odwiedzone strony: 1344
============================================================
```

### Auto-restart:

Jeśli bot zawiesie się na dłużej niż 60 sekund:
- Automatyczne wykrycie zawieszenia
- Zamknięcie wszystkich przeglądarek
- Reset sesji
- Kontynuacja z zachowaniem liczników

## 📊 Logi

Logi są zapisywane w katalogu `logs/`:
- `portal_bot.log` - Główny log bota
- Zawiera informacje o każdej sesji, błędach, fingerprintach

## 🛑 Zatrzymanie

Aby zatrzymać bota:
1. Naciśnij **Ctrl+C** w konsoli
2. Bot dokończy aktualną sesję i się zamknie
3. Statystyki zostaną zapisane

## 📁 Struktura Projektu

```
portale_bot/
├── main_bot.py              # Główny bot
├── fingerprint_generator.py # Generator fingerprintów
├── browser_controller.py    # Kontroler przeglądarki
├── monitoring.py            # System monitorowania
├── requirements.txt         # Zależności Python
├── start_bot.bat           # Launcher Windows (Batch)
├── start_bot.ps1           # Launcher Windows (PowerShell)
├── README.md               # Ta dokumentacja
├── logs/                   # Katalog z logami
│   └── portal_bot.log
└── bot_stats.json          # Statystyki (auto-generated)
```

## 🔧 Konfiguracja

### Zmiana czasów na stronach

W pliku `main_bot.py`, metoda `process_single_portal`:

```python
# Strona główna (zmień min_time i max_time)
controller.visit_homepage(min_time=12, max_time=18)

# Artykuł (zmień min_time i max_time)
controller.visit_article(min_time=14, max_time=20)
```

### Zmiana przerwy między sesjami

W pliku `main_bot.py`, metoda `run`:

```python
# Zmień wartość (domyślnie 3 sekundy)
time.sleep(3)
```

### Zmiana timeout dla auto-restartu

W pliku `main_bot.py`, metoda `run`:

```python
# Zmień timeout_seconds (domyślnie 60 sekund)
if self.monitoring.is_hung(timeout_seconds=60):
```

### Zmiana częstotliwości wyświetlania statystyk

W pliku `main_bot.py`, metoda `run`:

```python
# Zmień print_interval (domyślnie 30 sekund)
self.monitoring.start_monitoring(print_interval=30)
```

## 🎨 Fingerprints - Szczegóły

### Co jest generowane losowo?

1. **User Agent** - 5 różnych wersji Chrome
2. **Rozdzielczość ekranu** - 7 popularnych rozdzielczości
3. **WebGL Vendor/Renderer** - Intel, NVIDIA, AMD z realistycznymi GPU
4. **Hardware Concurrency** - 4, 6, 8, 12, 16 rdzeni
5. **Device Memory** - 4, 8, 16, 32 GB
6. **Canvas Fingerprint** - 32-znakowy hash
7. **Audio Context** - Losowa wartość 100-200
8. **Język** - Polski z różnymi wariantami preferencji

### Co jest stałe?

1. **Platform** - Win32 (Windows)
2. **Timezone** - Europe/Warsaw
3. **Timezone Offset** - -60 (UTC+1)
4. **Color Depth** - 24 bit
5. **Pixel Ratio** - 1.0

## 🍪 Cookies

Bot generuje realistyczne cookies dla każdej sesji:
- `_ga` - Google Analytics Visitor ID
- `_gid` - Google Analytics Session ID
- `session_id` - Session tracking
- `cookie_consent` - RODO consent

## 📈 Analytics Tracking

Bot jest zaprojektowany aby:
- ✅ W pełni wykonywać kod Google Analytics
- ✅ Generować ruch klasyfikowany jako "Direct"
- ✅ Tworzyć realistyczne sesje z czasem na stronie
- ✅ Scrollować zawartość (analytics trackuje scroll depth)
- ✅ Odwiedzać wiele stron (page views)

## ⚠️ Ważne Informacje

1. **Proxy**: Bot **WYMAGA** działającego proxy iproxy.online! Bez proxy nie uruchomi się!
2. **Zmiana IP**: Automatyczna po każdej sesji (60s przerwa)
3. **Zasoby**: Bot otwiera 16 przeglądarek jednocześnie - upewnij się że masz wystarczająco RAM (min. 8GB zalecane)
4. **Chrome**: Musi być zainstalowany Google Chrome
5. **ChromeDriver**: Pobierany automatycznie przez webdriver-manager
6. **Internet**: Wymagane stabilne połączenie internetowe

## 🐛 Troubleshooting

### Bot nie uruchamia się
- Sprawdź czy Python jest zainstalowany: `python --version`
- Sprawdź czy Chrome jest zainstalowany
- Zainstaluj zależności: `pip install -r requirements.txt`

### Bot zawiesza się
- Sprawdź logi w `logs/portal_bot.log`
- Upewnij się że masz wystarczająco RAM
- Zmniejsz liczbę równoległych przeglądarek (edytuj kod)

### Nie wszystkie portale są odwiedzane
- Sprawdź logi - mogą być problemy z konkretnymi portalami
- Bot kontynuuje jeśli ≥80% portali się uda

### Błąd "ChromeDriver"
- Usuń cache: `~/.wdm` (Linux/Mac) lub `%USERPROFILE%\.wdm` (Windows)
- Uruchom ponownie - webdriver-manager pobierze nowy ChromeDriver

## 📝 Licencja

Projekt do użytku wewnętrznego.

## 👨‍💻 Autor

Created with ❤️ for traffic generation

## 📞 Wsparcie

W przypadku problemów sprawdź logi w `logs/portal_bot.log`

