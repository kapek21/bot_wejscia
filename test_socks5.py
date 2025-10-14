"""
Test SOCKS5 proxy
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from proxy_manager import create_proxy_manager_from_config

def main():
    print("\n" + "="*60)
    print("TEST: SOCKS5 Proxy")
    print("="*60)
    
    proxy_manager = create_proxy_manager_from_config()
    
    print(f"\nProxy URL: {proxy_manager.get_proxy_url()}")
    print(f"Proxy Dict: {proxy_manager.get_proxy_dict()}")
    
    print("\n[1/1] Testing SOCKS5 connection...")
    
    if proxy_manager.test_proxy():
        print("\n[OK] SOCKS5 proxy działa!")
        print(f"IP: {proxy_manager.current_ip}")
    else:
        print("\n[FAIL] SOCKS5 proxy nie działa")


if __name__ == "__main__":
    main()


