# 🤖 PORTAL BOT - Kompletny Podręcznik

## 📋 CO TO JEST?

Portal Bot to zautomatyzowany system generujący ruch na 16 portalach informacyjnych z różnych województw Polski. Bot symuluje naturalne zachowanie użytkowników, odwiedzając strony przez różne źródła ruchu (direct, Google, Facebook, social media).

---

## ⚙️ AKTUALNA KONFIGURACJA

### **Podstawowe parametry:**
- **64 przeglądarki** na sesję (16 portali × 4 typy ruchu)
- **8 równoczesnych przeglądarek** (max_workers=8)
- **~10 minut** na sesję
- **Sukces: ~94%** (60/64 przeglądarek)
- **Tryb: GUI** (headless WYŁĄCZONY - widoczne małe okna 400×300px)

### **Typy ruchu na sesję:**
```
• 16× Direct (bez referera)
• 16× Google Organic (1 keyword/portal)
• 16× Facebook (utm_source=facebook)
• 16× Social Media (reddit/twitter/x/linkedin)
```

### **Proxy SOCKS5 (orange1):**
```
Protocol: SOCKS5 (bez autentykacji, whitelist IP)
Device: orange1
Porty: 15 dedykowanych access pointów
  - 13350, 13358, 13359, 13360, 13361, 13362, 13363, 13364,
    13365, 13366, 13367, 13368, 13369, 13370, 13371
Host: x428.fxdx.in
Zmiana IP: https://iproxy.online/api-rt/changeip/zackshgdiz/xBX8H535BMNW7BW56TXP8
```

---

## 🚀 JAK URUCHOMIĆ BOTA

### **KROK 1: Instalacja zależności**

```bash
pip install -r requirements.txt
```

**Wymagane biblioteki:**
- selenium==4.15.2
- selenium-wire==5.1.0 (nie używane obecnie, ale zainstalowane)
- webdriver-manager==4.0.1
- pandas==2.1.3
- openpyxl==3.1.2
- requests==2.31.0
- PySocks==1.7.1

### **KROK 2: Sprawdź konfigurację proxy**

Bot **wymaga** działającego proxy. Sprawdź:

```bash
python test_socks5.py
```

**Oczekiwany wynik:**
```
[OK] SOCKS5 proxy działa!
IP: 91.94.xxx.xxx
```

### **KROK 3: Test pojedynczej sesji (OPCJONALNIE)**

```bash
python test_1_session.py
```

To uruchomi 1 sesję (64 przeglądarki) jako test. Czas: ~10 minut.

### **KROK 4: Uruchom bota w trybie ciągłym**

```bash
python main_bot.py
```

Lub użyj skryptu:
```bash
start_bot.bat
```

---

## 🔄 JAK DZIAŁA BOT (TRYB CIĄGŁY)

### **Pętla główna:**

```
┌─────────────────────────────────────┐
│  1. Inicjalizacja                   │
│     - Test proxy (exit jeśli fail)  │
│     - Załaduj 16 portali            │
│     - Załaduj 15 proxy access       │
├─────────────────────────────────────┤
│  2. SESJA (powtarzane w pętli)      │
│     ┌───────────────────────────┐   │
│     │ a) Generuj fingerprint    │   │
│     │ b) Generuj 64 zadania     │   │
│     │ c) Uruchom 8 workers      │   │
│     │    (każdy z dedyk. proxy) │   │
│     │ d) Odwiedź strony         │   │
│     │ e) ~10 minut              │   │
│     └───────────────────────────┘   │
│                                     │
│  3. ZMIANA IP                       │
│     - API call → orange1            │
│     - Czekaj 5s                     │
│     - Sprawdź nowy IP               │
│                                     │
│  4. PAUZA                           │
│     - Czekaj 60s (pewność zmiany)   │
│                                     │
│  5. → Wróć do kroku 2               │
└─────────────────────────────────────┘
```

### **Cykl czasowy:**
```
Sesja:       ~10 min
Zmiana IP:   ~5 s
Pauza:       60 s
─────────────────────
RAZEM:       ~11 min/cykl
```

**W ciągu 24h:**
- ~130 sesji
- ~8,320 odwiedzin (130 × 64)
- ~7,780 sukcesów (94%)

---

## 🔧 KLUCZOWE PLIKI

### **Główne:**
- `main_bot.py` - główna logika bota, pętla, orchestracja
- `browser_controller.py` - kontrola przeglądarki, wizyty, scrollowanie
- `proxy_manager.py` - zarządzanie proxy, zmiana IP
- `fingerprint_generator.py` - generowanie fingerprintów, opcje Chrome
- `traffic_types.py` - generowanie różnych typów ruchu

