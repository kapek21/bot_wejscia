"""
Test pierwotnego kodu - 16 przeglądarek DIRECT (bez typów ruchu)
Sprawdzamy czy podstawowy scenariusz działa
"""
import sys
sys.path.insert(0, r'E:\gminy2\portale_bot')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fingerprint_generator import FingerprintGenerator
from browser_controller import BrowserController
from proxy_manager import create_proxy_manager_from_config
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time

print("="*60)
print("TEST PIERWOTNEGO SCENARIUSZA - 16 DIRECT")
print("="*60)

# Proxy
pm = create_proxy_manager_from_config()
pm.test_proxy()
print(f"Proxy OK: {pm.current_ip}")

# Portale
df = pd.read_excel(r'E:\gminy2\portale.xlsx', header=None)
portals = []
for idx, row in df.iterrows():
    portals.append({
        'url': f"https://{row[0]}" if not str(row[0]).startswith('http') else str(row[0]),
        'wojewodztwo': str(row[1]),
        'domain': str(row[0])
    })

print(f"Portali: {len(portals)}")

# Fingerprint
fp = FingerprintGenerator.generate()

# Funkcja
def process_portal(portal):
    driver = None
    try:
        proxy_url = pm.get_proxy_url()
        options = FingerprintGenerator.get_chrome_options(fp, proxy_url=proxy_url)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)
        
        controller = BrowserController(
            driver=driver,
            portal_url=portal['url'],
            portal_name=portal['wojewodztwo'],
            fingerprint=fp,
            referer=None,  # BEZ REFERERA
            traffic_type='direct'
        )
        
        controller.visit_homepage(min_time=12, max_time=18)
        controller.visit_article(min_time=14, max_time=20)
        
        driver.quit()
        return True
    except Exception as e:
        print(f"FAIL {portal['wojewodztwo']}: {str(e)[:100]}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return False

# Uruchom 16 równolegle
print("\nUruchamiam 16 przeglądarek HEADLESS...")
print("SPRAWDŹ ANALYTICS - powinny być DIRECT visits!")

success = 0
with ThreadPoolExecutor(max_workers=16) as executor:
    futures = {executor.submit(process_portal, p): p for p in portals}
    for future in as_completed(futures):
        if future.result():
            success += 1
            print(f"OK: {success}/16")

print(f"\n{'='*60}")
print(f"WYNIK: {success}/16 sukces")
print(f"{'='*60}")

