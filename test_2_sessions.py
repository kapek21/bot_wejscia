"""
Test 2 sesji z max_workers=1 (64 przeglądarki na sesję)
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from main_bot import PortalBot
import time

def main():
    print("\n" + "="*70)
    print("TEST: 2 sesje po 64 przegladarki (max_workers=1)".center(70))
    print("="*70)
    
    bot = PortalBot(excel_file='portale.xlsx')
    
    # IP przed rozpoczęciem
    print("\n[1/7] Sprawdzam IP poczatkowe...")
    ip_start = bot.proxy_manager.get_current_ip(use_proxy=True)
    print(f"IP poczatkowe: {ip_start}")
    
    # SESJA 1
    print("\n" + "="*70)
    print("SESJA 1 - START (64 przegladarki)".center(70))
    print("="*70)
    time_start_1 = time.time()
    
    success_1 = bot.run_session()
    
    time_end_1 = time.time()
    duration_1 = int(time_end_1 - time_start_1)
    
    print(f"\n[2/7] Sesja 1 zakonczena w {duration_1}s (~{duration_1//60}min)")
    
    # IP po sesji 1
    print("\n[3/7] Sprawdzam IP po sesji 1...")
    ip_after_1 = bot.proxy_manager.get_current_ip(use_proxy=True)
    print(f"IP po sesji 1: {ip_after_1}")
    
    # Sprawdź zmianę IP
    if ip_start != ip_after_1:
        print("[OK] IP ZMIENIL SIE po sesji 1!")
    else:
        print("[WARNING] IP NIE ZMIENIL SIE po sesji 1")
    
    # ZMIANA IP PRZED SESJĄ 2
    print("\n" + "-"*70)
    print("Zmieniam IP przed sesja 2...")
    print("-"*70)
    if bot.proxy_manager.change_ip():
        print("[OK] Komenda zmiany IP wyslana!")
    else:
        print("[WARNING] Zmiana IP nie powiodla sie")
    
    print("Czekam 60s aby IP sie zmienilo...")
    time.sleep(60)
    
    # SESJA 2
    print("\n" + "="*70)
    print("SESJA 2 - START (64 przegladarki)".center(70))
    print("="*70)
    time_start_2 = time.time()
    
    success_2 = bot.run_session()
    
    time_end_2 = time.time()
    duration_2 = int(time_end_2 - time_start_2)
    
    print(f"\n[4/7] Sesja 2 zakonczena w {duration_2}s (~{duration_2//60}min)")
    
    # IP po sesji 2
    print("\n[5/7] Sprawdzam IP po sesji 2...")
    ip_after_2 = bot.proxy_manager.get_current_ip(use_proxy=True)
    print(f"IP po sesji 2: {ip_after_2}")
    
    # Sprawdź zmianę IP
    if ip_after_1 != ip_after_2:
        print("[OK] IP ZMIENIL SIE po sesji 2!")
    else:
        print("[WARNING] IP NIE ZMIENIL SIE po sesji 2")
    
    # Cleanup
    bot.cleanup_drivers()
    
    # STATUS KOŃCOWY
    print("\n" + "="*70)
    print("STATUS KONCOWY".center(70))
    print("="*70)
    
    print(f"\nCzas sesji 1: {duration_1}s (~{duration_1//60}min {duration_1%60}s)")
    print(f"Czas sesji 2: {duration_2}s (~{duration_2//60}min {duration_2%60}s)")
    print(f"Czas calkowity: {duration_1 + duration_2}s (~{(duration_1 + duration_2)//60}min)")
    
    print(f"\nIP poczatkowe:  {ip_start}")
    print(f"IP po sesji 1:  {ip_after_1}  {'[ZMIENIONE]' if ip_start != ip_after_1 else '[TAKIE SAMO]'}")
    print(f"IP po sesji 2:  {ip_after_2}  {'[ZMIENIONE]' if ip_after_1 != ip_after_2 else '[TAKIE SAMO]'}")
    
    # Weryfikacja zmiany IP
    ip_changed_1 = ip_start != ip_after_1
    ip_changed_2 = ip_after_1 != ip_after_2
    
    print("\n" + "="*70)
    
    if ip_changed_1 and ip_changed_2:
        print("[SUKCES] IP zmienia sie pomiedzy sesjami!".center(70))
        print("="*70)
        print("\nBot jest gotowy do uruchomienia w trybie ciaglym!")
        return True
    else:
        print("[PROBLEM] IP nie zmienia sie poprawnie".center(70))
        print("="*70)
        if not ip_changed_1:
            print("\n[X] IP nie zmienil sie po sesji 1")
        if not ip_changed_2:
            print("\n[X] IP nie zmienil sie po sesji 2")
        return False

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1)

