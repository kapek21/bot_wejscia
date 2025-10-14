"""
Test 1 przeglądarki headless + proxy
"""
import sys
sys.path.insert(0, r'E:\gminy2\portale_bot')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fingerprint_generator import FingerprintGenerator
from browser_controller import BrowserController
from proxy_manager import create_proxy_manager_from_config
import time

print("="*60)
print("TEST 1 PRZEGLĄDARKI HEADLESS + PROXY")
print("="*60)

pm = create_proxy_manager_from_config()
print(f"Proxy: {pm.current_ip}")

fp = FingerprintGenerator.generate()
proxy_url = pm.get_proxy_url()
options = FingerprintGenerator.get_chrome_options(fp, proxy_url=proxy_url)
service = Service(ChromeDriverManager().install())

print("\nUruchamiam Chrome headless...")
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(60)

try:
    controller = BrowserController(
        driver=driver,
        portal_url='https://newslodzkie.pl',
        portal_name='Lodzkie',
        fingerprint=fp,
        referer=None,
        traffic_type='direct'
    )
    
    print("\nWchodze na homepage...")
    controller.visit_homepage(min_time=5, max_time=7)
    print("[OK] Homepage OK!")
    
    print("\nWchodze na artykul...")
    controller.visit_article(min_time=5, max_time=7)
    print("[OK] Artykul OK!")
    
    driver.quit()
    print("\n[SUCCESS] Test zakończony sukcesem!")
    
except Exception as e:
    print(f"\n[FAIL] Blad: {str(e)[:200]}")
    driver.quit()

