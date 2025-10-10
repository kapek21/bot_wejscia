# 🏗️ Architektura Portal Bot

## Przegląd Systemu

Portal Bot to zaawansowany system generowania ruchu na portalach internetowych z realistycznymi fingerprintami i ludzkim zachowaniem.

## 📦 Moduły

### 1. `fingerprint_generator.py`
**Odpowiedzialność**: Generowanie zaawansowanych fingerprintów przeglądarki

**Klasa**: `FingerprintGenerator`

**Funkcje**:
- `generate()` - Generuje kompletny fingerprint dla sesji
- `generate_cookies()` - Generuje realistyczne cookies
- `get_chrome_options()` - Tworzy opcje Chrome z fingerprintem

**Fingerprint zawiera**:
- User Agent (5 wariantów Chrome)
- Rozdzielczość ekranu (7 popularnych)
- WebGL vendor/renderer (Intel/NVIDIA/AMD)
- Hardware Concurrency (4-16 rdzeni)
- Device Memory (4-32 GB)
- Canvas & Audio fingerprints
- Język, timezone, platform

**Dlaczego jest ważny**:
Prawdziwe przeglądarki mają unikalne fingerprints. Bot symuluje to aby nie być wykrywanym jako automation.

---

### 2. `browser_controller.py`
**Odpowiedzialność**: Kontrola pojedynczej przeglądarki z realistycznym zachowaniem

**Klasa**: `BrowserController`

**Funkcje**:
- `inject_fingerprint_scripts()` - Wstrzykuje JS do zmiany fingerprinta
- `human_like_scroll()` - Scrolluje jak człowiek z easing
- `get_random_link()` - Znajduje losowy link artykułu
- `visit_homepage()` - Odwiedza stronę główną (12-18s)
- `visit_article()` - Odwiedza artykuł (14-20s)

**Realistyczne zachowanie**:
- Płynne scrollowanie z easing (ease-out cubic)
- Losowe pauzy między scrollami (0.5-2s)
- Czasami scroll w górę (30% szans)
- Losowe wybieranie linków
- Czekanie na załadowanie stron

**Dlaczego jest ważny**:
Analytics tracking może wykryć boty po nienaturalnym zachowaniu. Ten moduł symuluje prawdziwego użytkownika.

---

### 3. `monitoring.py`
**Odpowiedzialność**: Monitorowanie działania bota i zbieranie statystyk

**Klasa**: `MonitoringSystem`

**Funkcje**:
- `update_ip()` - Sprawdza aktualny IP
- `mark_activity()` - Oznacza aktywność bota
- `is_hung()` - Wykrywa zawieszenie (>60s)
- `increment_session()` - Liczy sesje
- `increment_page_visits()` - Liczy wejścia
- `get_stats()` - Zwraca statystyki
- `print_stats()` - Wyświetla statystyki
- `save_stats()` / `load_stats()` - Persistent storage

**Statystyki**:
- Sesje udane/nieudane
- Suma odwiedzonych stron
- Aktualny IP
- Czas działania (uptime)
- Ostatnia aktywność

**Dlaczego jest ważny**:
Pozwala monitorować czy bot działa poprawnie i zbierać metryki. Wykrywa zawieszenia i pozwala na auto-restart.

---

### 4. `main_bot.py`
**Odpowiedzialność**: Główna logika bota, zarządzanie sesjami

**Klasa**: `PortalBot`

**Funkcje**:
- `load_portals()` - Wczytuje portale z Excel
- `create_driver()` - Tworzy Chrome WebDriver
- `process_single_portal()` - Przetwarza jeden portal
- `run_session()` - Uruchamia pełną sesję (16 portali)
- `cleanup_drivers()` - Zamyka przeglądarki
- `run()` - Główna pętla bota

**Przepływ sesji**:
1. Wygeneruj fingerprint
2. Uruchom 16 przeglądarek równolegle (ThreadPoolExecutor)
3. Każda przeglądarka:
   - Odwiedza stronę główną
   - Scrolluje 12-18s
   - Odwiedza artykuł
   - Scrolluje 14-20s
4. Zamknij wszystkie przeglądarki
5. Pauza 3s
6. Powtórz

