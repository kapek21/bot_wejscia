"""
Główny bot do generowania ruchu na portalach
Obsługuje 16 równoległych przeglądarek z zaawansowanymi fingerprintami
"""

import pandas as pd
import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Importy lokalne
from fingerprint_generator import FingerprintGenerator
from browser_controller import BrowserController
from monitoring import MonitoringSystem
from proxy_manager import create_proxy_manager_from_config
from traffic_types import TrafficMixer


class PortalBot:
    """Główny bot zarządzający ruchem na portalach"""
    
    def __init__(self, excel_file: str = "portale.xlsx"):
        """
        Inicjalizuje bota
        
        Args:
            excel_file: Ścieżka do pliku Excel z portalami
        """
        # Konfiguruj logging
        self.setup_logging()
        self.logger = logging.getLogger("PortalBot")
        
        # PROXY MANAGER - KRYTYCZNE!
        self.logger.info("="*60)
        self.logger.info("Initializing Proxy Manager...")
        self.logger.info("="*60)
        
        self.proxy_manager = create_proxy_manager_from_config()
        self.proxy_manager.print_info()
        
        # Sprawdź czy proxy działa - BEZ PROXY BOT NIE MOŻE DZIAŁAĆ!
        if not self.proxy_manager.test_proxy():
            self.logger.error("="*60)
            self.logger.error("CRITICAL ERROR: Proxy is not working!")
            self.logger.error("Bot cannot run without proxy!")
            self.logger.error("="*60)
            raise RuntimeError("Proxy test failed - bot cannot start without working proxy")
        
        self.logger.info("✓ Proxy is working correctly!")
        
        # Załaduj portale
        self.portals = self.load_portals(excel_file)
        self.logger.info(f"Loaded {len(self.portals)} portals")
        
        # System monitorowania (będzie używał proxy do sprawdzania IP)
        self.monitoring = MonitoringSystem(proxy_manager=self.proxy_manager)
        
        # Kontrola działania
        self.running = True
        self.current_drivers = []
        
    def setup_logging(self):
        """Konfiguruje system logowania"""
        # Utwórz katalog na logi
        os.makedirs('logs', exist_ok=True)
        
        # Format logów
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # Główny logger
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                logging.FileHandler('logs/portal_bot.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Wyłącz verbose logi z Selenium i urllib
        logging.getLogger('selenium').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('WDM').setLevel(logging.WARNING)
    
    def load_portals(self, excel_file: str) -> list:
        """
        Ładuje listę portali z pliku Excel
        
        Args:
            excel_file: Ścieżka do pliku Excel
            
        Returns:
            Lista słowników z danymi portali
        """
        try:
            df = pd.read_excel(excel_file, header=None)
            
            portals = []
            for idx, row in df.iterrows():
                portal_domain = str(row[0]).strip()
                wojewodztwo = str(row[1]).strip()
                
                # Dodaj https:// jeśli nie ma
                if not portal_domain.startswith('http'):
                    portal_url = f"https://{portal_domain}"
                else:
                    portal_url = portal_domain
                
                portals.append({
                    'url': portal_url,
                    'wojewodztwo': wojewodztwo,
                    'domain': portal_domain
                })
            
            return portals
            
        except Exception as e:
            logging.error(f"Error loading portals from Excel: {e}")
            raise
    
    def create_driver(self, fingerprint: dict) -> webdriver.Chrome:
        """
        Tworzy instancję Chrome WebDriver z fingerprintem i proxy
        
        Args:
            fingerprint: Dane fingerprinta
            
        Returns:
            Instancja WebDriver
        """
        try:
            # Pobierz opcje Chrome z fingerprintem i PROXY (ORYGINALNY KOD!)
            proxy_url = self.proxy_manager.get_proxy_url()
            options = FingerprintGenerator.get_chrome_options(fingerprint, proxy_url=proxy_url)
            
            # Utwórz service
            service = Service(ChromeDriverManager().install())
            
            # Utwórz driver (ORYGINALNY KOD!)
            driver = webdriver.Chrome(service=service, options=options)
            
            # Ustaw timeouty
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(15)
            
            return driver
            
        except Exception as e:
            self.logger.error(f"Error creating driver: {e}")
            raise
    
    def process_single_task(self, task: dict, fingerprint: dict) -> bool:
        """
        Przetwarza pojedyncze zadanie (1 przeglądarka z określonym typem ruchu)
        
        Args:
            task: Dane zadania {'url', 'referer', 'traffic_type', 'portal_name', 'wojewodztwo'}
            fingerprint: Dane fingerprinta dla sesji
            
        Returns:
            True jeśli zadanie zakończyło się sukcesem
        """
        driver = None
        try:
            # Utwórz przeglądarkę
            driver = self.create_driver(fingerprint)
            self.current_drivers.append(driver)
            
            # Utwórz kontroler z refererem i typem ruchu
            controller = BrowserController(
                driver=driver,
                portal_url=task['url'],
                portal_name=task['portal_name'],
                fingerprint=fingerprint,
                referer=task.get('referer'),
                traffic_type=task['traffic_type']
            )
            
            # Odwiedź stronę główną (12-18 sekund)
            controller.visit_homepage(min_time=12, max_time=18)
            self.monitoring.increment_page_visits(1, traffic_type=task['traffic_type'])
            
            # Odwiedź artykuł (14-20 sekund)
            article_visited = controller.visit_article(min_time=14, max_time=20)
            if article_visited:
                self.monitoring.increment_page_visits(1, traffic_type=task['traffic_type'])
            
            # Zlicz sesję dla typu ruchu
            self.monitoring.increment_traffic_session(task['traffic_type'])
            
            # Zamknij przeglądarkę
            controller.close()
            
            if driver in self.current_drivers:
                self.current_drivers.remove(driver)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing task {task['portal_name']}-{task['traffic_type']}: {e}")
            
            # Zamknij przeglądarkę w przypadku błędu
            if driver:
                try:
                    driver.quit()
                    if driver in self.current_drivers:
                        self.current_drivers.remove(driver)
                except:
                    pass
            
            return False
    
    def run_session(self) -> bool:
        """
        Uruchamia jedną sesję - 96 przeglądarek (16 direct + 48 google + 16 facebook + 16 social)
        
        Returns:
            True jeśli sesja zakończyła się sukcesem
        """
        try:
            self.logger.info("="*60)
            self.logger.info("Starting new session - 96 browsers")
            self.logger.info("="*60)
            
            # Oznacz aktywność
            self.monitoring.mark_activity()
            
            # Wygeneruj fingerprint dla całej sesji
            fingerprint = FingerprintGenerator.generate()
            self.logger.info(f"Generated fingerprint: {fingerprint['user_agent'][:60]}...")
            
            # Wygeneruj wszystkie zadania (96 = 16 × 6 typów ruchu)
            all_tasks = TrafficMixer.generate_all_traffic(self.portals)
            
            self.logger.info(f"Generated {len(all_tasks)} tasks:")
            # Policz typy
            type_counts = {}
            for task in all_tasks:
                base_type = task['traffic_type'].split('-')[0]
                type_counts[base_type] = type_counts.get(base_type, 0) + 1
            
            for traffic_type, count in type_counts.items():
                self.logger.info(f"  - {traffic_type}: {count} browsers")
            
            # Uruchom w falach (15 na raz - limit iproxy.online)
            # 96 przeglądarek / 15 per batch = 7 batches (6×15 + 6)
            success_count = 0
            batch_size = 15  # LIMIT PROXY: maksymalnie 15 jednocześnie
            
            for batch_num in range(0, len(all_tasks), batch_size):
                batch = all_tasks[batch_num:batch_num + batch_size]
                batch_index = batch_num // batch_size + 1
                total_batches = (len(all_tasks) + batch_size - 1) // batch_size
                
                self.logger.info(f"Starting batch {batch_index}/{total_batches} ({len(batch)} browsers)...")
                
                with ThreadPoolExecutor(max_workers=batch_size) as executor:
                    # Wyślij batch zadań
                    futures = {
                        executor.submit(self.process_single_task, task, fingerprint): task
                        for task in batch
                    }
                    
                    # Czekaj na wyniki
                    for future in as_completed(futures):
                        task = futures[future]
                        try:
                            result = future.result()
                            if result:
                                success_count += 1
                            else:
                                pass  # Błędy logowane w process_single_task
                        except Exception as e:
                            self.logger.error(f"Task {task['portal_name']}-{task['traffic_type']} crashed: {e}")
                        
                        # Oznacz aktywność po każdym zadaniu
                        self.monitoring.mark_activity()
                
                self.logger.info(f"Batch {batch_index}/{total_batches} completed. Total progress: {success_count}/{len(all_tasks)}")
                
                # Krótka pauza między batchami (NIE zmiana IP!)
                if batch_num + batch_size < len(all_tasks):
                    self.logger.info(f"Waiting 3s before next batch...")
                    time.sleep(3)
            
            # Sesja zakończona
            session_success = success_count >= len(all_tasks) * 0.7  # 70% zadań musi się udać
            
            self.monitoring.increment_session(success=session_success)
            
            self.logger.info("-"*60)
            self.logger.info(f"Session completed: {success_count}/{len(all_tasks)} tasks successful")
            self.logger.info("-"*60)
            
            return session_success
            
        except Exception as e:
            self.logger.error(f"Error in session: {e}")
            self.monitoring.increment_session(success=False)
            return False
    
    def cleanup_drivers(self):
        """Zamyka wszystkie otwarte przeglądarki"""
        self.logger.info("Cleaning up browsers...")
        for driver in self.current_drivers:
            try:
                driver.quit()
            except:
                pass
        self.current_drivers.clear()
    
    def run(self):
        """Główna pętla bota"""
        try:
            self.logger.info("="*60)
            self.logger.info("PORTAL BOT STARTED")
            self.logger.info("="*60)
            self.logger.info(f"Portals to visit: {len(self.portals)}")
            self.logger.info("Press Ctrl+C to stop")
            self.logger.info("="*60)
            
            # Uruchom monitoring
            self.monitoring.start_monitoring(print_interval=30)
            
            # Główna pętla
            while self.running:
                try:
                    # Sprawdź czy bot się nie zawiesił (5 minut = 300s)
                    if self.monitoring.is_hung(timeout_seconds=300):
                        self.logger.error("="*60)
                        self.logger.error("BOT HUNG DETECTED (>5 minutes)! RESETTING...")
                        self.logger.error("="*60)
                        self.cleanup_drivers()
                        self.monitoring.mark_activity()
                        time.sleep(5)
                        continue
                    
                    # Uruchom sesję
                    self.run_session()
                    
                    # ZMIANA IP PO KAŻDEJ SESJI - KRYTYCZNE!
                    self.logger.info("="*60)
                    self.logger.info("Changing IP after session...")
                    self.logger.info("="*60)
                    
                    ip_change_success = self.proxy_manager.change_ip()
                    self.monitoring.increment_ip_change(success=ip_change_success)
                    
                    if ip_change_success:
                        self.logger.info("✓ IP changed successfully!")
                        self.logger.info(f"New IP: {self.proxy_manager.current_ip}")
                    else:
                        self.logger.error("="*60)
                        self.logger.error("CRITICAL: IP change FAILED!")
                        self.logger.error("Resetting bot and retrying...")
                        self.logger.error("="*60)
                        self.cleanup_drivers()
                        self.monitoring.mark_activity()
                        time.sleep(10)
                        continue
                    
                    # Pauza między sesjami (60 sekund - aby mieć pewność że IP się zmieniło)
                    self.logger.info("Waiting 60 seconds before next session (ensuring IP change)...")
                    time.sleep(60)
                    
                except KeyboardInterrupt:
                    self.logger.info("\nStopping bot (Ctrl+C pressed)...")
                    self.running = False
                    break
                    
                except Exception as e:
                    self.logger.error(f"Error in main loop: {e}")
                    self.cleanup_drivers()
                    self.monitoring.mark_activity()
                    time.sleep(5)
            
        except KeyboardInterrupt:
            self.logger.info("\nStopping bot...")
            self.running = False
            
        finally:
            # Cleanup
            self.cleanup_drivers()
            self.monitoring.stop_monitoring()
            self.monitoring.print_stats()
            self.logger.info("Bot stopped")


def main():
    """Główna funkcja uruchamiająca bota"""
    # Znajdź plik Excel
    excel_file = None
    
    # Sprawdź w katalogu głównym
    if os.path.exists('../portale.xlsx'):
        excel_file = '../portale.xlsx'
    elif os.path.exists('portale.xlsx'):
        excel_file = 'portale.xlsx'
    elif os.path.exists('E:/gminy2/portale.xlsx'):
        excel_file = 'E:/gminy2/portale.xlsx'
    else:
        print("ERROR: Could not find portale.xlsx file!")
        print("Please make sure the file exists in the project directory.")
        sys.exit(1)
    
    # Utwórz i uruchom bota
    bot = PortalBot(excel_file=excel_file)
    bot.run()


if __name__ == "__main__":
    main()

