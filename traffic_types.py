"""
Moduł obsługujący różne typy ruchu
- Direct (16 przeglądarek)
- Google Organic (16 przeglądarek - 1 keyword na portal)
- Facebook (16 przeglądarek)
- Social Media (16 przeglądarek - random reddit/twitter/x/linkedin)
"""

import random
from typing import List, Dict
from keywords_generator import KeywordsGenerator


class TrafficType:
    """Klasa reprezentująca typ ruchu"""
    
    def __init__(self, name: str, count: int, portal_url: str, portal_name: str, wojewodztwo: str):
        """
        Args:
            name: Nazwa typu (direct/google/facebook/social)
            count: Liczba przeglądarek
            portal_url: URL portalu
            portal_name: Nazwa portalu
            wojewodztwo: Województwo
        """
        self.name = name
        self.count = count
        self.portal_url = portal_url
        self.portal_name = portal_name
        self.wojewodztwo = wojewodztwo
    
    def generate_urls_and_referers(self) -> List[Dict]:
        """
        Generuje listę URL-i i refererów dla tego typu ruchu
        
        Returns:
            Lista słowników z url, referer, traffic_type
        """
        results = []
        
        if self.name == "direct":
            # Direct - bez referrera
            for i in range(self.count):
                results.append({
                    'url': self.portal_url,
                    'referer': None,
                    'traffic_type': 'direct',
                    'index': i
                })
        
        elif self.name == "google":
            # Google - 1 keyword dla każdego portalu
            keywords = KeywordsGenerator.generate_keywords_for_portal(self.wojewodztwo, count=1)
            
            for i, keyword in enumerate(keywords):
                referer = KeywordsGenerator.generate_google_referer(keyword)
                results.append({
                    'url': self.portal_url,
                    'referer': referer,
                    'traffic_type': f'google-{i+1}',
                    'keyword': keyword,
                    'index': i
                })
        
        elif self.name == "facebook":
            # Facebook - utm_source=facebook
            url_with_utm = KeywordsGenerator.generate_facebook_url(self.portal_url)
            for i in range(self.count):
                results.append({
                    'url': url_with_utm,
                    'referer': 'https://www.facebook.com/',
                    'traffic_type': 'facebook',
                    'index': i
                })
        
        elif self.name == "social":
            # Social Media - random reddit/twitter/x/linkedin
            for i in range(self.count):
                url_with_utm = KeywordsGenerator.generate_social_url(self.portal_url)
                
                # Wybierz random social
                social_referers = {
                    'reddit': 'https://www.reddit.com/',
                    'twitter': 'https://twitter.com/',
                    'x': 'https://x.com/',
                    'linkedin': 'https://www.linkedin.com/'
                }
                
                # Extract source from URL
                import re
                match = re.search(r'utm_source=(\w+)', url_with_utm)
                source = match.group(1) if match else 'reddit'
                
                results.append({
                    'url': url_with_utm,
                    'referer': social_referers.get(source, 'https://www.reddit.com/'),
                    'traffic_type': f'social-{source}',
                    'index': i
                })
        
        return results


class TrafficMixer:
    """Miesza różne typy ruchu dla wszystkich portali"""
    
    @staticmethod
    def generate_all_traffic(portals: List[Dict]) -> List[Dict]:
        """
        Generuje wszystkie typy ruchu dla wszystkich portali
        
        Args:
            portals: Lista portali [{'url': ..., 'wojewodztwo': ..., 'domain': ...}]
            
        Returns:
            Lista zadań do wykonania przez przeglądarki
        """
        all_tasks = []
        
        for portal in portals:
            portal_url = portal['url']
            wojewodztwo = portal['wojewodztwo']
            domain = portal['domain']
            
            # 1. Direct (1 przeglądarka na portal)
            direct = TrafficType("direct", 1, portal_url, domain, wojewodztwo)
            tasks = direct.generate_urls_and_referers()
            for task in tasks:
                task['portal_name'] = domain
                task['wojewodztwo'] = wojewodztwo
            all_tasks.extend(tasks)
            
            # 2. Google (1 przeglądarka na portal - 1 keyword)
            google = TrafficType("google", 1, portal_url, domain, wojewodztwo)
            tasks = google.generate_urls_and_referers()
            for task in tasks:
                task['portal_name'] = domain
                task['wojewodztwo'] = wojewodztwo
            all_tasks.extend(tasks)
            
            # 3. Facebook (1 przeglądarka na portal)
            facebook = TrafficType("facebook", 1, portal_url, domain, wojewodztwo)
            tasks = facebook.generate_urls_and_referers()
            for task in tasks:
                task['portal_name'] = domain
                task['wojewodztwo'] = wojewodztwo
            all_tasks.extend(tasks)
            
            # 4. Social Media (1 przeglądarka na portal)
            social = TrafficType("social", 1, portal_url, domain, wojewodztwo)
            tasks = social.generate_urls_and_referers()
            for task in tasks:
                task['portal_name'] = domain
                task['wojewodztwo'] = wojewodztwo
            all_tasks.extend(tasks)
        
        # Wymieszaj losowo
        random.shuffle(all_tasks)
        
        return all_tasks


if __name__ == "__main__":
    # Test
    portals = [
        {'url': 'https://newslodzkie.pl', 'wojewodztwo': 'łódzkie', 'domain': 'newslodzkie.pl'},
        {'url': 'https://newsmalopolska.pl', 'wojewodztwo': 'małopolskie', 'domain': 'newsmalopolska.pl'},
    ]
    
    tasks = TrafficMixer.generate_all_traffic(portals)
    
    print(f"Total tasks: {len(tasks)}")
    print(f"Expected: {len(portals)} * 6 = {len(portals) * 6}")
    
    # Pokaż przykłady
    print("\nPrzykladowe zadania:")
    for i, task in enumerate(tasks[:10], 1):
        print(f"\n{i}. {task['portal_name']} - {task['traffic_type']}")
        print(f"   URL: {task['url'][:80]}")
        if task['referer']:
            print(f"   Referer: {task['referer'][:80]}")

