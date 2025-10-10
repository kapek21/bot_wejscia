"""
Skrypt testowy do sprawdzenia czy bot działa poprawnie
Wykonuje jedną sesję testową
"""

import sys
import os
import logging

# Dodaj katalog do ścieżki
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fingerprint_generator import FingerprintGenerator
from monitoring import MonitoringSystem


def test_fingerprint_generation():
    """Test generowania fingerprintów"""
    print("\n" + "="*60)
    print("TEST 1: Generowanie Fingerprintów")
    print("="*60)
    
    try:
        fingerprint = FingerprintGenerator.generate()
        
        print(f"✓ User Agent: {fingerprint['user_agent']}")
        print(f"✓ Screen: {fingerprint['screen_width']}x{fingerprint['screen_height']}")
        print(f"✓ WebGL Vendor: {fingerprint['webgl_vendor']}")
        print(f"✓ WebGL Renderer: {fingerprint['webgl_renderer'][:60]}...")
        print(f"✓ Hardware Concurrency: {fingerprint['hardware_concurrency']} cores")
        print(f"✓ Device Memory: {fingerprint['device_memory']} GB")
        print(f"✓ Language: {fingerprint['language']}")
        print(f"✓ Timezone: {fingerprint['timezone']}")
        print(f"✓ Canvas Fingerprint: {fingerprint['canvas_fingerprint'][:16]}...")
        
        print("\n✅ Fingerprint generation: OK")
        return True
    except Exception as e:
        print(f"\n❌ Fingerprint generation: FAILED - {e}")
        return False


def test_cookies_generation():
    """Test generowania cookies"""
    print("\n" + "="*60)
    print("TEST 2: Generowanie Cookies")
    print("="*60)
    
    try:
        cookies = FingerprintGenerator.generate_cookies()
        
        print(f"✓ Generated {len(cookies)} cookies:")
        for cookie in cookies:
            print(f"  - {cookie['name']}: {cookie['value'][:40]}...")
        
        print("\n✅ Cookies generation: OK")
        return True
    except Exception as e:
        print(f"\n❌ Cookies generation: FAILED - {e}")
        return False


def test_monitoring_system():
    """Test systemu monitorowania"""
    print("\n" + "="*60)
    print("TEST 3: System Monitorowania")
    print("="*60)
    
    try:
        monitoring = MonitoringSystem(stats_file="test_stats.json")
        
        # Test aktualizacji IP
        print("Sprawdzanie IP...")
        monitoring.update_ip()
        print(f"✓ IP: {monitoring.current_ip}")
        
        # Test liczników
        monitoring.increment_session(success=True)
        monitoring.increment_page_visits(10)
        
        stats = monitoring.get_stats()
        print(f"✓ Sessions: {stats['successful_sessions']}")
        print(f"✓ Page visits: {stats['total_page_visits']}")
        
        # Cleanup
        if os.path.exists("test_stats.json"):
            os.remove("test_stats.json")
        
        print("\n✅ Monitoring system: OK")
        return True
    except Exception as e:
        print(f"\n❌ Monitoring system: FAILED - {e}")
        return False


def test_chrome_options():
    """Test opcji Chrome"""
    print("\n" + "="*60)
    print("TEST 4: Opcje Chrome")
    print("="*60)
    
    try:
        fingerprint = FingerprintGenerator.generate()
        options = FingerprintGenerator.get_chrome_options(fingerprint)
        
        print(f"✓ Arguments count: {len(options.arguments)}")
        print(f"✓ Headless: {'--headless=new' in options.arguments}")
        print(f"✓ User agent set: {any('user-agent=' in arg for arg in options.arguments)}")
        print(f"✓ Automation hidden: {options.experimental_options.get('excludeSwitches')}")
        
        print("\n✅ Chrome options: OK")
        return True
    except Exception as e:
        print(f"\n❌ Chrome options: FAILED - {e}")
        return False


def test_portals_file():
    """Test odczytu pliku z portalami"""
    print("\n" + "="*60)
    print("TEST 5: Plik Portali")
    print("="*60)
    
    try:
        import pandas as pd
        
        excel_paths = [
            '../portale.xlsx',
            'portale.xlsx',
            'E:/gminy2/portale.xlsx'
        ]
        
        excel_file = None
        for path in excel_paths:
            if os.path.exists(path):
                excel_file = path
                break
        
        if not excel_file:
            print("❌ Nie znaleziono pliku portale.xlsx")
            return False
        
        df = pd.read_excel(excel_file, header=None)
        print(f"✓ Znaleziono plik: {excel_file}")
        print(f"✓ Liczba portali: {len(df)}")
        print(f"✓ Pierwsze 3 portale:")
        for idx, row in df.head(3).iterrows():
            print(f"  {idx+1}. {row[0]} - {row[1]}")
        
        if len(df) != 16:
            print(f"\n⚠️  UWAGA: Oczekiwano 16 portali, znaleziono {len(df)}")
        
        print("\n✅ Portals file: OK")
        return True
    except Exception as e:
        print(f"\n❌ Portals file: FAILED - {e}")
        return False


def main():
    """Główna funkcja testowa"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "PORTAL BOT - TESTY" + " "*24 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Uruchom testy
    results.append(("Fingerprint Generation", test_fingerprint_generation()))
    results.append(("Cookies Generation", test_cookies_generation()))
    results.append(("Monitoring System", test_monitoring_system()))
    results.append(("Chrome Options", test_chrome_options()))
    results.append(("Portals File", test_portals_file()))
    
    # Podsumowanie
    print("\n" + "="*60)
    print("PODSUMOWANIE TESTÓW")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name:.<45} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-"*60)
    print(f"Testy zakończone: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 Wszystkie testy przeszły pomyślnie!")
        print("Bot jest gotowy do uruchomienia.")
        print("\nUruchom bota komendą:")
        print("  python main_bot.py")
        print("lub kliknij na:")
        print("  start_bot.bat")
    else:
        print("\n⚠️  Niektóre testy nie powiodły się.")
        print("Sprawdź błędy powyżej i napraw problemy.")
    
    print()


if __name__ == "__main__":
    main()

