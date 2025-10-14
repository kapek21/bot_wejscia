"""
System monitorowania dla bota
Śledzi sesje, wejścia, IP oraz wykrywa zawieszenie
"""

import time
import threading
import requests
import logging
from datetime import datetime
from typing import Dict, Optional
import json
import os


class MonitoringSystem:
    """System monitorowania bota"""
    
    def __init__(self, stats_file: str = "bot_stats.json", proxy_manager=None):
        """
        Inicjalizuje system monitorowania
        
        Args:
            stats_file: Ścieżka do pliku ze statystykami
            proxy_manager: ProxyManager do sprawdzania IP przez proxy
        """
        self.stats_file = stats_file
        self.logger = logging.getLogger("Monitoring")
        self.proxy_manager = proxy_manager
        
        # Statystyki
        self.total_sessions = 0
        self.successful_sessions = 0
        self.failed_sessions = 0
        self.total_page_visits = 0
        self.start_time = datetime.now()
        self.last_activity_time = time.time()
        
        # Statystyki per typ ruchu
        self.traffic_stats = {
            'direct': {'page_visits': 0, 'sessions': 0},
            'google': {'page_visits': 0, 'sessions': 0},
            'facebook': {'page_visits': 0, 'sessions': 0},
            'social': {'page_visits': 0, 'sessions': 0},
        }
        
        # Licznik nieudanych zmian IP
        self.failed_ip_changes = 0
        self.total_ip_changes = 0
        
        # Current IP
        self.current_ip = "Checking..."
        
        # Lock dla thread-safe operations
        self.lock = threading.Lock()
        
        # Wątek monitorujący
        self.monitoring_thread = None
        self.running = False
        
        # Załaduj poprzednie statystyki jeśli istnieją
        self.load_stats()
    
    def load_stats(self):
        """Ładuje statystyki z pliku"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.successful_sessions = data.get('successful_sessions', 0)
                    self.total_page_visits = data.get('total_page_visits', 0)
                    self.traffic_stats = data.get('traffic_stats', self.traffic_stats)
                    self.total_ip_changes = data.get('total_ip_changes', 0)
                    self.logger.info(f"Loaded stats: {self.successful_sessions} sessions, {self.total_page_visits} visits")
        except Exception as e:
            self.logger.warning(f"Could not load stats: {e}")
    
    def save_stats(self):
        """Zapisuje statystyki do pliku (bez locka aby nie blokować)"""
        try:
            # Kopiuj dane BEZ trzymania locka (może być race condition ale nie krytyczne)
            data = {
                'successful_sessions': self.successful_sessions,
                'failed_sessions': self.failed_sessions,
                'total_page_visits': self.total_page_visits,
                'traffic_stats': self.traffic_stats.copy(),
                'total_ip_changes': self.total_ip_changes,
                'failed_ip_changes': self.failed_ip_changes,
                'last_update': datetime.now().isoformat(),
                'current_ip': self.current_ip,
            }
            # Zapisz do pliku BEZ locka
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.warning(f"Could not save stats: {e}")
    
    def update_ip(self):
        """Aktualizuje informację o aktualnym IP (używa proxy jeśli dostępne)"""
        try:
            # Jeśli mamy proxy manager, użyj go (BEZ LOCKA - żeby nie blokować!)
            if self.proxy_manager:
                ip = self.proxy_manager.get_current_ip(use_proxy=True)
                if ip:
                    # Ustaw IP bez locka - to atomic operation
                    self.current_ip = ip
                    self.logger.info(f"Current IP (via proxy): {self.current_ip}")
                    return
            
            # Fallback - bez proxy
            services = [
                'https://api.ipify.org?format=json',
                'https://api.myip.com',
                'https://ifconfig.me/ip',
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        if 'json' in service or 'api' in service:
                            try:
                                data = response.json()
                                self.current_ip = data.get('ip', response.text.strip())
                            except:
                                self.current_ip = response.text.strip()
                        else:
                            self.current_ip = response.text.strip()
                        
                        self.logger.info(f"Current IP: {self.current_ip}")
                        return
                except:
                    continue
            
            self.logger.warning("Could not determine IP address")
            self.current_ip = "Unknown"
            
        except Exception as e:
            self.logger.warning(f"Error updating IP: {e}")
            self.current_ip = "Error"
    
    def mark_activity(self):
        """Oznacza że bot jest aktywny"""
        with self.lock:
            self.last_activity_time = time.time()
    
    def is_hung(self, timeout_seconds: int = 60) -> bool:
        """
        Sprawdza czy bot się zawiesił
        
        Args:
            timeout_seconds: Po ilu sekundach uznać że bot się zawiesił
            
        Returns:
            True jeśli bot się zawiesił
        """
        with self.lock:
            elapsed = time.time() - self.last_activity_time
            return elapsed > timeout_seconds
    
    def increment_session(self, success: bool = True):
        """
        Zwiększa licznik sesji
        
        Args:
            success: Czy sesja zakończyła się sukcesem
        """
        with self.lock:
            self.total_sessions += 1
            if success:
                self.successful_sessions += 1
            else:
                self.failed_sessions += 1
            self.save_stats()
    
    def increment_page_visits(self, count: int = 1, traffic_type: str = None):
        """
        Zwiększa licznik odwiedzonych stron
        
        Args:
            count: Liczba odwiedzonych stron
            traffic_type: Typ ruchu (direct/google/facebook/social)
        """
        with self.lock:
            self.total_page_visits += count
            
            # Zliczaj per typ ruchu
            if traffic_type:
                # Normalizuj typ (google-1 -> google, social-reddit -> social)
                base_type = traffic_type.split('-')[0]
                if base_type in self.traffic_stats:
                    self.traffic_stats[base_type]['page_visits'] += count
    
    def increment_traffic_session(self, traffic_type: str):
        """
        Zwiększa licznik sesji dla typu ruchu
        
        Args:
            traffic_type: Typ ruchu (direct/google/facebook/social)
        """
        with self.lock:
            base_type = traffic_type.split('-')[0]
            if base_type in self.traffic_stats:
                self.traffic_stats[base_type]['sessions'] += 1
        
        # Zapisz statystyki BEZ locka (po zwolnieniu)
        self.save_stats()
    
    def increment_ip_change(self, success: bool = True):
        """
        Zwiększa licznik zmian IP
        
        Args:
            success: Czy zmiana się powiodła
        """
        with self.lock:
            self.total_ip_changes += 1
            if not success:
                self.failed_ip_changes += 1
            self.save_stats()
    
    def get_stats(self) -> Dict:
        """
        Zwraca aktualne statystyki (bez locka - tylko czyta dane)
        
        Returns:
            Słownik ze statystykami
        """
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Usuń mikrosekundy
        
        return {
            'total_sessions': self.total_sessions,
            'successful_sessions': self.successful_sessions,
            'failed_sessions': self.failed_sessions,
            'total_page_visits': self.total_page_visits,
            'current_ip': self.current_ip,
            'uptime': uptime_str,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_activity': time.time() - self.last_activity_time,
        }
    
    def print_stats(self):
        """Wyświetla statystyki w konsoli"""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("STATYSTYKI BOTA".center(60))
        print("="*60)
        print(f"IP: {stats['current_ip']}")
        print(f"Uruchomiony: {stats['start_time']}")
        print(f"Czas działania: {stats['uptime']}")
        print(f"Ostatnia aktywność: {stats['last_activity']:.1f}s temu")
        print("-"*60)
        print(f"Sesje zakończone sukcesem: {stats['successful_sessions']}")
        print(f"Sesje nieudane: {stats['failed_sessions']}")
        print(f"Wszystkie sesje: {stats['total_sessions']}")
        print(f"Odwiedzone strony: {stats['total_page_visits']}")
        print("-"*60)
        print("TYPY RUCHU:")
        for traffic_type, data in self.traffic_stats.items():
            print(f"  {traffic_type.upper():12} - {data['page_visits']:4} page views, {data['sessions']:3} sessions")
        print("-"*60)
        print(f"Zmiany IP: {self.total_ip_changes} (failed: {self.failed_ip_changes})")
        print("="*60 + "\n")
    
    def start_monitoring(self, print_interval: int = 30):
        """
        Uruchamia wątek monitorujący
        
        Args:
            print_interval: Co ile sekund wyświetlać statystyki
        """
        self.running = True
        
        def monitor_loop():
            last_print = time.time()
            
            while self.running:
                # Aktualizuj IP co 5 minut
                if time.time() % 300 < 1:
                    self.update_ip()
                
                # Wyświetl statystyki
                if time.time() - last_print >= print_interval:
                    self.print_stats()
                    last_print = time.time()
                
                time.sleep(1)
        
        # Najpierw zaktualizuj IP
        self.update_ip()
        
        # Uruchom wątek
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info("Monitoring started")
    
    def stop_monitoring(self):
        """Zatrzymuje wątek monitorujący"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.save_stats()
        self.logger.info("Monitoring stopped")

