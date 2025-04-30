from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd


def get_all_nba_team(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}.html"
    res = requests.get(url)
    res.encoding = "utf-8"  # bardzo ważne dla znaków specjalnych!
    soup = BeautifulSoup(res.text, "html.parser")

    # Szukamy komentarzy zawierających dane All-NBA
    comment_html = None
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if "div_all-nba" in comment:
            comment_html = comment
            break

    if comment_html is None:
        print("Nie znaleziono danych All-NBA.")
        return pd.DataFrame()

    section = BeautifulSoup(comment_html, "html.parser")

    all_teams = []

    for team_id, team_num in zip(["all-nba_1", "all-nba_2", "all-nba_3"], [1, 2, 3]):
        team_div = section.find("div", id=team_id)
        if team_div:
            players = [a.text.strip() for a in team_div.find_all("a")]
            for player in players:
                all_teams.append({"Player": player, "all_nba_team": team_num})

    return pd.DataFrame(all_teams)


def get_all_rookie_team(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}.html"
    res = requests.get(url)
    res.encoding = "utf-8"  # bardzo ważne dla znaków specjalnych!
    soup = BeautifulSoup(res.text, "html.parser")
    

    # Szukamy komentarzy zawierających dane All-Rookie
    comment_html = None
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if "div_all-rookie" in comment:
            comment_html = comment
            break

    if comment_html is None:
        print("Nie znaleziono danych All-Rookie.")
        return pd.DataFrame()

    section = BeautifulSoup(comment_html, "html.parser")

    all_teams = []

    for team_id, team_num in zip(["all-rookie_1", "all-rookie_2"], [1, 2]):
        team_div = section.find("div", id=team_id)
        if team_div:
            players = [a.text.strip() for a in team_div.find_all("a")]
            for player in players:
                all_teams.append({"Player": player, "all_rookie_team": team_num})

    return pd.DataFrame(all_teams)





def build_awards_column(df_all_nba, df_all_rookie):
    """Tworzy jedną kolumnę 'awards' dla klasyfikacji All-NBA i All-Rookie"""
    awards = {}

    # All-NBA Teams
    for _, row in df_all_nba.iterrows():
        player = row["Player"].strip()
        team = row["all_nba_team"]
        if player:  
            awards[player] = team  # 1, 2, 3

    # All-Rookie Teams
    for _, row in df_all_rookie.iterrows():
        player = row["Player"].strip()
        team = row["all_rookie_team"]
        if player:
            # Jeśli zawodnik już ma All-NBA, zostaw tamto
            if player not in awards:
                awards[player] = team + 3  # 4, 5

    # Zwróć jako DataFrame
    df_awards = pd.DataFrame.from_dict(awards, orient="index", columns=["target"]).reset_index()
    df_awards = df_awards.rename(columns={"index": "Player"})
    
    return df_awards


