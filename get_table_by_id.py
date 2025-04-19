def get_table_by_id(url, table_id):
    """Pobiera tabelę z Basketball Reference po ID, także jeśli jest ukryta w komentarzach"""
    import requests
    from bs4 import BeautifulSoup, Comment
    import pandas as pd

    # Pobieramy stronę
    # i parsujemy HTML
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Szukamy tabeli wewnątrz komentarzy
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        if table_id in c:
            comment_soup = BeautifulSoup(c, "html.parser")
            table = comment_soup.find("table", {"id": table_id})
            if table:
                return pd.read_html(str(table))[0]

    table = soup.find("table", {"id": table_id})
    if table:
        return pd.read_html(str(table))[0]

    raise ValueError(f"❌ Table with id '{table_id}' not found at {url}")