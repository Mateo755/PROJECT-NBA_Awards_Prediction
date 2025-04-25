"""
Merge players stats with team stats
Add players awards 
Merge target data or return X and y
make a loop to go through number of seasons 

PARAMS:
sezon końcowy
ilość sezonów
"""

# from creating_datasets import get_players_stats
# import pandas as pd

# df_players = get_players_stats("2020")
# df_players.head()

# from creating_datasets import get_teams_stats
# df_teams = get_teams_stats("2020")
# df_teams.head()

# from creating_datasets import get_award_counts
# df_awards = get_award_counts("2020")

# from creating_datasets import get_rookie_players
# df_rookies = get_rookie_players("2020")
# df_rookies = get_rookie_players("2020")
# df_players["is_rookie"] = df_players["Player"].isin(df_rookies["Player"])   

# from creating_target_data import build_awards_column, get_all_nba_team, get_all_rookie_team

# df_all_nba = get_all_nba_team("2020")
# df_all_rookie = get_all_rookie_team("2020")
# df_awards = build_awards_column(df_all_nba, df_all_rookie)
# print(df_awards.head(25))

from creating_datasets import get_players_stats, get_teams_stats, get_award_counts, get_rookie_players
from creating_target_data import build_awards_column, get_all_nba_team, get_all_rookie_team
import pandas as pd


def build_features_dataset(last_season: int, n_seasons: int, return_full=False):
    """
    Tworzy pełny dataset cech (X) i etykiet (y) do klasyfikacji All-NBA / All-Rookie.
    
    :param last_season: ostatni sezon (np. 2024)
    :param n_seasons: liczba sezonów wstecz (np. 5 → 2020–2024)
    :param return_full: jeśli True, zwraca też df_full (X + Player + Team + awards)
    :return: X, y (i opcjonalnie df_full)
    """
    all_dfs = []

    for season in range(last_season - n_seasons + 1, last_season + 1):
        print(f"📦 Przetwarzanie sezonu {season}...")

        # === 1. Pobierz podstawowe dane ===
        df_players = get_players_stats(str(season))
        df_teams = get_teams_stats(str(season))
        df_awards_signals = get_award_counts(str(season))
        df_rookies = get_rookie_players(str(season))

        df_rookies["is_rookie"] = 1

        # === 2. All-NBA / All-Rookie jako target ===
        df_all_nba = get_all_nba_team(str(season))
        df_all_rookie = get_all_rookie_team(str(season))
        df_awards_target = build_awards_column(df_all_nba, df_all_rookie)

        # === 3. Merge danych cech ===
        df = df_players.merge(df_teams, on="Team", how="left")
        print(f"Merged players and teams {season}")
        df = df.merge(df_awards_signals, on="Player", how="left")
        print(f"Merged players and awards {season}")
        df = df.merge(df_rookies[["Player", "is_rookie"]], on="Player", how="left")
        print(f"Merged players and rookies {season}")
        df = df.merge(df_awards_target, on="Player", how="left")
        print(f"Merged players and awards target {season}")

        print(df.columns)

        # === 4. Czyszczenie ===
        df[["potw_count", "potm_count", "rookie_of_month_count", "is_rookie", "target"]] = \
            df[["potw_count", "potm_count", "rookie_of_month_count", "is_rookie", "target"]].fillna(0).astype(int)
        
        print(f"Cleaned data {season}")

        df["season"] = season
        all_dfs.append(df)

    # === 5. Łączenie wszystkich sezonów ===
    df_full = pd.concat(all_dfs, ignore_index=True)

    # === 6. Przygotowanie X i y ===
    drop_cols = ["Player", "Team", "Pos", "season", "target"]
    X = df_full.drop(columns=drop_cols, errors="ignore")
    y = df_full["target"]

    if return_full:
        return X, y, df_full
    else:
        return X, y


X, y, df_full = build_features_dataset(last_season=2020, n_seasons=1, return_full=True)
