def debug_all_table_ids(url):
    import requests
    from bs4 import BeautifulSoup, Comment
    import pandas as pd

    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # sprawdź wszystkie ID w komentarzach
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        soup_comment = BeautifulSoup(c, "html.parser")
        tables = soup_comment.find_all("table")
        for t in tables:
            print("TABLE IN COMMENT:", t.get("id"))

    # sprawdź tabele widoczne bez komentarzy
    for t in soup.find_all("table"):
        print("VISIBLE TABLE:", t.get("id"))