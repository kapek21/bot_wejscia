"""
Moduł do generowania zaawansowanych fingerprintów dla przeglądarek
Generuje realistyczne parametry, które sprawiają, że bot wygląda jak prawdziwy użytkownik
"""

import random
import string
from typing import Dict, List, Tuple


class FingerprintGenerator:
    """Generuje zaawansowane fingerprints dla przeglądarek"""
    
    # Realistyczne User Agents (aktualne wersje Chrome - Desktop i Mobile)
    USER_AGENTS = [
        # Desktop Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        
        # Mobile Android
        "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
        
        # Mobile iOS
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.109 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.109 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/118.0.5993.88 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.85 Mobile/15E148 Safari/604.1",
    ]
    
    # Popularne rozdzielczości ekranu w Polsce (Desktop i Mobile)
    SCREEN_RESOLUTIONS = [
        # Desktop
        (1920, 1080),
        (1366, 768),
        (1536, 864),
        (1440, 900),
        (1600, 900),
        (2560, 1440),
        (1280, 720),
        
        # Mobile Android
        (360, 640),   # Samsung Galaxy S8
        (375, 667),   # iPhone 6/7/8
        (414, 896),   # iPhone 11 Pro Max
        (390, 844),   # iPhone 12/13
        (393, 851),   # iPhone 14 Pro
        (412, 915),   # Samsung Galaxy S21
        (360, 800),   # Samsung Galaxy A52
        (384, 854),   # Samsung Galaxy A72
        
        # Tablet
        (768, 1024),  # iPad
        (810, 1080),  # iPad Air
        (834, 1194),  # iPad Pro 11"
        (1024, 1366), # iPad Pro 12.9"
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
    
    # Platform (Desktop i Mobile)
    PLATFORMS = {
        "desktop": "Win32",
        "mobile_android": "Linux armv8l",
        "mobile_ios": "iPhone",
        "tablet_ios": "iPad"
    }
    
    # Hardware concurrency (liczba rdzeni CPU)
    HARDWARE_CONCURRENCY = {
        "desktop": [4, 6, 8, 12, 16],
        "mobile": [4, 6, 8],
        "tablet": [4, 6, 8]
    }
    
    # Device memory (GB)
    DEVICE_MEMORY = {
        "desktop": [4, 8, 16, 32],
        "mobile": [2, 4, 6, 8],
        "tablet": [4, 6, 8, 16]
    }
    
    @staticmethod
    def generate() -> Dict:
        """
        Generuje kompletny zestaw fingerprintów dla jednej sesji
        Wszystkie przeglądarki w sesji będą używać tego samego fingerprinta
        65% szansy na urządzenie mobilne, 35% na desktop
        """
        # Wybierz User Agent z biasem na mobile (65% mobile, 35% desktop)
        if random.random() < 0.65:  # 65% szansy na mobile
            # Wybierz z mobile user agents
            mobile_agents = [ua for ua in FingerprintGenerator.USER_AGENTS if any(x in ua.lower() for x in ['android', 'iphone', 'ipad'])]
            user_agent = random.choice(mobile_agents)
        else:  # 35% szansy na desktop
            # Wybierz z desktop user agents
            desktop_agents = [ua for ua in FingerprintGenerator.USER_AGENTS if 'windows' in ua.lower()]
            user_agent = random.choice(desktop_agents)
        
        # Określ typ urządzenia na podstawie User Agent
        device_type = FingerprintGenerator._detect_device_type(user_agent)
        
        # Wybierz rozdzielczość ekranu
        width, height = random.choice(FingerprintGenerator.SCREEN_RESOLUTIONS)
        
        # Wybierz język
        language = random.choice(FingerprintGenerator.LANGUAGES)
        
        # Wybierz platformę na podstawie typu urządzenia
        platform = FingerprintGenerator._get_platform_for_device_type(device_type)
        
        # Wybierz WebGL vendor i renderer (tylko dla desktop)
        if device_type == "desktop":
            vendor = random.choice(FingerprintGenerator.WEBGL_VENDORS)
            renderer = random.choice(FingerprintGenerator.WEBGL_RENDERERS[vendor])
        else:
            # Mobile/tablet - uproszczone WebGL
            vendor = "Google Inc. (Qualcomm)"
            renderer = "ANGLE (Qualcomm, Adreno 640 Direct3D11 vs_5_0 ps_5_0)"
        
        # Wybierz hardware concurrency na podstawie typu urządzenia
        hw_type = "desktop" if device_type == "desktop" else ("tablet" if "tablet" in device_type else "mobile")
        hardware_concurrency = random.choice(FingerprintGenerator.HARDWARE_CONCURRENCY[hw_type])
        
        # Wybierz device memory na podstawie typu urządzenia
        device_memory = random.choice(FingerprintGenerator.DEVICE_MEMORY[hw_type])
        
        # Generuj Canvas fingerprint (pseudo-unique)
        canvas_fingerprint = ''.join(random.choices(string.hexdigits.lower(), k=32))
        
        # Generuj AudioContext fingerprint
        audio_fingerprint = round(random.uniform(100, 200), 10)
        
        # Ustaw pixel ratio na podstawie typu urządzenia
        pixel_ratio = 2.0 if device_type in ["mobile_android", "mobile_ios"] else (1.5 if "tablet" in device_type else 1.0)
        
        fingerprint = {
            'user_agent': user_agent,
            'viewport_width': width,
            'viewport_height': height,
            'screen_width': width,
            'screen_height': height,
            'language': language,
            'languages': language.split(','),
            'platform': platform,
            'device_type': device_type,
            'webgl_vendor': vendor,
            'webgl_renderer': renderer,
            'hardware_concurrency': hardware_concurrency,
            'device_memory': device_memory,
            'timezone': FingerprintGenerator.TIMEZONE,
            'timezone_offset': -60,  # UTC+1 (zima) lub -120 dla UTC+2 (lato)
            'canvas_fingerprint': canvas_fingerprint,
            'audio_fingerprint': audio_fingerprint,
            'color_depth': 24,
            'pixel_ratio': pixel_ratio,
            'session_storage': True,
            'local_storage': True,
            'indexed_db': True,
            'cookies_enabled': True,
            'do_not_track': None,  # Większość użytkowników nie ustawia DNT
        }
        
        return fingerprint
    
    @staticmethod
    def _detect_device_type(user_agent: str) -> str:
        """
        Wykrywa typ urządzenia na podstawie User Agent
        
        Args:
            user_agent: User Agent string
            
        Returns:
            Typ urządzenia: desktop, mobile_android, mobile_ios, tablet_ios
        """
        user_agent_lower = user_agent.lower()
        
        if "iphone" in user_agent_lower:
            return "mobile_ios"
        elif "ipad" in user_agent_lower:
            return "tablet_ios"
        elif "android" in user_agent_lower:
            if "mobile" in user_agent_lower:
                return "mobile_android"
            else:
                return "tablet_android"
        else:
            return "desktop"
    
    @staticmethod
    def _get_platform_for_device_type(device_type: str) -> str:
        """
        Zwraca platformę na podstawie typu urządzenia
        
        Args:
            device_type: Typ urządzenia
            
        Returns:
            Platform string
        """
        return FingerprintGenerator.PLATFORMS.get(device_type, "Win32")
    
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
        
        # DEMOGRAFIA - wiek 19-50 lat, województwo, płeć (60% M, 40% K)
        user_age = random.randint(19, 50)
        user_region = wojewodztwo if wojewodztwo else "mazowieckie"
        user_gender = 'M' if random.random() < 0.6 else 'K'  # 60% Mężczyźni, 40% Kobiety
        
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
            # Płeć
            {
                'name': 'user_gender',
                'value': user_gender,
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
        
        # Window size - dostosowane do typu urządzenia
        device_type = fingerprint.get('device_type', 'desktop')
        if device_type in ['mobile_android', 'mobile_ios']:
            # Mobile - małe okno symulujące telefon
            width, height = fingerprint['viewport_width'], fingerprint['viewport_height']
            options.add_argument(f'--window-size={width},{height}')
            options.add_argument(f'--window-position={random.randint(0, 200)},{random.randint(0, 200)}')
        elif 'tablet' in device_type:
            # Tablet - średnie okno
            width, height = fingerprint['viewport_width'], fingerprint['viewport_height']
            options.add_argument(f'--window-size={min(width, 800)},{min(height, 600)}')
            options.add_argument(f'--window-position={random.randint(0, 400)},{random.randint(0, 300)}')
        else:
            # Desktop - małe okna aby nie zasłaniały ekranu
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
        
        # Opcje specyficzne dla urządzeń mobilnych
        if device_type in ['mobile_android', 'mobile_ios']:
            # Mobile-specific options
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-ipc-flooding-protection')
            # Symuluj touch events
            options.add_experimental_option("mobileEmulation", {
                "deviceMetrics": {
                    "width": fingerprint['viewport_width'],
                    "height": fingerprint['viewport_height'],
                    "pixelRatio": fingerprint['pixel_ratio']
                },
                "userAgent": fingerprint['user_agent']
            })
        elif 'tablet' in device_type:
            # Tablet-specific options
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_experimental_option("mobileEmulation", {
                "deviceMetrics": {
                    "width": fingerprint['viewport_width'],
                    "height": fingerprint['viewport_height'],
                    "pixelRatio": fingerprint['pixel_ratio']
                },
                "userAgent": fingerprint['user_agent']
            })
        
        # Ustaw language
        options.add_argument(f'--lang={fingerprint["language"].split(",")[0]}')
        
        return options, seleniumwire_options

