"""
Moduł zarządzania proxy iproxy.online z automatyczną zmianą IP
"""

import requests
import logging
import time
from typing import Optional, Dict


class ProxyManager:
    """Zarządza proxy iproxy.online i zmianą IP"""
    
    def __init__(
        self,
        proxy_host: str,
        proxy_port: int,
        proxy_username: str,
        proxy_password: str,
        api_key_1: str,
        api_key_2: str,
        change_ip_url: str,
        device_name: str = "tmobile1"
    ):
        """
        Inicjalizuje menedżer proxy
        
        Args:
            proxy_host: Host proxy (np. x340.fxdx.in)
            proxy_port: Port proxy (np. 13206)
            proxy_username: Username do proxy
            proxy_password: Hasło do proxy
            api_key_1: Pierwszy klucz API
            api_key_2: Drugi klucz API
            change_ip_url: URL do zmiany IP
            device_name: Nazwa urządzenia (domyślnie tmobile1)
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.api_key_1 = api_key_1
        self.api_key_2 = api_key_2
        self.change_ip_url = change_ip_url
        self.device_name = device_name
        
        self.logger = logging.getLogger("ProxyManager")
        
        # Aktualny IP
        self.current_ip = None
        self.last_ip_change = None
        
    def get_proxy_url(self) -> str:
        """
        Zwraca URL proxy w formacie dla Chrome
        
        Returns:
            URL proxy (http://username:password@host:port)
        """
        return f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
    
    def get_proxy_dict(self) -> Dict[str, str]:
        """
        Zwraca słownik proxy dla requests
        
        Returns:
            Dict z proxy dla http i https
        """
        proxy_url = self.get_proxy_url()
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def change_ip(self, timeout: int = 30) -> bool:
        """
        Zmienia IP przez API iproxy.online
        
        Args:
            timeout: Timeout dla requestu (sekundy)
            
        Returns:
            True jeśli zmiana się powiodła
        """
        try:
            self.logger.info("Changing IP via iproxy.online API...")
            
            # Wywołaj API zmiany IP
            response = requests.get(self.change_ip_url, timeout=timeout)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('ok') == 1:
                        self.logger.info("✓ IP change successful!")
                        self.last_ip_change = time.time()
                        
                        # Poczekaj chwilę aby IP się zmieniło
                        time.sleep(5)
                        
                        # Sprawdź nowy IP
                        new_ip = self.get_current_ip()
                        if new_ip:
                            self.logger.info(f"✓ New IP: {new_ip}")
                            self.current_ip = new_ip
                        
                        return True
                    else:
                        self.logger.error(f"✗ IP change failed: {data}")
                        return False
                except Exception as e:
                    self.logger.error(f"✗ Error parsing response: {e}")
                    return False
            else:
                self.logger.error(f"✗ IP change failed with status {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.logger.error(f"✗ IP change timeout after {timeout}s")
            return False
        except Exception as e:
            self.logger.error(f"✗ Error changing IP: {e}")
            return False
    
    def get_current_ip(self, use_proxy: bool = True) -> Optional[str]:
        """
        Sprawdza aktualny IP
        
        Args:
            use_proxy: Czy użyć proxy (True) czy sprawdzić bez proxy (False)
            
        Returns:
            Aktualny IP lub None jeśli nie udało się sprawdzić
        """
        try:
            services = [
                'https://api.ipify.org?format=json',
                'https://api.myip.com',
                'https://ifconfig.me/ip',
            ]
            
            proxies = self.get_proxy_dict() if use_proxy else None
            
            for service in services:
                try:
                    response = requests.get(service, proxies=proxies, timeout=10)
                    if response.status_code == 200:
                        if 'json' in service or 'api' in service:
                            try:
                                data = response.json()
                                ip = data.get('ip', response.text.strip())
                                return ip
                            except:
                                return response.text.strip()
                        else:
                            return response.text.strip()
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error getting IP: {e}")
            return None
    
    def test_proxy(self) -> bool:
        """
        Testuje czy proxy działa
        
        Returns:
            True jeśli proxy działa poprawnie
        """
        try:
            self.logger.info("Testing proxy connection...")
            
            # Sprawdź IP przez proxy
            proxy_ip = self.get_current_ip(use_proxy=True)
            
            if proxy_ip:
                self.logger.info(f"✓ Proxy working! IP through proxy: {proxy_ip}")
                self.current_ip = proxy_ip
                return True
            else:
                self.logger.error("✗ Proxy test failed - could not get IP")
                return False
                
        except Exception as e:
            self.logger.error(f"✗ Proxy test failed: {e}")
            return False
    
    def get_proxy_info(self) -> Dict:
        """
        Zwraca informacje o proxy
        
        Returns:
            Słownik z informacjami o proxy
        """
        return {
            'proxy_host': self.proxy_host,
            'proxy_port': self.proxy_port,
            'proxy_username': self.proxy_username,
            'device': self.device_name,
            'current_ip': self.current_ip,
            'last_ip_change': self.last_ip_change,
        }
    
    def print_info(self):
        """Wyświetla informacje o proxy"""
        info = self.get_proxy_info()
        
        print("\n" + "="*60)
        print("PROXY CONFIGURATION".center(60))
        print("="*60)
        print(f"Host: {info['proxy_host']}:{info['proxy_port']}")
        print(f"Username: {info['proxy_username']}")
        print(f"Device: {info['device']}")
        print(f"Current IP: {info['current_ip'] or 'Not checked yet'}")
        if info['last_ip_change']:
            print(f"Last IP change: {int(time.time() - info['last_ip_change'])}s ago")
        print("="*60 + "\n")


def create_proxy_manager_from_config() -> ProxyManager:
    """
    Tworzy ProxyManager z konfiguracją iproxy.online
    
    Returns:
        Instancja ProxyManager
    """
    # Parsuj dane proxy
    # Format: http://x340.fxdx.in:13206:softedgedtrailhead104154:jIhUckJtAOt9
    proxy_full = "x340.fxdx.in:13206:softedgedtrailhead104154:jIhUckJtAOt9"
    parts = proxy_full.split(':')
    
    proxy_host = parts[0]
    proxy_port = int(parts[1])
    proxy_username = parts[2]
    proxy_password = parts[3]
    
    # Klucze API
    api_key_1 = "f661d5f96788ccb81588f6d09a35ee22c05976047dc20142a50cdc0898b8b758"
    api_key_2 = "c45b49d179af7d7cbcbf06f0c1a252bdfd8f379b0d362606bb45e96880f6f030"
    
    # URL zmiany IP
    change_ip_url = "https://iproxy.online/api-rt/changeip/laun4g452b/x589FCCSBYYAY672XTTVR"
    
    # Urządzenie
    device_name = "tmobile1"
    
    return ProxyManager(
        proxy_host=proxy_host,
        proxy_port=proxy_port,
        proxy_username=proxy_username,
        proxy_password=proxy_password,
        api_key_1=api_key_1,
        api_key_2=api_key_2,
        change_ip_url=change_ip_url,
        device_name=device_name
    )

