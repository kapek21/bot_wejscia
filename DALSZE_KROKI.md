# 🚀 Dalsze Kroki - Rozszerzenie do 96 Przeglądarek

## ✅ CO ZOSTAŁO ZROBIONE:

1. ✅ **Browser Controller** - dodano obsługę refererów i traffic_type
2. ✅ **Keywords Generator** - generuje słowa kluczowe dla każdego województwa
3. ✅ **Traffic Types** - moduł obsługujący 4 typy ruchu:
   - Direct (16) - bez referrera
   - Google (48) - 3 keywords × 16 portali
   - Facebook (16) - utm_source=facebook
   - Social (16) - reddit/twitter/x/linkedin random

## 🔄 CO TRZEBA ZROBIĆ:

### 1. Zmodyfikować `main_bot.py`:

**Zmienić metodę `run_session()`:**
```python
def run_session(self):
    # Zamiast 16 portali:
    # portals = self.portals
    
    # Użyj TrafficMixer:
    from traffic_types import TrafficMixer
    all_tasks = TrafficMixer.generate_all_traffic(self.portals)
    # all_tasks = 96 zadań (16 × 6)
    
    # Każde zadanie ma:
    # - url: URL do odwiedzenia
    # - referer: HTTP Referer (lub None)
    # - traffic_type: typ ruchu
    # - portal_name: nazwa portalu
    
    # Uruchom 96 przeglądarek równolegle
    with ThreadPoolExecutor(max_workers=96) as executor:
        futures = {
            executor.submit(self.process_single_task, task, fingerprint): task
            for task in all_tasks
        }
```

**Dodać metodę `process_single_task()`:**
```python
def process_single_task(self, task: dict, fingerprint: dict) -> bool:
    """Przetwarza jedno zadanie (1 przeglądarka)"""
    driver = None
    try:
        driver = self.create_driver(fingerprint)
        
        controller = BrowserController(
            driver=driver,
            portal_url=task['url'],
            portal_name=task['portal_name'],
            fingerprint=fingerprint,
            referer=task.get('referer'),
            traffic_type=task['traffic_type']
        )
        
        # Odwiedź stronę główną
        controller.visit_homepage(min_time=12, max_time=18)
        self.monitoring.increment_page_visits(1)
        
        # Odwiedź artykuł
        if controller.visit_article(min_time=14, max_time=20):
            self.monitoring.increment_page_visits(1)
        
        controller.close()
        return True
        
    except Exception as e:
        self.logger.error(f"Error: {e}")
        if driver:
            driver.quit()
        return False
```

### 2. Przetestować:

**Test z 2 portalami (12 przeglądarek):**
```bash
python test_traffic_mixer_small.py
```

**Test z 16 portalami (96 przeglądarek):**
```bash
python test_bot_5_sessions.py
```

### 3. Monitoring:

**Statystyki powinny pokazywać:**
- Direct: 16 wejść
- Google: 48 wejść (różne keywords)
- Facebook: 16 wejść
- Social: 16 wejść
- **TOTAL: 96 wejść na sesję × 2 (strona główna + artykuł) = 192 page views**

### 4. Google Analytics:

**W Real-Time powinno być widoczne:**
- Źródła ruchu:
  - Direct
  - Google / Organic (z różnymi keywords!)
  - Facebook
  - Reddit/Twitter/X/LinkedIn
- Lokalizacja: Mińsk Mazowiecki, T-Mobile
- ~96 aktywnych użytkowników podczas sesji

## ⚙️ Parametry:

**Czasy:**
- Sesja z 96 przeglądarkami: ~3-4 minuty (headless równolegle)
- Zmiana IP: ~5s
- Przerwa: 60s
- **Cykl: ~4-5 minut**

**RAM:**
- Headless: ~100-150 MB na przeglądarkę
- 96 przeglądarek: ~10-15 GB RAM
- **Zalecane minimum: 16 GB RAM**

**CPU:**
- 96 równoległych przeglądarek = duże obciążenie
- Zalecane: CPU z 8+ rdzeniami

## 🎯 Następny Krok:

**Zaimplementuj zmiany w `main_bot.py` lub stwórz `main_bot_96.py`**

Zobacz przykład implementacji w załączonym kodzie.

