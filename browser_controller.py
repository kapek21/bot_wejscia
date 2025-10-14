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
    
    def __init__(self, driver: webdriver.Chrome, portal_url: str, portal_name: str, fingerprint: dict, referer: str = None, traffic_type: str = "direct", wojewodztwo: str = None):
        """
        Inicjalizuje kontroler przeglądarki
        
        Args:
            driver: Instancja Selenium WebDriver
            portal_url: URL portalu
            portal_name: Nazwa portalu (województwo)
            fingerprint: Dane fingerprinta dla tej sesji
            referer: HTTP Referer (dla Google organic)
            traffic_type: Typ ruchu (direct/google/facebook/social)
            wojewodztwo: Województwo dla cookies demograficznych
        """
        self.driver = driver
        self.portal_url = portal_url
        self.portal_name = portal_name
        self.fingerprint = fingerprint
        self.referer = referer
        self.traffic_type = traffic_type
        self.wojewodztwo = wojewodztwo if wojewodztwo else "mazowieckie"
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
            
            # Ustaw referer jeśli jest (dla Google organic)
            if self.referer:
                # Najpierw wejdź na referer
                try:
                    self.driver.get(self.referer)
                    time.sleep(random.uniform(1.0, 2.0))
                except:
                    pass
            
            # Wejdź na stronę
            self.driver.get(self.portal_url)
            
            # Wstrzyknij fingerprint
            self.inject_fingerprint_scripts()
            
            # Ustaw cookies demograficzne (wiek 19-50, województwo)
            self.set_demographic_cookies()
            
            # WAŻNE: Czekaj aby strona się załadowała
            time.sleep(random.uniform(2.5, 4.0))
            
            # Akceptuj cookies banner
            self.accept_cookies()
            
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
            # Pobierz losowy link
            article_url = self.get_random_link()
            
            if not article_url:
                self.logger.warning("No article found, skipping article visit")
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
    
    def set_demographic_cookies(self):
        """
        Ustawia cookies demograficzne (wiek 19-50, województwo)
        """
        try:
            from fingerprint_generator import FingerprintGenerator
            
            # Generuj cookies z demografią
            cookies = FingerprintGenerator.generate_cookies(wojewodztwo=self.wojewodztwo)
            
            # Ustaw cookies
            for cookie in cookies:
                try:
                    # Ustaw domenę na aktualną
                    from urllib.parse import urlparse
                    domain = urlparse(self.portal_url).netloc
                    cookie['domain'] = '.' + domain  # Dodaj kropkę na początku
                    
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    # Ignoruj błędy pojedynczych cookies
                    pass
            
            self.logger.info(f"Demographic cookies set (age: 19-50, region: {self.wojewodztwo})")
            
        except Exception as e:
            self.logger.warning(f"Error setting demographic cookies: {e}")
    
    def accept_cookies(self):
        """
        Próbuje kliknąć przycisk akceptacji cookies
        Sprawdza popularne selektory (Accept All, Zgadzam się, itp.)
        """
        try:
            # Lista popularnych selektorów dla przycisków cookies
            selectors = [
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept all')]",
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'zgadzam się')]",
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'akceptuj')]",
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
                "//button[contains(@id, 'accept')]",
                "//button[contains(@class, 'accept')]",
                "//a[contains(@class, 'accept')]",
                "//div[contains(@class, 'cookie')]//button[1]",
            ]
            
            for selector in selectors:
                try:
                    button = self.driver.find_element(By.XPATH, selector)
                    if button.is_displayed():
                        button.click()
                        self.logger.info("Cookies accepted")
                        time.sleep(random.uniform(0.5, 1.5))
                        return
                except:
                    continue
            
            # Jeśli nie znaleziono przycisku - OK, kontynuuj
            
        except Exception as e:
            # Ignoruj błędy - nie wszystkie strony mają cookies banner
            pass
    
    def close(self):
        """Zamyka przeglądarkę"""
        try:
            self.driver.quit()
            self.logger.debug("Browser closed")
        except:
            pass

