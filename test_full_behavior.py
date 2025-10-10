"""
Test z pełnym zachowaniem użytkownika - scroll, czekanie, artykuł
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fingerprint_generator import FingerprintGenerator
from browser_controller import BrowserController
from proxy_manager import create_proxy_manager_from_config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    print("\n" + "="*60)
    print("TEST PEŁNEGO ZACHOWANIA - newslodzkie.pl")
    print("="*60)
    print("Symulacja prawdziwego użytkownika:")
    print("  - Strona główna: 20-30s ze scrollowaniem")
    print("  - Artykuł: 20-30s ze scrollowaniem")
    print("  - Pełna interakcja")
    print("="*60 + "\n")
    
    # Setup
    print("[1/4] Inicjalizacja...")
    proxy_manager = create_proxy_manager_from_config()
    proxy_manager.test_proxy()
    print(f"IP przez proxy: {proxy_manager.current_ip}")
    
    fingerprint = FingerprintGenerator.generate()
    proxy_url = proxy_manager.get_proxy_url()
    options = FingerprintGenerator.get_chrome_options(fingerprint, proxy_url=proxy_url)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    
    print("[OK] Przeglądarka uruchomiona (WIDOCZNA)")
    
    # Test
    try:
        controller = BrowserController(
            driver=driver,
            portal_url="https://newslodzkie.pl",
            portal_name="lodzkie",
            fingerprint=fingerprint
        )
        
        print("\n[2/4] STRONA GŁÓWNA (30 sekund)...")
        print("SPRAWDŹ ANALYTICS REAL-TIME TERAZ!")
        print("Powinieneś zobaczyć:")
        print("  1. Aktywnego użytkownika")
        print("  2. Page view")
        print("  3. Scrollowanie (jeśli Analytics to trackuje)")
        
        controller.visit_homepage(min_time=25, max_time=30)
        print("[OK] Strona główna - 30s z pełnym scrollowaniem")
        
        print("\n[3/4] ARTYKUŁ (30 sekund)...")
        print("Teraz powinno być:")
        print("  - 1 aktywny użytkownik")
        print("  - 2 page views")
        
        if controller.visit_article(min_time=25, max_time=30):
            print("[OK] Artykuł - 30s z pełnym scrollowaniem")
        else:
            print("[WARN] Brak artykułu, pozostaję na głównej")
            time.sleep(30)
        
        print("\n[4/4] CZEKAM 10s przed zamknięciem...")
        print("Analytics powinien teraz mieć pełne dane!")
        time.sleep(10)
        
        driver.quit()
        
        print("\n" + "="*60)
        print("TEST ZAKOŃCZONY")
        print("="*60)
        print("Sprawdź w Analytics Real-Time:")
        print("  ✓ Czy widzisz użytkownika?")
        print("  ✓ Czy widzisz 2 page views?")
        print("  ✓ Jaka jest lokalizacja? (powinna być z proxy)")
        print(f"\nIP podczas testu: {proxy_manager.current_ip}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        driver.quit()
        return False


if __name__ == "__main__":
    success = main()
    input("\nNaciśnij Enter aby zakończyć...")
    sys.exit(0 if success else 1)