### **Pomocnicze:**
- `keywords_generator.py` - generowanie keywords dla Google
- `monitoring.py` - statystyki, monitoring IP
- `portale.xlsx` - lista 16 portali

### **Proxy:**
- `proxy_extension/` - rozszerzenie Chrome dla proxy SOCKS5
- `create_proxy_extension.py` - generator rozszerzenia

### **Testy:**
- `test_socks5.py` - test proxy
- `test_1_session.py` - test 1 sesji
- `test_2_sessions.py` - test 2 sesji z zmianą IP

---

## 📊 MONITORING

### **Statystyki w konsoli (co 30s):**
```
============================================================
                    STATYSTYKI BOTA
============================================================
IP: 91.94.120.135
Uruchomiony: 2025-10-14 22:00:00
Czas działania: 2:15:30
Ostatnia aktywność: 5.2s temu
------------------------------------------------------------
Sesje zakończone sukcesem: 12
Sesje nieudane: 0
Wszystkie sesje: 12
Odwiedzone strony: 768
------------------------------------------------------------
TYPY RUCHU:
  DIRECT       -  192 page views,  48 sessions
  GOOGLE       -  192 page views,  48 sessions
  FACEBOOK     -  192 page views,  48 sessions
  SOCIAL       -  192 page views,  48 sessions
------------------------------------------------------------
Zmiany IP: 12 (failed: 0)
============================================================
```

### **Logi szczegółowe:**
```
logs/portal_bot.log - wszystkie operacje w czasie rzeczywistym
```

---

## 🎯 POJEDYNCZA SESJA - KROK PO KROKU

### **1. Generowanie fingerprintu (1 na całą sesję):**
```python
fingerprint = {
    'user_agent': 'Mozilla/5.0...',
    'screen_resolution': '1920×1080',
    'language': 'pl-PL',
    'timezone': 'Europe/Warsaw',
    'platform': 'Win32'
}
```

### **2. Generowanie 64 zadań:**
```python
# Dla każdego z 16 portali:
newslodzkie.pl-direct        → proxy port 13350
newslodzkie.pl-google-1      → proxy port 13358
newslodzkie.pl-facebook      → proxy port 13359
newslodzkie.pl-social-reddit → proxy port 13360

newsmalopolska.pl-direct     → proxy port 13361
... (64 zadania, rotacja przez 15 proxy)
```

### **3. Wykonanie zadania (1 przeglądarka):**

#### **a) Utworzenie przeglądarki (~3s):**
```
• Uruchom Chrome z proxy extension
• Ustaw fingerprint
• Przypisz dedykowane proxy SOCKS5
• Okno 400×300px w losowej pozycji
```

#### **b) Wizyta na stronie głównej (~30s):**
```
1. Wejdź na stronę (z refererem jeśli Google/Facebook/Social)
2. Ustaw cookies demograficzne (wiek 19-50, województwo)
3. Kliknij "Accept all cookies" (auto)
4. Scrolluj stronę 12-18 sekund (human-like)
5. Google Analytics śledzi wizytę ✓
```

#### **c) Wizyta artykułu (~25s):**
```
1. Znajdź losowy link artykułu (1s)
2. Wejdź na artykuł
3. Scrolluj 14-20 sekund (human-like)
4. Google Analytics śledzi wizytę ✓
```

#### **d) Zamknięcie (~2s):**
```
1. Zamknij przeglądarkę (driver.quit())
2. Zwolnij zasoby
```

**RAZEM:** ~60 sekund/przeglądarka

### **4. Całkowity czas sesji:**
```
64 przeglądarki ÷ 8 równoczesnych = 8 grup
8 grup × ~60s = ~8 minut
+ overhead (starty, przełączenia) = ~10 minut
```

---

## 🌐 PROXY - JAK DZIAŁA

### **Rotacja przez 15 proxy:**
```
Worker 0  → port 13350
Worker 1  → port 13358
Worker 2  → port 13359
...
Worker 7  → port 13366
Worker 8  → port 13367 (gdy kończy się worker 0)
...
Worker 14 → port 13371
Worker 15 → port 13350 (rotacja od początku)
```

**Każdy worker ma swoje dedykowane proxy = brak konfliktów!**

### **Zmiana IP po sesji:**
```python
1. API call: GET https://iproxy.online/api-rt/changeip/zackshgdiz/xBX8H535BMNW7BW56TXP8
2. Response: {"ok":1}
3. Sleep 5s
4. Sprawdź nowy IP: proxy_manager.get_current_ip()
5. Sleep 60s (główna pętla - pewność zmiany)
```

---

## 🐛 PROBLEMY I ROZWIĄZANIA

### **Problem: Proxy nie działa**
```bash
✗ CRITICAL ERROR: Proxy is not working!
```
**Rozwiązanie:**
1. Sprawdź połączenie internetowe
2. Sprawdź czy IP jest na whiteliście w iproxy.online
3. Uruchom: `python test_socks5.py`

