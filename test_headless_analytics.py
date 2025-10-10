"""
Test headless mode z Analytics
Sprawdzamy czy z obecnymi poprawkami Analytics zadziała w headless
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
    print("TEST HEADLESS MODE + ANALYTICS")
    print("="*60)
    print("Testujemy czy Analytics zadziala w headless chrome")
    print("Z poprawkami:")
    print("  - Wymuszenie ga/gtag events")
    print("  - 2s czekanie przed zamknieciem")
    print("  - Proxy extension")
    print("  - Wylaczone blokowanie cookies")
    print("="*60 + "\n")
    
    # Setup
    print("[1/4] Inicjalizacja proxy...")
    proxy_manager = create_proxy_manager_from_config()
    proxy_manager.test_proxy()
    print(f"[OK] IP przez proxy: {proxy_manager.current_ip}")
    
    print("\n[2/4] Tworzenie headless Chrome...")
    fingerprint = FingerprintGenerator.generate()
    proxy_url = proxy_manager.get_proxy_url()
    options = FingerprintGenerator.get_chrome_options(fingerprint, proxy_url=proxy_url)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    print("[OK] Chrome HEADLESS uruchomiony")
    
    # Test
    try:
        controller = BrowserController(
            driver=driver,
            portal_url="https://newslodzkie.pl",
            portal_name="lodzkie",
            fingerprint=fingerprint
        )
        
        print("\n[3/4] TEST PORTALU newslodzkie.pl...")
        print(">>> Strona glowna (30s)...")
        print("\nSPRAWDZ ANALYTICS REAL-TIME TERAZ!")
        print("Powinienes zobaczyc:")
        print("  - 1 uzytkownika")
        print("  - Page view")
        print("  - Lokalizacja z proxy (Minsk Mazowiecki)")
        
        controller.visit_homepage(min_time=25, max_time=30)
        print("[OK] Strona glowna - 30s")
        
        print("\n>>> Artykul (30s)...")
        if controller.visit_article(min_time=25, max_time=30):
            print("[OK] Artykul - 30s")
        else:
            print("[WARN] Brak artykulu")
        
        print("\n[4/4] Czekam 10s przed zamknieciem...")
        time.sleep(10)
        
        driver.quit()
        
        print("\n" + "="*60)
        print("TEST ZAKONCZONY")
        print("="*60)
        print("\nCZY WIDZISZ W ANALYTICS REAL-TIME:")
        print("  1. Uzytkownika aktywnego?")
        print("  2. 2 page views?")
        print("  3. Lokalizacja z proxy?")
        print(f"\nIP: {proxy_manager.current_ip}")
        print("\nJesli TAK - headless dziala z Analytics!")
        print("Jesli NIE - trzeba uzyc widocznych przegladarek")
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
    input("\nNacisnij Enter aby zakonczyc...")
    sys.exit(0 if success else 1)

