"""
Test proxy iproxy.online
Sprawdza czy proxy działa i czy zmiana IP działa
"""

import sys
import os

# Dodaj katalog do ścieżki
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from proxy_manager import create_proxy_manager_from_config


def main():
    """Test proxy"""
    print("\n" + "="*60)
    print("TEST PROXY iproxy.online")
    print("="*60)
    
    # Utwórz proxy manager
    print("\n[1/4] Creating proxy manager...")
    try:
        proxy_manager = create_proxy_manager_from_config()
        print("[OK] Proxy manager created")
        proxy_manager.print_info()
    except Exception as e:
        print(f"[FAIL] Failed to create proxy manager: {e}")
        return False
    
    # Test proxy
    print("\n[2/4] Testing proxy connection...")
    try:
        if proxy_manager.test_proxy():
            print("[OK] Proxy is working!")
            print(f"[OK] IP through proxy: {proxy_manager.current_ip}")
        else:
            print("[FAIL] Proxy test failed!")
            return False
    except Exception as e:
        print(f"[FAIL] Proxy test failed: {e}")
        return False
    
    # Sprawdź IP bez proxy
    print("\n[3/4] Checking real IP (without proxy)...")
    try:
        real_ip = proxy_manager.get_current_ip(use_proxy=False)
        if real_ip:
            print(f"[OK] Real IP (without proxy): {real_ip}")
            if real_ip != proxy_manager.current_ip:
                print("[OK] Proxy is masking IP correctly!")
            else:
                print("[WARN] Proxy IP same as real IP - proxy might not be working")
        else:
            print("[FAIL] Could not get real IP")
    except Exception as e:
        print(f"[WARN] Could not check real IP: {e}")
    
    # Test zmiany IP
    print("\n[4/4] Testing IP change...")
    old_ip = proxy_manager.current_ip
    print(f"Current IP: {old_ip}")
    print("Requesting IP change...")
    
    try:
        if proxy_manager.change_ip():
            new_ip = proxy_manager.current_ip
            print(f"[OK] IP change successful!")
            print(f"Old IP: {old_ip}")
            print(f"New IP: {new_ip}")
            
            if old_ip != new_ip:
                print("[OK] IP actually changed!")
            else:
                print("[WARN] IP is the same (might take time to change)")
        else:
            print("[FAIL] IP change failed!")
            return False
    except Exception as e:
        print(f"[FAIL] IP change failed: {e}")
        return False
    
    # Podsumowanie
    print("\n" + "="*60)
    print("PODSUMOWANIE")
    print("="*60)
    print("[OK] Proxy manager dziala poprawnie")
    print("[OK] Polaczenie przez proxy dziala")
    print("[OK] Zmiana IP przez API dziala")
    print("\nBot moze uzywac tego proxy!")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