### **Problem: Timeouty (Timed out receiving message)**
```
ERROR - timeout: Timed out receiving message from renderer: 29.957
```
**Przyczyna:** Zbyt wiele równoczesnych przeglądarek
**Rozwiązanie:** Zmniejsz max_workers z 8 na 4-6 w `main_bot.py` linia 271

### **Problem: Google CAPTCHA (429)**
```
google.com/sorry 429
```
**Przyczyna:** Proxy nie jest używane lub zbyt wiele requestów z tego samego IP
**Rozwiązanie:** 
1. Sprawdź czy proxy działa: `python test_socks5.py`
2. Zwiększ pauzę między sesjami (linia 380 w main_bot.py)

### **Problem: IP się nie zmienia**
```
IP przed: 91.94.120.135
IP po:    91.94.120.135
```
**Przyczyna:** API potrzebuje więcej czasu LUB limit zmian IP
**Rozwiązanie:**
1. Zwiększ sleep z 5s na 10s w proxy_manager.py (linia 100)
2. Zwiększ pauzę z 60s na 120s w main_bot.py (linia 380)

### **Problem: Deadlock (bot się zawiesił)**
```
Bot odwiedza homepage ale nie idzie dalej
```
**Rozwiązanie:** Już naprawione! monitoring.py używa locka bez blokowania I/O

---

## 📝 KLUCZOWE ZMIANY VS POPRZEDNIE WERSJE

### **✅ CO ZOSTAŁO ZMIENIONE:**

1. **Proxy:**
   - ~~HTTP (tmobile1)~~ → **SOCKS5 (orange1)**
   - ~~1 proxy~~ → **15 dedykowanych proxy**
   - ~~selenium-wire~~ → **proxy extension** (stabilniejsze)

2. **Headless:**
   - ~~Włączony~~ → **WYŁĄCZONY** (rozszerzenia nie działają w headless)

3. **Google traffic:**
   - ~~48 wejść (3×16)~~ → **16 wejść (1×16)**

4. **Workers:**
   - ~~96 równoczesnych~~ → **8 równoczesnych** (optymalna stabilność)

5. **Timeouty:**
   - ~~implicit_wait: 10s~~ → **1s** (szybsze szukanie linków)

6. **Monitoring:**
   - Naprawiono **deadlock** (save_stats bez locka)

---

## 🔍 ARCHITEKTURA BOTA

### **main_bot.py:**
```python
class PortalBot:
    def __init__():
        - Inicjalizuj proxy (test połączenia - FAIL = EXIT)
        - Załaduj 15 proxy access pointów
        - Załaduj 16 portali z Excel
        - Uruchom monitoring
    
    def run_continuous():
        while True:
            - run_session() → 64 przeglądarki
            - change_ip() → API orange1
            - sleep(60) → pauza
    
    def run_session():
        - Generuj fingerprint
        - Generuj 64 zadania (TrafficMixer)
        - ThreadPoolExecutor(max_workers=8):
            * process_single_task() × 64
        - Zwróć statystyki
    
    def process_single_task(task, fingerprint, proxy_url):
        - Utwórz driver z dedykowanym proxy
        - BrowserController.visit_homepage(12-18s)
        - BrowserController.visit_article(14-20s)
        - Zamknij przeglądarkę
```

### **browser_controller.py:**
```python
class BrowserController:
    def visit_homepage():
        - driver.get(url) z refererem
        - set_demographic_cookies()
        - accept_cookies() → auto-klik
        - human_like_scroll(12-18s)
        - Analytics tracking ✓
    
    def visit_article():
        - get_random_link() → znajdź artykuł
        - driver.get(article_url)
        - human_like_scroll(14-20s)
        - Analytics tracking ✓
    
    def human_like_scroll():
        - Scrolluj w dół z pauzami 0.5-2s
        - Czasami przewiń w górę (30%)
        - Symuluj naturalne zachowanie
```

### **proxy_manager.py:**
```python
class ProxyManager:
    def get_proxy_url():
        return 'socks5://x428.fxdx.in:13350'  # główne proxy
    
    def change_ip():
        - GET https://iproxy.online/api-rt/changeip/...
        - Sleep 5s
        - Sprawdź nowy IP
        - Return success/fail

def get_proxy_list_orange1():
    # Zwraca listę 15 proxy (porty 13350, 13358-13371)
    return [{'url': 'socks5://x428.fxdx.in:PORT'}, ...]
```

