"""
Generator słów kluczowych dla portali regionalnych
"""

import random

class KeywordsGenerator:
    """Generuje słowa kluczowe dla portali regionalnych"""
    
    # Szablony słów kluczowych dla portali regionalnych
    KEYWORDS_TEMPLATES = [
        "wiadomości {wojewodztwo}",
        "aktualności {wojewodztwo}",
        "wydarzenia {wojewodztwo}",
        "news {wojewodztwo}",
        "co się dzieje {wojewodztwo}",
        "najnowsze wiadomości {wojewodztwo}",
        "portal {wojewodztwo}",
        "informacje {wojewodztwo}",
        "lokalne wiadomości {wojewodztwo}",
        "region {wojewodztwo}",
        "{wojewodztwo} news",
        "{wojewodztwo} aktualności",
        "{wojewodztwo} dziś",
        "{wojewodztwo} teraz",
        "co nowego {wojewodztwo}",
    ]
    
    # Mapy województw do różnych form
    WOJEWODZTWA_FORMS = {
        'zachodniopomorskie': ['zachodniopomorskie', 'zachodniopomorskim', 'szczecin'],
        'wielkopolskie': ['wielkopolskie', 'wielkopolskim', 'poznań'],
        'warmińsko-mazurskie': ['warmińsko-mazurskie', 'warmińsko-mazurskim', 'olsztyn'],
        'świętokrzyskie': ['świętokrzyskie', 'świętokrzyskim', 'kielce'],
        'śląskie': ['śląskie', 'śląskim', 'katowice', 'śląsk'],
        'pomorskie': ['pomorskie', 'pomorskim', 'gdańsk', 'trójmiasto'],
        'podlaskie': ['podlaskie', 'podlaskiem', 'białystok'],
        'podkarpackie': ['podkarpackie', 'podkarpackim', 'rzeszów'],
        'opolskie': ['opolskie', 'opolskim', 'opole'],
        'mazowieckie': ['mazowieckie', 'mazowieckim', 'warszawa'],
        'małopolskie': ['małopolskie', 'małopolskim', 'kraków', 'małopolska'],
        'lubuskie': ['lubuskie', 'lubuskim', 'gorzów', 'zielona góra'],
        'lubelskie': ['lubelskie', 'lubelskim', 'lublin'],
        'łódzkie': ['łódzkie', 'łódzkim', 'łódź'],
        'kujawsko-pomorskie': ['kujawsko-pomorskie', 'kujawsko-pomorskim', 'bydgoszcz', 'toruń'],
        'dolnośląskie': ['dolnośląskie', 'dolnośląskim', 'wrocław', 'dolny śląsk'],
    }
    
    @staticmethod
    def generate_keywords_for_portal(wojewodztwo: str, count: int = 3) -> list:
        """
        Generuje słowa kluczowe dla portalu wojewódzkiego
        
        Args:
            wojewodztwo: Nazwa województwa
            count: Liczba słów kluczowych do wygenerowania
            
        Returns:
            Lista słów kluczowych
        """
        keywords = []
        wojewodztwo_lower = wojewodztwo.lower().strip()
        
        # Pobierz formy województwa
        forms = KeywordsGenerator.WOJEWODZTWA_FORMS.get(wojewodztwo_lower, [wojewodztwo_lower])
        
        # Generuj keywords
        used_templates = set()
        while len(keywords) < count:
            template = random.choice(KeywordsGenerator.KEYWORDS_TEMPLATES)
            
            # Unikaj powtórzeń
            if template in used_templates and len(used_templates) < len(KeywordsGenerator.KEYWORDS_TEMPLATES):
                continue
            
            used_templates.add(template)
            
            # Wybierz losową formę województwa
            form = random.choice(forms)
            
            # Wygeneruj keyword
            keyword = template.format(wojewodztwo=form)
            keywords.append(keyword)
        
        return keywords
    
    @staticmethod
    def generate_google_referer(keyword: str) -> str:
        """
        Generuje URL referrer z Google dla słowa kluczowego
        
        Args:
            keyword: Słowo kluczowe
            
        Returns:
            URL referrer
        """
        # Encode keyword dla URL
        import urllib.parse
        encoded_keyword = urllib.parse.quote_plus(keyword)
        
        # Różne warianty Google
        google_domains = [
            'https://www.google.pl',
            'https://www.google.com',
        ]
        
        domain = random.choice(google_domains)
        
        return f"{domain}/search?q={encoded_keyword}"
    
    @staticmethod
    def generate_facebook_url(portal_url: str) -> str:
        """Generuje URL z utm_source=facebook"""
        separator = '&' if '?' in portal_url else '?'
        return f"{portal_url}{separator}utm_source=facebook&utm_medium=social"
    
    @staticmethod
    def generate_social_url(portal_url: str) -> str:
        """Generuje URL z random social media"""
        social_sources = ['reddit', 'twitter', 'x', 'linkedin']
        source = random.choice(social_sources)
        
        separator = '&' if '?' in portal_url else '?'
        return f"{portal_url}{separator}utm_source={source}&utm_medium=social"


if __name__ == "__main__":
    # Test
    wojewodztwa = ['zachodniopomorskie', 'małopolskie', 'śląskie']
    
    for woj in wojewodztwa:
        print(f"\n{woj.upper()}:")
        keywords = KeywordsGenerator.generate_keywords_for_portal(woj, 3)
        for i, kw in enumerate(keywords, 1):
            print(f"  {i}. {kw}")
            print(f"     Referer: {KeywordsGenerator.generate_google_referer(kw)}")

