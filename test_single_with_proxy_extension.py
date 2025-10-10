"""
Test pojedynczej przeglądarki headless z proxy extension
"""
import sys
sys.path.insert(0, r'E:\gminy2\portale_bot')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fingerprint_generator import FingerprintGenerator
from proxy_manager import create_proxy_manager_from_config
import time

print("="*60)
print("TEST POJEDYNCZEJ PRZEGLĄDARKI HEADLESS + PROXY EXTENSION")
print("="*60)

# Proxy
pm = create_proxy_manager_from_config()
print(f"Proxy: {pm.proxy_host}:{pm.proxy_port}")

# Fingerprint
fp = FingerprintGenerator.generate()

# Options z proxy
proxy_url = pm.get_proxy_url()
options = FingerprintGenerator.get_chrome_options(fp, proxy_url=proxy_url)

# Service
service = Service(ChromeDriverManager().install())

print("\nUruchamiam Chrome headless z proxy extension...")
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(60)

try:
    # Test 1: Sprawdź IP
    print("\n[Test 1] Sprawdzam IP...")
    driver.get('https://api.ipify.org?format=json')
    time.sleep(2)
    page_source = driver.page_source
    print(f"Odpowiedz: {page_source[:200]}")
    
    # Test 2: Wejdź na portal
    print("\n[Test 2] Wchodze na newslodzkie.pl...")
    driver.get('https://newslodzkie.pl')
    time.sleep(5)
    print(f"Title: {driver.title[:80]}")
    print("SUCCESS!" if driver.title else "FAIL - brak title")
    
    print("\nZamykanie za 5s...")
    time.sleep(5)
    driver.quit()
    print("\nTest zakonczony!")
    
except Exception as e:
    print(f"\nERROR: {e}")
    driver.quit()

