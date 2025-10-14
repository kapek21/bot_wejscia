# 🤖 Portal Bot - Advanced Traffic Generator

**Zaawansowany bot do generowania ruchu na 16 portalach regionalnych z Google Analytics tracking**

[![Status](https://img.shields.io/badge/status-production-green)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-private-red)]()

---

## 🎯 Features

### 96 Przeglądarek na Sesję
- **16 Direct** - bezpośredni ruch (bez referrera)
- **48 Google Organic** - ruch z wyszukiwarki (3 keywords × 16 portali)
- **16 Facebook** - ruch z social media (utm_source=facebook)
- **16 Social Media** - random (reddit/twitter/x/linkedin)

### Proxy iproxy.online
- ✅ Obowiązkowe proxy
- ✅ Automatyczna zmiana IP po każdej sesji
- ✅ Lokalizacja: Polska (T-Mobile)
- ✅ Reset przy nieudanej zmianie IP

### Google Analytics Tracking
- ✅ **Działa w trybie headless!**
- ✅ Wszystkie typy ruchu klasyfikowane poprawnie
- ✅ Direct, Google/Organic, Facebook, Social
- ✅ Użytkownicy widoczni w Real-Time
- ✅ Lokalizacja z proxy (nie prawdziwe IP)

### Zaawansowane Fingerprints
- User Agent, WebGL, Canvas, Audio
- Hardware Concurrency, Device Memory
- Cookies, Timezone, Language (Polski)
- Każda sesja = unikalny fingerprint

### Realistyczne Zachowanie
- Płynne scrollowanie z easing
- Czasy: 12-18s główna, 14-20s artykuł
- Losowe wybieranie artykułów
- Wymuszenie wykonania Analytics events

### Monitoring & Stats
- Statystyki per typ ruchu
- Licznik sesji i page views
- Aktualny IP przez proxy
- Wykrywanie zawieszenia (>5 min)
- Auto-restart przy problemach

---

## 📋 Quick Start

### 1. Instalacja

```bash
git clone https://github.com/kapek21/bot_wejscia.git
cd bot_wejscia
pip install -r requirements.txt
```

### 2. Konfiguracja

**Ważne:** Bot wymaga:
- Plik `portale.xlsx` w katalogu nadrzędnym
- Skonfigurowane proxy iproxy.online (w `proxy_manager.py`)
- Google Chrome zainstalowany

### 3. Test proxy

```bash
python test_proxy.py
```

### 4. Uruchomienie

```bash
python main_bot.py
```

lub na Windows: kliknij `start_bot.bat`

---

## 📊 Jak to działa

### Jedna sesja (~6-9 minut):

1. **Generowanie fingerprinta** - jeden dla całej sesji
2. **Generowanie 96 zadań:**
   - 16 direct
   - 48 google (3 keywords × 16 portali)
   - 16 facebook
   - 16 social media
3. **Uruchomienie 96 przeglądarek headless** (równolegle)
4. **Każda przeglądarka:**
   - Odwiedza stronę główną (12-18s)
   - Scrolluje jak człowiek
   - Odwiedza losowy artykuł (14-20s)
   - Wysyła dane do Analytics
5. **Zmiana IP** przez API iproxy.online
6. **Przerwa 60s** (pewność zmiany IP)
7. **Powtórzenie** z nowym IP i fingerprintem

### Statystyki (przykład):

```
Sesje: 15 (udane: 15, nieudane: 0)
Page views: 2880 (15 sesji × 192)

TYPY RUCHU:
  DIRECT       -  480 page views,  240 sessions
  GOOGLE       - 1440 page views,  720 sessions  
  FACEBOOK     -  480 page views,  240 sessions
  SOCIAL       -  480 page views,  240 sessions

Zmiany IP: 15 (failed: 0)
```

---

## 🛠️ Wymagania

### Systemowe:
- **Python 3.8+**
- **Google Chrome**
- **RAM:** 16 GB (zalecane), min. 12 GB
- **CPU:** 8+ rdzeni (zalecane)
- **OS:** Windows 10/11, Linux, macOS

### Zewnętrzne:
- **Proxy:** iproxy.online (skonfigurowane w kodzie)
- **Excel:** Plik `portale.xlsx` z 16 portalami

---

## 📁 Główne Moduły

| Plik | Opis |
|------|------|
| `main_bot.py` | Główny bot (96 przeglądarek) |
| `fingerprint_generator.py` | Generator fingerprintów |
| `browser_controller.py` | Kontroler przeglądarki + Analytics |
| `proxy_manager.py` | Proxy iproxy.online + zmiana IP |
| `monitoring.py` | System monitorowania + stats per typ |
| `keywords_generator.py` | Generator słów kluczowych |
| `traffic_types.py` | 4 typy ruchu (96 zadań) |

---

## 🧪 Testy

```bash
# Test proxy (KRYTYCZNE!)
python test_proxy.py

# Test małej próbki (2 portale = 12 przeglądarek)
python test_bot_small.py

# Test 5 sesji (16 portali = 96 przeglądarek × 5)
python test_bot_5_sessions.py

# Test headless + Analytics
python test_headless_analytics.py
```

---

## 📖 Dokumentacja

- **`STATUS_PROJEKTU.md`** - ⭐ PRZECZYTAJ NAJPIERW! Status dla kolejnego developera
- **`README.md`** - Pełna dokumentacja techniczna
- **`SZYBKI_START.md`** - Quick start guide
- **`ARCHITEKTURA.md`** - Opis architektury systemu
- **`PROXY_INFO.md`** - Dokumentacja proxy
- **`INSTRUKCJA_PORTAL_BOT.md`** - Instrukcja użytkowania

---

## ⚙️ Konfiguracja

### Proxy (w `proxy_manager.py`):
⚠️ **Dane wrażliwe - nie commituj publicznie!**

```python
# SOCKS5 Proxy - orange1 device
proxy_host = "x428.fxdx.in"
proxy_port = 13350
proxy_username = "karol1234567"
proxy_password = "Karol1234567"
change_ip_url = "https://iproxy.online/api-rt/changeip/..."
```

### Czasy (w `main_bot.py`):
```python
visit_homepage(min_time=12, max_time=18)  # Strona główna
visit_article(min_time=14, max_time=20)   # Artykuł
time.sleep(60)                            # Przerwa między sesjami
```

---

## 🎨 Google Analytics

### Co rejestruje bot:

**Acquisition → All Traffic → Source/Medium:**
- `(direct) / (none)` - 16 wejść
- `google / organic` - 48 wejść (różne keywords!)
- `facebook / social` - 16 wejść
- `reddit/twitter/x/linkedin / social` - 16 wejść

**Behavior → Site Content → All Pages:**
- Strony główne portali
- Artykuły (losowo wybrane)

**Realtime:**
- ~96 aktywnych użytkowników podczas sesji
- Lokalizacja: Polska, Mińsk Mazowiecki
- ISP: T-Mobile

---

## ⚠️ Security Notice

⚠️ **Ten kod zawiera wrażliwe dane:**
- Dane dostępowe do proxy
- API keys
- Credentials

**Jeśli publikujesz publicznie:**
- Usuń dane z `proxy_manager.py`
- Użyj zmiennych środowiskowych
- Nie commituj `bot_stats.json`

---

## 🐛 Troubleshooting

### Bot nie uruchamia się
```bash
python test_proxy.py  # Sprawdź proxy NAJPIERW!
```

### Za mało RAM
- Bot potrzebuje ~10-15 GB dla 96 przeglądarek
- Rozważ zmniejszenie liczby w `traffic_types.py`

### ChromeDriver error
- Wyczyść cache: `rm -rf ~/.wdm`

---

## 📊 Stats & Monitoring

Bot automatycznie:
- ✅ Zapisuje statystyki do `bot_stats.json`
- ✅ Loguje do `logs/portal_bot.log`
- ✅ Wyświetla statystyki co 30s
- ✅ Monitoruje IP
- ✅ Wykrywa zawieszenia
- ✅ Resetuje się przy problemach

---

## 🚀 Production Deployment

### Windows:
```bash
start_bot.bat
```

### Linux/Server:
```bash
nohup python3 main_bot.py > bot_output.log 2>&1 &
```

### Docker (TODO):
```bash
docker build -t portal-bot .
docker run -d portal-bot
```

---

## 🎓 Architecture

```
TrafficMixer → 96 zadań
    ↓
ThreadPoolExecutor (96 workers)
    ↓
BrowserController × 96
    ↓
├─ Strona główna (12-18s + scroll)
├─ Artykuł (14-20s + scroll)
└─ Analytics flush (2s)
    ↓
Zmiana IP (API)
    ↓
60s przerwa
    ↓
Repeat
```

---

## 📈 Performance

- **Sesja (96 browsers):** ~5-8 minut
- **Page views per sesja:** ~192
- **Zmiana IP:** ~5 sekund
- **Przerwa:** 60 sekund
- **Cykl:** ~6-9 minut

**24h continuous:**
- ~160-240 sesji
- ~30,000-46,000 page views
- ~160-240 zmian IP

---

## 🌟 Highlights

✨ **96 równoległych przeglądarek** - szybkie wykonanie  
✨ **4 typy ruchu** - diverse traffic sources  
✨ **Google Analytics** - full tracking (headless!)  
✨ **Auto IP change** - każda sesja = nowy IP  
✨ **Auto-restart** - self-healing bot  
✨ **Per-type stats** - szczegółowe statystyki  

---

## 📝 License

Private / Internal Use

---

## 👨‍💻 Author

Created for advanced traffic generation with Analytics tracking

---

## 🔗 Links

- **Repository:** https://github.com/kapek21/bot_wejscia
- **Documentation:** See `STATUS_PROJEKTU.md` for current status
- **Issues:** GitHub Issues (if public)

---

**⚡ Bot is PRODUCTION READY and currently RUNNING! ⚡**

Last update: 2025-10-10

