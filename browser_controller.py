"""
Moduł kontrolujący przeglądarkę z realistycznym zachowaniem użytkownika
"""

import time
import random
import logging
from typing import List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import math


class BrowserController:
    """Kontroluje przeglądarkę symulując zachowanie człowieka"""
    
    def __init__(self, driver: webdriver.Chrome, portal_url: str, portal_name: str, fingerprint: dict, referer: str = None, traffic_type: str = "direct"):
        """
        Inicjalizuje kontroler przeglądarki
        
        Args:
            driver: Instancja Selenium WebDriver
            portal_url: URL portalu
            portal_name: Nazwa portalu (województwo)
            fingerprint: Dane fingerprinta dla tej sesji
            referer: HTTP Referer (dla Google organic)
            traffic_type: Typ ruchu (direct/google/facebook/social)
        """
        self.driver = driver
        self.portal_url = portal_url
        self.portal_name = portal_name
        self.fingerprint = fingerprint
        self.referer = referer
        self.traffic_type = traffic_type
        self.logger = logging.getLogger(f"Browser-{portal_name}-{traffic_type}")
        
    def inject_fingerprint_scripts(self):
        """Wstrzykuje skrypty JavaScript aby zmienić fingerprint przeglądarki"""
        try:
            # Ukryj webdriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Zmień WebGL vendor i renderer
            webgl_script = f"""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return '{self.fingerprint["webgl_vendor"]}';
                }}
                if (parameter === 37446) {{
                    return '{self.fingerprint["webgl_renderer"]}';
                }}
                return getParameter.apply(this, arguments);
            }};
            """
            self.driver.execute_script(webgl_script)
            
            # Zmień hardware concurrency
            self.driver.execute_script(
                f"Object.defineProperty(navigator, 'hardwareConcurrency', {{get: () => {self.fingerprint['hardware_concurrency']}}})"
            )
            
            # Zmień device memory
            self.driver.execute_script(
                f"Object.defineProperty(navigator, 'deviceMemory', {{get: () => {self.fingerprint['device_memory']}}})"
            )
            
            # Zmień languages
            languages_str = str(self.fingerprint['languages']).replace("'", '"')
            self.driver.execute_script(
                f"Object.defineProperty(navigator, 'languages', {{get: () => {languages_str}}})"
            )
            
            # Zmień platform
            self.driver.execute_script(
                f"Object.defineProperty(navigator, 'platform', {{get: () => '{self.fingerprint['platform']}' }})"
            )
            
            # Usuń ślady automatyzacji
            self.driver.execute_script("""
                delete navigator.__proto__.webdriver;
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                window.chrome = {
                    runtime: {}
                };
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({state: 'prompt'})
                    })
                });
            """)
            
            self.logger.debug("Fingerprint scripts injected successfully")
            
        except Exception as e:
            self.logger.warning(f"Error injecting fingerprint scripts: {e}")
    
    def human_like_scroll(self, duration_seconds: float):
        """
        Scrolluje stronę w sposób imitujący człowieka
        
        Args:
            duration_seconds: Ile czasu ma trwać scrollowanie
        """
        try:
            # Pobierz wysokość strony
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            if page_height <= viewport_height:
                # Strona jest za krótka do scrollowania
                time.sleep(duration_seconds)
                return
            
            start_time = time.time()
            current_position = 0
            
            # Oblicz ile scrolli wykonać
            num_scrolls = random.randint(3, 8)
            
            while time.time() - start_time < duration_seconds:
                # Losowy scroll w dół
                scroll_amount = random.randint(100, 400)
                new_position = min(current_position + scroll_amount, page_height - viewport_height)
                
                # Płynny scroll (easing)
                steps = random.randint(3, 8)
                for step in range(steps):
                    progress = (step + 1) / steps
                    # Easing function (ease-out)
                    eased_progress = 1 - math.pow(1 - progress, 3)
                    scroll_to = current_position + (new_position - current_position) * eased_progress
                    
                    self.driver.execute_script(f"window.scrollTo(0, {scroll_to});")
                    time.sleep(random.uniform(0.05, 0.15))
                
                current_position = new_position
                
                # Czasami przewiń trochę do góry (naturalne zachowanie)
                if random.random() < 0.3 and current_position > 200:
                    scroll_back = random.randint(50, 150)
                    current_position = max(0, current_position - scroll_back)
                    self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                
                # Pauza między scrollami
                pause_time = random.uniform(0.5, 2.0)
                time.sleep(pause_time)
                
                # Jeśli dotarliśmy do końca strony
                if current_position >= page_height - viewport_height - 100:
                    # Czasami przewiń na górę i zacznij od nowa
                    if random.random() < 0.4:
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        current_position = 0
                    else:
                        break
            
            # Doczekaj pozostałego czasu
            elapsed = time.time() - start_time
            if elapsed < duration_seconds:
                time.sleep(duration_seconds - elapsed)
            
            self.logger.debug(f"Scrolled for {duration_seconds} seconds")
            
        except Exception as e:
            self.logger.warning(f"Error during scrolling: {e}")
            time.sleep(duration_seconds)
    
    def get_random_link(self) -> str:
        """
        Pobiera losowy link artykułu ze strony
        
        Returns:
            URL losowego artykułu lub None jeśli nie znaleziono
        """
        try:
            # Poczekaj aż strona się załaduje
            time.sleep(2)
            
            # Szukaj linków do artykułów (różne selektory)
            selectors = [
                "a[href*='news']",
                "article a",
                ".article a",
                ".post a",
                ".entry a",
                "a[href*='artykul']",
                "a[href*='article']",
                "main a",
                ".content a",
            ]
            
            links = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute('href')
                        if href and href.startswith('http') and self.portal_url.replace('https://', '').replace('http://', '').split('/')[0] in href:
                            # Sprawdź czy to nie link do strony głównej
                            if href != self.portal_url and href != self.portal_url + '/':
                                links.append(href)
                except:
                    continue
            
            # Usuń duplikaty
            links = list(set(links))
            
            if links:
                selected_link = random.choice(links)
                self.logger.debug(f"Found {len(links)} links, selected: {selected_link[:100]}")
                return selected_link
            else:
                self.logger.warning("No article links found")
                return None
                
        except Exception as e:
            self.logger.warning(f"Error getting random link: {e}")
            return None
    
    def visit_homepage(self, min_time: int = 12, max_time: int = 18):
        """
        Odwiedza stronę główną portalu i scrolluje ją
        
        Args:
            min_time: Minimalny czas na stronie (sekundy)
            max_time: Maksymalny czas na stronie (sekundy)
        """
        try:
            self.logger.info(f"Visiting homepage: {self.portal_url} (type: {self.traffic_type})")
            
            # Ustaw referer w headerze (bez faktycznego wejścia - oszczędza requesty)
            if self.referer:
                try:
                    # Ustaw referer przez JavaScript przed wejściem na stronę
                    self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': {'Referer': self.referer}})
                except:
                    # Fallback - niektóre wersje Chrome nie wspierają CDP
                    pass
            
            # Wejdź na stronę
            self.driver.get(self.portal_url)
            
            # Wstrzyknij fingerprint
            self.inject_fingerprint_scripts()
            
            # WAŻNE: Czekaj aby Google Analytics się załadował
            time.sleep(random.uniform(2.5, 4.0))
            
            # Wymuś wykonanie pending analytics events
            try:
                self.driver.execute_script("""
                    // Force flush Google Analytics
                    if (typeof ga !== 'undefined') {
                        ga('send', 'pageview');
                    }
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'page_view');
                    }
                    if (typeof _gaq !== 'undefined') {
                        _gaq.push(['_trackPageview']);
                    }
                    // Google Tag Manager
                    if (typeof dataLayer !== 'undefined') {
                        dataLayer.push({'event': 'pageview'});
                    }
                """)
            except:
                pass
            
            # Losowy czas na stronie
            stay_time = random.uniform(min_time, max_time)
            
            # Scrolluj stronę
            self.human_like_scroll(stay_time)
            
            # KRYTYCZNE: Dodatkowe czekanie aby analytics wysłał dane przed zamknięciem
            time.sleep(2.0)
            
            self.logger.info(f"Stayed on homepage for {stay_time:.1f} seconds")
            
        except Exception as e:
            self.logger.error(f"Error visiting homepage: {e}")
            raise
    
    def visit_article(self, min_time: int = 14, max_time: int = 20):
        """
        Odwiedza losowy artykuł i scrolluje go
        
        Args:
            min_time: Minimalny czas na stronie (sekundy)
            max_time: Maksymalny czas na stronie (sekundy)
        
        Returns:
            True jeśli udało się odwiedzić artykuł, False w przeciwnym razie
        """
        try:
            # Pobierz losowy link (z cache stron głównych dla przyspieszenia)
            article_url = self.get_random_link()
            
            if not article_url:
                # Jeśli nie znaleziono artykułu, zostań na głównej dłużej
                time.sleep(10)
                return False
            
            self.logger.info(f"Visiting article: {article_url[:100]}")
            
            # Wejdź na artykuł
            self.driver.get(article_url)
            
            # Wstrzyknij fingerprint (na wszelki wypadek)
            self.inject_fingerprint_scripts()
            
            # WAŻNE: Czekaj aby Google Analytics się załadował
            time.sleep(random.uniform(2.5, 4.0))
            
            # Wymuś wykonanie pending analytics events
            try:
                self.driver.execute_script("""
                    // Force flush Google Analytics
                    if (typeof ga !== 'undefined') {
                        ga('send', 'pageview');
                    }
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'page_view');
                    }
                    if (typeof _gaq !== 'undefined') {
                        _gaq.push(['_trackPageview']);
                    }
                    // Google Tag Manager
                    if (typeof dataLayer !== 'undefined') {
                        dataLayer.push({'event': 'pageview'});
                    }
                """)
            except:
                pass
            
            # Losowy czas na stronie
            stay_time = random.uniform(min_time, max_time)
            
            # Scrolluj artykuł
            self.human_like_scroll(stay_time)
            
            # KRYTYCZNE: Dodatkowe czekanie aby analytics wysłał dane przed zamknięciem
            time.sleep(2.0)
            
            self.logger.info(f"Stayed on article for {stay_time:.1f} seconds")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error visiting article: {e}")
            return False
    
    def close(self):
        """Zamyka przeglądarkę"""
        try:
            self.driver.quit()
            self.logger.debug("Browser closed")
        except:
            pass

