# 🚀 Szybki Start - Portal Bot

## Instalacja (5 minut)

### 1. Sprawdź Python
```bash
python --version
```
Jeśli nie masz Python, pobierz z: https://www.python.org/downloads/

### 2. Zainstaluj zależności
```bash
cd E:\gminy2\portale_bot
pip install -r requirements.txt
```

### 3. Test proxy (KRYTYCZNE!)
```bash
python test_proxy.py
```
**Bez działającego proxy bot się nie uruchomi!**

### 4. Sprawdź plik Excel
Upewnij się że `E:\gminy2\portale.xlsx` zawiera 16 portali w kolumnach A i B.

## Uruchomienie

### Windows - Najłatwiejsza metoda
Kliknij dwa razy na: **`start_bot.bat`**

### Alternatywnie
```bash
python main_bot.py
```

## Co się dzieje?

1. ✅ Bot testuje proxy iproxy.online (jeśli nie działa - stop!)
2. ✅ Bot wczytuje 16 portali z pliku Excel
3. ✅ Generuje zaawansowany fingerprint
4. ✅ Otwiera 16 przeglądarek Chrome przez proxy (headless - niewidoczne)
5. ✅ Każda przeglądarka:
   - Odwiedza stronę główną portalu (12-18s)
   - Scrolluje naturalnie jak człowiek
   - Wchodzi w losowy artykuł (14-20s)
   - Scrolluje artykuł
   - Zamyka się
6. ✅ Zmienia IP przez API
7. ✅ Pauza 60 sekund (aby IP się zmienił)
8. ✅ Powtarza w nieskończoność z nowym IP

## Statystyki (co 30s)

```
============================================================
                    STATYSTYKI BOTA
============================================================
IP: 123.45.67.89
Uruchomiony: 2025-10-10 12:00:00
Czas działania: 0:15:30
Ostatnia aktywność: 1.2s temu
------------------------------------------------------------
Sesje zakończone sukcesem: 10
Sesje nieudane: 0
Wszystkie sesje: 10
Odwiedzone strony: 320
============================================================
```

## Zatrzymanie

Naciśnij **Ctrl+C** w oknie konsoli.

## Najczęstsze pytania

**Q: Czy zobaczę przeglądarki?**  
A: Nie, działają w trybie headless (niewidoczne).

**Q: Ile to zajmuje RAM?**  
A: Około 2-4 GB podczas sesji (16 przeglądarek).

**Q: Czy muszę mieć proxy?**  
A: TAK! Bot nie działa bez proxy iproxy.online. Jest to obowiązkowe.

**Q: Jak sprawdzić czy działa?**  
A: Patrz na statystyki w konsoli i sprawdź logi w `logs/portal_bot.log`.

**Q: Czy bot się automatycznie restartuje?**  
A: Tak, jeśli zawiesza się na >60s, resetuje sesję.

**Q: Gdzie są zapisane statystyki?**  
A: W pliku `bot_stats.json` w katalogu bota.

## Potrzebujesz pomocy?

Sprawdź logi:
```bash
type logs\portal_bot.log
```

Lub otwórz plik: `E:\gminy2\portale_bot\logs\portal_bot.log`

---

**Gotowe! Bot powinien działać bez problemu. Miłego generowania ruchu! 🎉**

