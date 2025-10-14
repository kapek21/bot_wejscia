"""
Test 1 sesji bota (96 browsers) z SOCKS5
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from main_bot import PortalBot

def main():
    print("\n" + "="*60)
    print("TEST: 1 sesja bota (96 browsers) z SOCKS5")
    print("="*60)
    
    bot = PortalBot(excel_file='portale.xlsx')
    
    # Uruchom JEDNĄ sesję
    print("\nUruchamiam sesję...")
    success = bot.run_session()
    
    print("\n" + "="*60)
    if success:
        print("[OK] Sesja zakończona sukcesem!")
    else:
        print("[FAIL] Sesja niepomyślna")
    print("="*60)
    
    # Cleanup
    bot.cleanup_drivers()


if __name__ == "__main__":
    main()


