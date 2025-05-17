import pandas as pd
import requests
from bs4 import BeautifulSoup

from .get_table_by_id import get_table_by_id
from .extract_from_commented_html import extract_from_commented_html

TEAM_NAME_MAP = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",  
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS",
    "New Orleans Hornets": "NOH",
    "Charlotte Bobcats": "CHA",
    "New Jersey Nets": "NJN"
}



def get_players_stats(season):
    """Pobiera i łączy per game + advanced statystyki graczy z BR dla wybranego sezonu"""
    base_url = f"https://www.basketball-reference.com/leagues/NBA_{season}"

    # 1. Pobierz per game
    per_game_url = f"{base_url}_per_game.html"
    per_game = get_table_by_id(per_game_url, "per_game_stats")
    per_game = per_game[per_game['Player'] != 'Player'].dropna(subset=['Player']).fillna(0)
    per_game.columns = per_game.columns.str.strip()

    # 2. Pobierz advanced
    advanced_url = f"{base_url}_advanced.html"
    advanced = get_table_by_id(advanced_url, "advanced")
    advanced = advanced[advanced['Player'] != 'Player'].dropna(subset=['Player']).fillna(0)
    advanced.columns = advanced.columns.str.strip()

    # 3. Dopasowanie wspólnych kolumn do merge
    join_cols = [col for col in ["Player", "Pos", "Age", "Team"]
                 if col in per_game.columns and col in advanced.columns]

    # 4. Merge
    df = pd.merge(per_game, advanced, on=join_cols, suffixes=('_per_game', '_adv'))


    # Zamiana nazwy Team_per_game -> Team
    # Usunięcie Team_adv (identyczne co Team_per_game)
    df.rename(columns={'Team_per_game': 'Team'}, inplace=True)
    df.rename(columns={'G_per_game': 'G'}, inplace=True)
    df.rename(columns={'GS_per_game': 'GS'}, inplace=True)
    df.drop(columns=['Team_adv'], errors='ignore', inplace=True)

    df.rename(columns={'MP_per_game': 'MP_avg',
                       'MP_adv': 'MP_total'}, inplace=True)
    
    df.drop(columns=['Rk_per_game', 'Rk_adv'], errors='ignore', inplace=True)
    df.drop(columns=['G_adv', 'GS_adv' ], errors='ignore', inplace=True)

    df.drop(columns=['Awards_per_game', 'Awards_adv'], errors='ignore', inplace=True)
    df.drop(df.index[-1], errors='ignore', inplace=True) # Usunięcie ostatniego wiersza League Average


    return df.reset_index(drop=True)




def get_teams_stats(season):
    """Pobiera i czyści dane z 'Advanced Team Stats' z Basketball Reference"""
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}.html"
    table_id = "advanced-team"

    df = get_table_by_id(url, table_id)
    
    # Spłaszczenie MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]
    else:
        df.columns = df.columns.str.strip()

    # Usuń 'Unnamed:' z kolumn, ale zostaw te z prefixem np. 'Offense Four Factors'
    df.columns = [col if not col.startswith('Unnamed') else col.split(' ')[-1] for col in df.columns]

    # Usuń kolumny gdzie wszystkie wartości są NaN (kolumny techniczne)
    null_cols = df.columns[df.isna().all()]
    df.drop(columns=null_cols, inplace=True, errors='ignore')

    df.drop(columns=[
    'Rk', 'Age', 'PW', 'PL', 'Arena', 'Attend.', 'Attend./G'
    ], errors='ignore', inplace=True)

    # Automatyczne wykrycie kolumny z nazwą drużyny
    team_col = "Team" if "Team" in df.columns else "Tm"

    df = df[df[team_col] != "League Average"]
    df[team_col] = df[team_col].str.replace("*", "", regex=False)
    df.rename(columns={team_col: "Team"}, inplace=True)
    df["Team"] = df["Team"].map(TEAM_NAME_MAP)



    return df



def get_award_counts(season):

    season_int = int(season)
    season_label = f"{season_int - 1}-{str(season_int)[-2:]}"  # np. 2019-20

    url = "https://www.basketball-reference.com/leagues/NBA_2020.html"
    res = requests.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, "html.parser")

    section = extract_from_commented_html(soup, "players_of_the_week_and_month")
    if section is None:
        print(f"Nie znaleziono sekcji 'players_of_the_week_and_month' w sezonie {season_label}.")
        return pd.DataFrame()

    potw, potm, rotm = [], [], []
    current_award = ""

    for tag in section.find_all(["h3", "a"]):
        text = tag.get_text().lower()
        if tag.name == "h3":
            if "players of the week" in text:
                current_award = "potw"
            elif "players of the month" in text and "rookie" not in text:
                current_award = "potm"
            elif "rookies of the month" in text:
                current_award = "rotm"
            else:
                current_award = ""

        elif tag.name == "a":
            player = text.title()
            if current_award == "potw":
                potw.append(player)
            elif current_award == "potm":
                potm.append(player)
            elif current_award == "rotm":
                rotm.append(player)

    #print(f"Znaleziono {len(potw)} graczy tygodnia, {len(potm)} graczy miesiąca i {len(rotm)} debiutantów miesiąca w sezonie {season_label}.")
    df = pd.DataFrame()
    df["Player"] = list(set(potw + potm + rotm))
    df["potw_count"] = df["Player"].apply(lambda x: potw.count(x))
    df["potm_count"] = df["Player"].apply(lambda x: potm.count(x))
    df["rookie_of_month_count"] = df["Player"].apply(lambda x: rotm.count(x))

    return df


def get_rookie_players(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_rookies.html"
    df = get_table_by_id(url, "rookies")

    # Spłaszczenie MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]
    else:
        df.columns = df.columns.str.strip()
    df.columns

    # Usuń 'Unnamed:' z kolumn, ale zostaw te z prefixem np. 'Offense Four Factors'
    df.columns = [col if not col.startswith('Unnamed') else col.split(' ')[-1] for col in df.columns]


    # Zostaw tylko kolumnę Player i usuń duplikaty
    df = df[["Player"]].copy()
    df["Player"] = df["Player"].str.strip()
    df = df.drop_duplicates().reset_index(drop=True)

    return df