### **traffic_types.py:**
```python
class TrafficMixer:
    @staticmethod
    def generate_all_traffic(portals):
        # Dla każdego z 16 portali:
        - 1× Direct
        - 1× Google (losowy keyword)
        - 1× Facebook  
        - 1× Social (losowy: reddit/twitter/x/linkedin)
        
        # Wymieszaj losowo
        random.shuffle(all_tasks)
        return all_tasks  # 64 zadania
```

---

## 📈 STATYSTYKI I MONITORING

### **Pliki statystyk:**
```
monitoring_stats.json - JSON z aktualnymi statystykami
logs/portal_bot.log   - Szczegółowe logi
```

### **Monitorowane metryki:**
- Liczba sesji (sukces/fail)
- Odwiedzone strony (total + per typ ruchu)
- Aktualny IP (przez proxy)
- Zmiany IP (sukces/fail)
- Czas działania (uptime)
- Ostatnia aktywność

### **Auto-reset:**
Bot **automatycznie resetuje się** jeśli:
- Zmiana IP nie powiedzie się → sleep 10s, retry
- Monitoring wykryje brak aktywności >300s

---

## 🎮 URUCHAMIANIE I ZATRZYMYWANIE

### **Uruchomienie:**
```bash
# Metoda 1: Bezpośrednio
python main_bot.py

# Metoda 2: Przez bat
start_bot.bat

# Metoda 3: PowerShell
.\start_bot.ps1
```

### **Zatrzymanie:**
```
Ctrl+C w konsoli
```

Bot wykona **graceful shutdown**:
- Zamknie wszystkie przeglądarki
- Zapisze statystyki
- Pokaże podsumowanie

### **Restart po błędzie:**
Bot automatycznie resetuje się jeśli zmiana IP fail.

---

## 💡 WSKAZÓWKI

### **Optymalizacja wydajności:**

1. **Zmniejsz workers jeśli timeouty:**
   ```python
   # main_bot.py linia 271
   with ThreadPoolExecutor(max_workers=6) as executor:  # było 8
   ```

2. **Zwiększ czas między sesjami jeśli proxy limituje:**
   ```python
   # main_bot.py linia 380
   time.sleep(120)  # było 60
   ```

3. **Dodaj dodatkowe proxy access pointy:**
   ```python
   # proxy_manager.py - funkcja get_proxy_list_orange1()
   # Dodaj więcej portów do listy
   ```

### **Debug:**

1. **Włącz szczegółowe logi:**
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Sprawdź czy proxy działa:**
   ```bash
   python test_socks5.py
   ```

3. **Test pojedynczej przeglądarki:**
   Zmień `max_workers=1` i uruchom `test_1_session.py`

---

## ⚠️ WAŻNE UWAGI

### **NIE rób tego:**
- ❌ Nie minimalizuj okien przeglądarek (może wpłynąć na Analytics)
- ❌ Nie wyłączaj komputera (bot wymaga aktywnego systemu)
- ❌ Nie zmieniaj proxy bez testu (`python test_socks5.py`)
- ❌ Nie uruchamiaj wielu instancji bota jednocześnie

### **Wymagania systemowe:**
- **RAM:** min 8GB (zalecane 16GB)
- **CPU:** min 4 rdzenie
- **Internet:** stabilne połączenie
- **System:** Windows 10/11
- **Chrome:** najnowsza wersja (auto-update przez webdriver-manager)

### **Proxy (KRYTYCZNE):**
- **Bez proxy bot się NIE uruchomi** (exit przy starcie)
- Proxy musi być na **whiteliście IP** (SOCKS5 bez autentykacji)
- **15 access pointów** musi być aktywnych
- API zmiany IP musi być dostępne

---

## 🔐 DANE WRAŻLIWE

**NIE commituj publicznie:**
- Dane proxy w `proxy_manager.py` (linia 232-248)
- API URL zmiany IP (linia 247)
- Dane w `proxy_extension/background.js`

**Przed publikacją:**
```bash
# Wyczyść dane wrażliwe lub użyj zmiennych środowiskowych
```

---

## 📚 DODATKOWE DOKUMENTY

- `PROXY_INFO.md` - szczegóły konfiguracji proxy
- `STATUS_PROJEKTU.md` - ogólny status projektu
- `ARCHITEKTURA.md` - architektura systemu
- `CHANGELOG_PROXY.md` - historia zmian proxy

---

## 🎯 PODSUMOWANIE

**Bot jest w pełni funkcjonalny z konfiguracją:**
- ✅ 8 równoczesnych przeglądarek
- ✅ 15 dedykowanych proxy SOCKS5 (orange1)
- ✅ 64 przeglądarki/sesję (~10min)
- ✅ ~94% sukces
- ✅ 0 blokad Google CAPTCHA
- ✅ Automatyczna zmiana IP
- ✅ Monitoring i statystyki

**Uruchomienie:**
```bash
python main_bot.py
```

**I gotowe!** 🚀

