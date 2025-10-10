# 🔒 Konfiguracja Proxy - iproxy.online

## Ważne: Bot nie może działać bez proxy!

Portal Bot został skonfigurowany do **obowiązkowej** pracy przez proxy iproxy.online. Bez działającego proxy bot się nie uruchomi.

## 📋 Konfiguracja Proxy

### Dane dostępowe (skonfigurowane w `proxy_manager.py`):

```
Host: x340.fxdx.in
Port: 13206
Username: softedgedtrailhead104154
Password: jIhUckJtAOt9
Device: tmobile1
```

### Klucze API:
```
API Key 1: f661d5f96788ccb81588f6d09a35ee22c05976047dc20142a50cdc0898b8b758
API Key 2: c45b49d179af7d7cbcbf06f0c1a252bdfd8f379b0d362606bb45e96880f6f030
```

### URL zmiany IP:
```
https://iproxy.online/api-rt/changeip/laun4g452b/x589FCCSBYYAY672XTTVR
```

## 🔄 Jak działa zmiana IP?

1. **Po każdej sesji** (16 portali)
2. Bot wysyła request do API: `GET https://iproxy.online/api-rt/changeip/...`
3. API zwraca: `{"ok":1}`
4. Bot czeka **5 sekund** na zmianę IP
5. Bot sprawdza nowy IP
6. Bot czeka **60 sekund** przed następną sesją (aby mieć pewność że IP się zmieniło)

## ✅ Test Proxy

Przed uruchomieniem bota możesz przetestować proxy:

```bash
python test_proxy.py
```

Test sprawdzi:
- ✓ Czy proxy działa
- ✓ Jakie IP masz przez proxy
- ✓ Czy zmiana IP działa
- ✓ Czy IP faktycznie się zmienia

## 🚀 Uruchomienie bota z proxy

Bot automatycznie:
1. **Inicjalizuje proxy** przy starcie
2. **Testuje połączenie** - jeśli proxy nie działa, bot się nie uruchomi
3. **Używa proxy** we wszystkich przeglądarkach
4. **Zmienia IP** po każdej sesji
5. **Sprawdza IP** przez proxy co 5 minut

### Przykładowy output przy starcie:

```
============================================================
Initializing Proxy Manager...
============================================================

============================================================
                  PROXY CONFIGURATION
============================================================
Host: x340.fxdx.in:13206
Username: softedgedtrailhead104154
Device: tmobile1
Current IP: Not checked yet
============================================================

Testing proxy connection...
✓ Proxy working! IP through proxy: 123.45.67.89
✓ Proxy is working correctly!
```

## 📊 Monitoring IP

Bot wyświetla aktualny IP w statystykach (co 30 sekund):

```
============================================================
                    STATYSTYKI BOTA
============================================================
IP: 123.45.67.89  ← IP przez proxy
Uruchomiony: 2025-10-10 12:00:00
Czas działania: 1:23:45
...
```

## 🔧 Zmiana konfiguracji proxy

Jeśli chcesz zmienić proxy, edytuj plik `proxy_manager.py`, funkcję `create_proxy_manager_from_config()`:

```python
def create_proxy_manager_from_config() -> ProxyManager:
    # Twoje nowe dane proxy
    proxy_host = "nowy.host.com"
    proxy_port = 12345
    proxy_username = "username"
    proxy_password = "password"
    
    # Twój nowy URL zmiany IP
    change_ip_url = "https://..."
    
    return ProxyManager(...)
```

## ⚠️ Troubleshooting

### Proxy nie działa

```
✗ CRITICAL ERROR: Proxy is not working!
Bot cannot run without proxy!
```

**Rozwiązanie:**
1. Sprawdź czy dane proxy są poprawne
2. Sprawdź czy masz internet
3. Sprawdź czy serwis iproxy.online działa
4. Uruchom `python test_proxy.py` aby zdiagnozować problem

### Zmiana IP nie działa

```
⚠ IP change failed - continuing anyway...
```

**Rozwiązanie:**
1. Sprawdź czy URL zmiany IP jest poprawny
2. Sprawdź czy API key jest poprawny
3. Sprawdź logi w `logs/portal_bot.log`

### IP się nie zmienia między sesjami

```
Old IP: 123.45.67.89
New IP: 123.45.67.89
⚠ Warning: IP is the same
```

**Możliwe przyczyny:**
- API potrzebuje więcej czasu na zmianę IP
- Limit zmian IP (sprawdź w panelu iproxy.online)
- Problem z urządzeniem (tmobile1)

## 📈 Statystyki zmian IP

Bot loguje każdą zmianę IP:

```
============================================================
Changing IP after session...
============================================================
Changing IP via iproxy.online API...
✓ IP change successful!
✓ New IP: 98.76.54.32
Waiting 60 seconds before next session (ensuring IP change)...
```

## 🔐 Bezpieczeństwo

- Dane proxy są hardcoded w kodzie (dla prostoty)
- Jeśli udostępniasz kod, usuń dane proxy z `proxy_manager.py`
- Możesz użyć zmiennych środowiskowych zamiast hardcoded wartości

## 📚 API iproxy.online

Dokumentacja: [iproxy.online](https://iproxy.online)

### Endpoint zmiany IP:
```
GET https://iproxy.online/api-rt/changeip/{device}/{api_key}
```

### Response:
```json
{"ok": 1}  // Sukces
{"ok": 0}  // Błąd
```

## 💡 Wskazówki

1. **Czas między sesjami (60s)** jest celowo długi aby mieć pewność że IP się zmieni
2. Jeśli chcesz szybsze sesje, zmniejsz czas w `main_bot.py` ale ryzykujesz że IP nie zmieni się na czas
3. Bot kontynuuje pracę nawet jeśli zmiana IP nie powiedzie się (loguje warning)
4. IP jest sprawdzane przez proxy aby mieć pewność że widzimy właściwe IP

---

**Proxy jest kluczowe dla działania bota!** Bez proxy bot nie uruchomi się.

