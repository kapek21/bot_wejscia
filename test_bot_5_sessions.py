"""
Test bota na 5 sesjach
Ograniczona wersja dla testów
"""

import sys
import os

# Dodaj katalog do ścieżki
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_bot import PortalBot
import logging


def main():
    """Test bota na 5 sesjach"""
    print("\n" + "="*60)
    print("TEST BOTA - 5 SESJI")
    print("="*60)
    print("Bot wykona 5 sesji i zatrzyma sie automatycznie")
    print("Kazda sesja:")
    print("  - 16 portali (rownolegle)")
    print("  - Zmiana IP")
    print("  - 60s przerwa")
    print("="*60 + "\n")
    
    # Znajdź plik Excel
    excel_file = None
    
    if os.path.exists('../portale.xlsx'):
        excel_file = '../portale.xlsx'
    elif os.path.exists('portale.xlsx'):
        excel_file = 'portale.xlsx'
    elif os.path.exists('E:/gminy2/portale.xlsx'):
        excel_file = 'E:/gminy2/portale.xlsx'
    else:
        print("ERROR: Could not find portale.xlsx file!")
        return False
    
    try:
        # Utwórz bota
        bot = PortalBot(excel_file=excel_file)
        
        print("\n" + "="*60)
        print("Starting 5-session test...")
        print("="*60 + "\n")
        
        # Uruchom monitoring
        bot.monitoring.start_monitoring(print_interval=30)
        
        # Wykonaj 5 sesji
        MAX_SESSIONS = 5
        
        for session_num in range(1, MAX_SESSIONS + 1):
            print("\n" + "="*60)
            print(f"SESSION {session_num}/{MAX_SESSIONS}")
            print("="*60)
            
            try:
                # Sprawdź czy bot się nie zawiesił
                if bot.monitoring.is_hung(timeout_seconds=60):
                    print("[WARN] Bot hung detected! Restarting session...")
                    bot.cleanup_drivers()
                    bot.monitoring.mark_activity()
                    import time
                    time.sleep(3)
                    continue
                
                # Uruchom sesję
                success = bot.run_session()
                
                if success:
                    print(f"\n[OK] Session {session_num}/{MAX_SESSIONS} completed successfully!")
                else:
                    print(f"\n[WARN] Session {session_num}/{MAX_SESSIONS} had some errors")
                
                # Jeśli to nie ostatnia sesja, zmień IP i czekaj
                if session_num < MAX_SESSIONS:
                    print("\n" + "-"*60)
                    print("Changing IP after session...")
                    print("-"*60)
                    
                    if bot.proxy_manager.change_ip():
                        print("[OK] IP changed successfully!")
                        print(f"New IP: {bot.proxy_manager.current_ip}")
                    else:
                        print("[WARN] IP change failed - continuing anyway...")
                    
                    # Przerwa między sesjami
                    print(f"\nWaiting 60 seconds before session {session_num + 1}...")
                    import time
                    time.sleep(60)
                else:
                    print("\n" + "="*60)
                    print("ALL 5 SESSIONS COMPLETED!")
                    print("="*60)
                    
            except Exception as e:
                print(f"\n[ERROR] Error in session {session_num}: {e}")
                bot.cleanup_drivers()
                bot.monitoring.mark_activity()
                import time
                time.sleep(5)
        
        # Zatrzymaj monitoring i pokaż statystyki
        bot.monitoring.stop_monitoring()
        bot.monitoring.print_stats()
        
        print("\n" + "="*60)
        print("TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Sessions completed: {bot.monitoring.successful_sessions}")
        print(f"Total page visits: {bot.monitoring.total_page_visits}")
        print(f"Final IP: {bot.monitoring.current_ip}")
        print("="*60 + "\n")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n[STOP] Test stopped by user (Ctrl+C)")
        if 'bot' in locals():
            bot.cleanup_drivers()
            bot.monitoring.stop_monitoring()
            bot.monitoring.print_stats()
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        if 'bot' in locals():
            bot.cleanup_drivers()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

