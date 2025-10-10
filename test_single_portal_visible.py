"""
Test pojedynczego portalu z WIDOCZNĄ przeglądarką
Sprawdzamy czy Analytics rejestruje ruch
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
    print("TEST POJEDYNCZEGO PORTALU - WIDOCZNA PRZEGLĄDARKA")
    print("="*60)
    print("Sprawdzamy czy Google Analytics rejestruje ruch")
    print("Otworzy się WIDOCZNA przeglądarka Chrome")
    print("Sprawdź Analytics Real-Time podczas testu!")
    print("="*60 + "\n")
    
    # Proxy
    print("[1/5] Inicjalizacja proxy...")
    proxy_manager = create_proxy_manager_from_config()
    if not proxy_manager.test_proxy():
        print("[FAIL] Proxy nie działa!")
        return False
    print(f"[OK] Proxy działa, IP: {proxy_manager.current_ip}")
    
    # Fingerprint
    print("\n[2/5] Generowanie fingerprinta...")
    fingerprint = FingerprintGenerator.generate()
    print(f"[OK] User-Agent: {fingerprint['user_agent'][:60]}...")
    
    # Driver
    print("\n[3/5] Tworzenie przeglądarki...")
    proxy_url = proxy_manager.get_proxy_url()
    options = FingerprintGenerator.get_chrome_options(fingerprint, proxy_url=proxy_url)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    print("[OK] Przeglądarka uruchomiona (WIDOCZNA)")
    
    # Test portal
    portal_url = "https://newszachodniopomorskie.pl"
    portal_name = "zachodniopomorskie"
    
    print(f"\n[4/5] Test portalu: {portal_url}")
    print("Obserwuj Analytics Real-Time teraz!")
    
    try:
        controller = BrowserController(
            driver=driver,
            portal_url=portal_url,
            portal_name=portal_name,
            fingerprint=fingerprint
        )
        
        # Strona główna
        print("\n>>> Odwiedzam stronę główną...")
        controller.visit_homepage(min_time=15, max_time=18)
        print("[OK] Strona główna odwiedzona (15-18s)")
        
        # Artykuł
        print("\n>>> Odwiedzam losowy artykuł...")
        if controller.visit_article(min_time=15, max_time=18):
            print("[OK] Artykuł odwiedzony (15-18s)")
        else:
            print("[WARN] Nie znaleziono artykułu")
        
        print("\n[5/5] Test zakończony!")
        print("\nSprawdź Analytics Real-Time:")
        print("  - Czy widzisz 1 aktywnego użytkownika?")
        print("  - Czy widzisz 2 page views?")
        print("  - Lokalizacja powinna być z proxy!")
        
        print(f"\nIP podczas testu: {proxy_manager.current_ip}")
        print("\nPrzeglądarka zamknie się za 10 sekund...")
        time.sleep(10)
        
        driver.quit()
        print("\n[OK] Test zakończony pomyślnie!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Błąd: {e}")
        driver.quit()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

