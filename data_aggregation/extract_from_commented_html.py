from bs4 import BeautifulSoup, Comment

def extract_from_commented_html(soup: BeautifulSoup, id_contains: str) -> BeautifulSoup:
    """
    Szuka komentarzy w HTML zawierających dane, np. <div> zakomentowany w <!-- ... -->
    i zwraca zawartość jako parsowalny fragment BeautifulSoup.
    
    :param soup: obiekt BeautifulSoup z requests.get(url).text
    :param id_contains: fragment tekstu identyfikujący interesujący blok np. "players_of_the_week"
    :return: BeautifulSoup z zawartością z komentarza (lub None jeśli nie znaleziono)
    """
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if id_contains in comment:
            return BeautifulSoup(comment, "html.parser")
    
    print(f"Nie znaleziono komentarza zawierającego '{id_contains}'")
    return None