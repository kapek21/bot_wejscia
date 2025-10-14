"""
Moduł do generowania zaawansowanych fingerprintów dla przeglądarek
Generuje realistyczne parametry, które sprawiają, że bot wygląda jak prawdziwy użytkownik
"""

import random
import string
from typing import Dict, List, Tuple


class FingerprintGenerator:
    """Generuje zaawansowane fingerprints dla przeglądarek"""
    
    # Realistyczne User Agents (aktualne wersje Chrome)
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    ]
    
    # Popularne rozdzielczości ekranu w Polsce
    SCREEN_RESOLUTIONS = [
        (1920, 1080),
        (1366, 768),
        (1536, 864),
        (1440, 900),
        (1600, 900),
        (2560, 1440),
        (1280, 720),
    ]
    
    # Popularne języki w Polsce
    LANGUAGES = [
        "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "pl-PL,pl;q=0.9",
        "pl,en-US;q=0.9,en;q=0.8",
    ]
    
    # Timezone dla Polski
    TIMEZONE = "Europe/Warsaw"
    
    # WebGL vendors i renderers (realistyczne dla Windows)
    WEBGL_VENDORS = [
        "Google Inc. (Intel)",
        "Google Inc. (NVIDIA)",
        "Google Inc. (AMD)",
    ]
    
    WEBGL_RENDERERS = {
        "Google Inc. (Intel)": [
            "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)",
        ],
        "Google Inc. (NVIDIA)": [
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)",
        ],
        "Google Inc. (AMD)": [
            "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, Radeon RX 580 Series Direct3D11 vs_5_0 ps_5_0)",
        ]
    }
    
    # Platform
    PLATFORM = "Win32"
    
    # Hardware concurrency (liczba rdzeni CPU)
    HARDWARE_CONCURRENCY = [4, 6, 8, 12, 16]
    
    # Device memory (GB)
    DEVICE_MEMORY = [4, 8, 16, 32]
    
    @staticmethod
    def generate() -> Dict:
        """
        Generuje kompletny zestaw fingerprintów dla jednej sesji
        Wszystkie przeglądarki w sesji będą używać tego samego fingerprinta
        """
        # Wybierz User Agent
        user_agent = random.choice(FingerprintGenerator.USER_AGENTS)
        
        # Wybierz rozdzielczość ekranu
        width, height = random.choice(FingerprintGenerator.SCREEN_RESOLUTIONS)
        
        # Wybierz język
        language = random.choice(FingerprintGenerator.LANGUAGES)
        
        # Wybierz WebGL vendor i renderer
        vendor = random.choice(FingerprintGenerator.WEBGL_VENDORS)
        renderer = random.choice(FingerprintGenerator.WEBGL_RENDERERS[vendor])
        
        # Wybierz hardware concurrency
        hardware_concurrency = random.choice(FingerprintGenerator.HARDWARE_CONCURRENCY)
        
        # Wybierz device memory
        device_memory = random.choice(FingerprintGenerator.DEVICE_MEMORY)
        
        # Generuj Canvas fingerprint (pseudo-unique)
        canvas_fingerprint = ''.join(random.choices(string.hexdigits.lower(), k=32))
        
        # Generuj AudioContext fingerprint
        audio_fingerprint = round(random.uniform(100, 200), 10)
        
        fingerprint = {
            'user_agent': user_agent,
            'viewport_width': width,
            'viewport_height': height,
            'screen_width': width,
            'screen_height': height,
            'language': language,
            'languages': language.split(','),
            'platform': FingerprintGenerator.PLATFORM,
            'webgl_vendor': vendor,
            'webgl_renderer': renderer,
            'hardware_concurrency': hardware_concurrency,
            'device_memory': device_memory,
            'timezone': FingerprintGenerator.TIMEZONE,
            'timezone_offset': -60,  # UTC+1 (zima) lub -120 dla UTC+2 (lato)
            'canvas_fingerprint': canvas_fingerprint,
            'audio_fingerprint': audio_fingerprint,
            'color_depth': 24,
            'pixel_ratio': 1.0,
            'session_storage': True,
            'local_storage': True,
            'indexed_db': True,
            'cookies_enabled': True,
            'do_not_track': None,  # Większość użytkowników nie ustawia DNT
        }
        
        return fingerprint
    
    @staticmethod
    def generate_cookies(wojewodztwo: str = None) -> List[Dict]:
        """
        Generuje realistyczne cookies z demografią użytkownika
        
        Args:
            wojewodztwo: Nazwa województwa (opcjonalne)
        """
        cookies = []
        
        # Generuj losowy identyfikator sesji
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        # Generuj losowy visitor ID (jak Google Analytics)
        visitor_id = f"GA1.2.{random.randint(100000000, 999999999)}.{int(random.random() * 10000000000)}"
        
        # Cookie zgody na cookies (RODO)
        consent_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        
        # DEMOGRAFIA - wiek 19-50 lat, województwo
        user_age = random.randint(19, 50)
        user_region = wojewodztwo if wojewodztwo else "mazowieckie"
        
        cookies_list = [
            {
                'name': '_ga',
                'value': visitor_id,
                'domain': '',  # Zostanie ustawiona dynamicznie
                'path': '/',
                'expires': None,  # Session cookie
            },
            {
                'name': '_gid',
                'value': f"GA1.2.{random.randint(100000000, 999999999)}",
                'domain': '',
                'path': '/',
                'expires': None,
            },
            {
                'name': 'session_id',
                'value': session_id,
                'domain': '',
                'path': '/',
                'expires': None,
            },
            {
                'name': 'cookie_consent',
                'value': consent_value,
                'domain': '',
                'path': '/',
                'expires': None,
            },
            # DEMOGRAFIA - wiek 19-50
            {
                'name': 'user_age',
                'value': str(user_age),
                'domain': '',
                'path': '/',
                'expires': None,
            },
            # Województwo
            {
                'name': 'user_region',
                'value': user_region,
                'domain': '',
                'path': '/',
                'expires': None,
            },
        ]
        
        return cookies_list
    
    @staticmethod
    def get_chrome_options(fingerprint: Dict, proxy_url: str = None):
        """
        Zwraca opcje Chrome skonfigurowane z fingerprintem i proxy (selenium-wire)
        
        Args:
            fingerprint: Dane fingerprinta
            proxy_url: URL proxy w formacie socks5://user:pass@host:port (opcjonalnie)
            
        Returns:
            tuple: (options, seleniumwire_options) - opcje dla Chrome i selenium-wire
        """
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        
        # HEADLESS MODE wyłączony - używamy proxy extension (wymaga GUI)
        # options.add_argument('--headless=new')
        
        # User Agent
        options.add_argument(f'user-agent={fingerprint["user_agent"]}')
        
        # Window size (mniejsze okna aby nie zasłaniały ekranu)
        import random
        options.add_argument(f'--window-size=400,300')
        options.add_argument(f'--window-position={random.randint(0, 1000)},{random.randint(0, 500)}')
        
        # PROXY - KRYTYCZNE! Używamy proxy extension (działa bez headless)
        seleniumwire_options = {}
        if proxy_url:
            # Chrome wymaga rozszerzenia dla proxy z autentykacją lub bez
            import os
            extension_path = os.path.join(os.path.dirname(__file__), 'proxy_extension')
            if os.path.exists(extension_path):
                options.add_argument(f'--load-extension={extension_path}')
                # proxy_extension jest już skonfigurowane w background.js
        
        # Ukryj automatyzację
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Dodatkowe opcje dla stabilności
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        
        # KRYTYCZNE dla Analytics: Pozwól na pełne wykonanie JavaScript
        options.add_argument('--enable-javascript')
        options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
        
        # Nie blokuj third-party cookies (Google Analytics)
        options.add_argument('--disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure')
        
        # Pozwól na tracking
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.cookies": 1,
            "profile.cookie_controls_mode": 0,
        })
        
        # Wyłącz logi
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Symuluj normalne zachowanie
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        # Ustaw language
        options.add_argument(f'--lang={fingerprint["language"].split(",")[0]}')
        
        return options, seleniumwire_options