**Dlaczego jest ważny**:
To serce systemu - koordynuje wszystkie moduły i zarządza lifecycle sesji.

---

## 🔄 Przepływ Danych

```
┌─────────────────┐
│  portale.xlsx   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│        PortalBot.load_portals() │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     PortalBot.run_session()     │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ FingerprintGenerator.generate() │ ◄─── Jeden fingerprint dla całej sesji
└────────┬────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────┐
│          ThreadPoolExecutor (16 workers)                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  process_single_portal() × 16 (równolegle)       │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │  1. create_driver()                        │  │   │
│  │  │  2. BrowserController.visit_homepage()     │  │   │
│  │  │  3. BrowserController.visit_article()      │  │   │
│  │  │  4. driver.quit()                          │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Monitoring.increment_*()      │ ◄─── Aktualizacja statystyk
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  time.sleep(3)                  │ ◄─── Pauza między sesjami
└─────────────────────────────────┘
         │
         └─────► Powtórz sesję
```

---

## 🧵 Threading Model

### Główny wątek (Main Thread)
- Główna pętla bota
- Tworzenie sesji
- Sprawdzanie zawieszenia

### Wątek monitorowania (Monitoring Thread)
- Daemon thread (zamyka się z głównym wątkiem)
- Aktualizuje IP co 5 minut
- Wyświetla statystyki co 30s
- Uruchamiany przez `monitoring.start_monitoring()`

### ThreadPoolExecutor (16 workers)
- Równoległe przetwarzanie portali
- Każdy worker = jeden portal
- `as_completed()` - zbiera wyniki w miarę kończenia

**Dlaczego threading?**
- 16 portali jednocześnie = 16x szybciej
- Monitoring w tle nie blokuje głównej pętli
- ThreadPoolExecutor zapewnia thread-safe execution

---

## 🎯 Direct Traffic - Jak to działa?

### Problem:
Google Analytics klasyfikuje ruch jako:
- **Direct** - bezpośrednie wejście (wpisany URL, zakładka)
- **Referral** - z innej strony
- **Organic** - z wyszukiwarki
- **Social** - z social media

### Rozwiązanie:
1. **Brak Referrera**: Bot wchodzi bezpośrednio na URL (bez `document.referrer`)
2. **Cookies**: Bot ma cookies jak prawdziwy user (nie nowa sesja)
3. **Session Storage**: Bot ma session storage
4. **Fingerprint**: Bot wygląda jak prawdziwa przeglądarka

### Analytics Tracking:
Bot wykonuje pełny kod analytics:
- ✅ JavaScript jest włączony
- ✅ Cookies są włączone
- ✅ Strona jest w pełni załadowana
- ✅ User scrolluje (scroll tracking)
- ✅ User spędza czas na stronie (time on page)
- ✅ User odwiedza wiele stron (page views)

---

## 🔒 Anti-Detection Techniques

### 1. Fingerprint Spoofing
- Zmiana WebGL vendor/renderer
- Zmiana hardware concurrency
- Zmiana device memory
- Zmiana canvas fingerprint
- Zmiana audio context

### 2. WebDriver Hiding
```javascript
Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
delete navigator.__proto__.webdriver
```

### 3. Plugins & Chrome Object
```javascript
Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})
window.chrome = { runtime: {} }
```

### 4. Human-like Behavior
- Randomowe czasy (12-18s, 14-20s)
- Płynne scrollowanie z easing
- Losowe pauzy i cofanie
- Naturalne ruchy (nie instant scroll)

### 5. Headless Detection Prevention
- `--disable-blink-features=AutomationControlled`
- `excludeSwitches: ["enable-automation"]`
- Realistyczny User Agent

---

## 📊 Statystyki - Persistent Storage

### bot_stats.json
```json
{
  "successful_sessions": 42,
  "failed_sessions": 1,
  "total_page_visits": 1344,
  "last_update": "2025-10-10T12:34:56",
  "current_ip": "123.45.67.89"
}
```

**Dlaczego JSON?**
- Łatwe do odczytu
- Zachowane między restartami
- Można analizować zewnętrznymi narzędziami

---

## 🛡️ Error Handling

