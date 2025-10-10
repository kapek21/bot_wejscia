"""
Test bota na małej próbce - 2 portale × 6 typów = 12 przeglądarek
Sprawdzenie czy wszystko działa przed pełnym testem 96 przeglądarek
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import logging
from fingerprint_generator import FingerprintGenerator
from browser_controller import BrowserController
from monitoring import MonitoringSystem
from proxy_manager import create_proxy_manager_from_config
from traffic_types import TrafficMixer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def main():
    print("\n" + "="*60)
    print("TEST MAŁA PRÓBKA - 2 PORTALE × 6 TYPÓW = 12 PRZEGLĄDAREK")
    print("="*60)
    print("Typy ruchu:")
    print("  - 2× Direct")
    print("  - 6× Google (3 keywords × 2 portale)")
    print("  - 2× Facebook")
    print("  - 2× Social Media")
    print("="*60 + "\n")
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # Proxy
    print("[1/5] Inicjalizacja proxy...")
    proxy_manager = create_proxy_manager_from_config()
    if not proxy_manager.test_proxy():
        print("[FAIL] Proxy nie działa!")
        return False
    print(f"[OK] Proxy: {proxy_manager.current_ip}")
    
    # Wczytaj 2 portale
    print("\n[2/5] Ładowanie portali...")
    df = pd.read_excel('../portale.xlsx', header=None)
    portals = []
    for idx, row in df.head(2).iterrows():  # Tylko pierwsze 2
        portals.append({
            'url': f"https://{row[0]}" if not str(row[0]).startswith('http') else str(row[0]),
            'wojewodztwo': str(row[1]),
            'domain': str(row[0])
        })
    
    print(f"[OK] Załadowano {len(portals)} portale:")
    for p in portals:
        print(f"  - {p['domain']} ({p['wojewodztwo']})")
    
    # Generuj zadania
    print("\n[3/5] Generowanie zadań...")
    all_tasks = TrafficMixer.generate_all_traffic(portals)
    
    type_counts = {}
    for task in all_tasks:
        base_type = task['traffic_type'].split('-')[0]
        type_counts[base_type] = type_counts.get(base_type, 0) + 1
    
    print(f"[OK] Wygenerowano {len(all_tasks)} zadań:")
    for traffic_type, count in type_counts.items():
        print(f"  - {traffic_type}: {count} przeglądarek")
    
    # Monitoring
    monitoring = MonitoringSystem(proxy_manager=proxy_manager, stats_file="test_small_stats.json")
    
    # Fingerprint
    print("\n[4/5] Generowanie fingerprinta...")
    fingerprint = FingerprintGenerator.generate()
    print(f"[OK] {fingerprint['user_agent'][:60]}...")
    
    # Wykonaj zadania
    print("\n[5/5] Uruchamianie 12 przeglądarek (headless)...")
    print("SPRAWDŹ ANALYTICS REAL-TIME TERAZ!")
    print("Powinieneś zobaczyć różne źródła ruchu!\n")
    
    current_drivers = []
    success_count = 0
    
    def create_driver(fp, pm):
        """Tworzy driver"""
        proxy_url = pm.get_proxy_url()
        options = FingerprintGenerator.get_chrome_options(fp, proxy_url=proxy_url)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver
    
    def process_task(task, fp, pm):
        """Przetwarza zadanie"""
        driver = None
        try:
            driver = create_driver(fp, pm)
            
            controller = BrowserController(
                driver=driver,
                portal_url=task['url'],
                portal_name=task['portal_name'],
                fingerprint=fp,
                referer=task.get('referer'),
                traffic_type=task['traffic_type']
            )
            
            # Strona główna
            controller.visit_homepage(min_time=12, max_time=18)
            monitoring.increment_page_visits(1, traffic_type=task['traffic_type'])
            
            # Artykuł
            if controller.visit_article(min_time=14, max_time=20):
                monitoring.increment_page_visits(1, traffic_type=task['traffic_type'])
            
            monitoring.increment_traffic_session(task['traffic_type'])
            
            controller.close()
            return True
            
        except Exception as e:
            print(f"[ERROR] Task {task['portal_name']}-{task['traffic_type']}: {e}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            return False
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(process_task, task, fingerprint, proxy_manager): task
            for task in all_tasks
        }
        
        for future in as_completed(futures):
            task = futures[future]
            try:
                if future.result():
                    success_count += 1
                    print(f"[OK] {success_count}/12 - {task['portal_name']}-{task['traffic_type']}")
            except Exception as e:
                print(f"[FAIL] {task['portal_name']}-{task['traffic_type']}: {e}")
    
    # Podsumowanie
    monitoring.print_stats()
    
    print("\n" + "="*60)
    print("TEST ZAKOŃCZONY")
    print("="*60)
    print(f"Sukces: {success_count}/12 przeglądarek")
    print("\nSPRAWDŹ W ANALYTICS REAL-TIME:")
    print("  - Różne źródła ruchu (Direct, Google, Facebook, Social)")
    print("  - Różne keywords dla Google")
    print("  - Lokalizacja: Mińsk Mazowiecki, T-Mobile")
    print("="*60 + "\n")
    
    # Cleanup
    if os.path.exists("test_small_stats.json"):
        os.remove("test_small_stats.json")
    
    return success_count >= 8  # Minimum 8/12


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