### Try-Catch Hierarchy
```
main_bot.run()
  └─► try: run_session()
        └─► try: process_single_portal()
              └─► try: visit_homepage()
              └─► try: visit_article()
              └─► finally: driver.quit()
```

### Strategia:
1. **Retry na poziomie sesji**: Jeśli sesja fail, loguj i kontynuuj
2. **Timeout detection**: Wykryj zawieszenie po 60s
3. **Cleanup**: Zawsze zamknij przeglądarki (finally)
4. **Logging**: Loguj wszystkie błędy do `portal_bot.log`

---

## ⚡ Optymalizacje

### 1. Concurrent Execution
- 16 portali równolegle zamiast sekwencyjnie
- Czas sesji: ~30s zamiast ~8 minut

### 2. Headless Chrome
- Brak GUI = mniej RAM
- Szybsze renderowanie

### 3. Shared Fingerprint
- Jeden fingerprint dla całej sesji
- Nie trzeba generować 16x

### 4. Lazy Loading
- ChromeDriver pobierany tylko przy pierwszym użyciu (webdriver-manager)

---

## 📝 Logging Strategy

### Poziomy logowania:
- **INFO**: Normalne operacje (sesje, wejścia)
- **WARNING**: Problemy nieblokujące (brak artykułu)
- **ERROR**: Błędy (crash przeglądarki)
- **DEBUG**: Szczegóły (fingerprint injection)

### Output:
- Console: INFO+
- File (`portal_bot.log`): wszystko

### Format:
```
2025-10-10 12:34:56 - PortalBot - INFO - Starting new session
2025-10-10 12:35:20 - Browser-zachodniopomorskie - INFO - Visited homepage
```

---

## 🔮 Przyszłe Rozszerzenia

### Możliwe ulepszenia:
1. **Proxy rotation**: Rotacja IP przez proxy
2. **VPN integration**: Automatyczna zmiana VPN
3. **Captcha solving**: Integracja z 2captcha/AntiCaptcha
4. **Machine learning**: Uczenie na prawdziwych sesjach
5. **Dashboard**: Web UI z live statystykami
6. **Database**: PostgreSQL zamiast JSON
7. **Distributed**: Wiele botów na różnych maszynach
8. **A/B Testing**: Różne strategie scrollowania

---

## 🎓 Najważniejsze Decyzje Architektoniczne

### 1. Dlaczego Selenium zamiast Puppeteer?
- ✅ Python ekosystem (łatwiejszy deployment)
- ✅ Stabilniejszy WebDriver
- ✅ Lepsza dokumentacja dla fingerprintingu

### 2. Dlaczego Threading zamiast Asyncio?
- ✅ Selenium jest synchroniczne
- ✅ ThreadPoolExecutor jest prosty
- ✅ Wystarczy dla 16 przeglądarek

### 3. Dlaczego JSON zamiast Database?
- ✅ Prosty deployment (zero dependencies)
- ✅ Wystarczy dla obecnych potrzeb
- ✅ Łatwo migrować do DB później

### 4. Dlaczego jeden fingerprint na sesję?
- ✅ Symuluje jednego usera odwiedzającego wszystkie portale
- ✅ Mniej computational overhead
- ✅ Bardziej realistyczne (user z jednego IP odwiedza wszystkie portale)

---

## 📚 Zależności

### Core:
- **selenium**: WebDriver automation
- **webdriver-manager**: Auto-download ChromeDriver
- **pandas**: Excel parsing
- **requests**: IP checking

### Opcjonalne:
- **openpyxl**: Excel backend (automatycznie instalowane przez pandas)

---

## 🏁 Podsumowanie

Portal Bot to **produkcyjny system** zaprojektowany aby:
- ✅ Generować **realistyczny ruch** na 16 portalach
- ✅ **Nie być wykrywanym** przez analytics
- ✅ Działać **24/7** z auto-restartem
- ✅ Być **łatwy w deploymencie** (zero config)
- ✅ Być **monitorowalny** (stats, logs, IP)

**Architektura jest:**
- **Modularna** - każdy moduł ma jedną odpowiedzialność
- **Skalowalna** - łatwo dodać więcej portali
- **Niezawodna** - error handling + auto-restart
- **Maintainable** - czysty kod, dokumentacja

