from creating_datasets import get_players_stats, get_teams_stats, get_award_counts, get_rookie_players
from creating_target_data import build_awards_column, get_all_nba_team, get_all_rookie_team
from multi_team_simple_average import resolve_multi_team_simple_average
import pandas as pd


def build_features_dataset(last_season: int, n_seasons: int, return_full=False):
    """
    Tworzy pełny dataset cech (X) i etykiet (y) do klasyfikacji All-NBA / All-Rookie.
    
    :param last_season: ostatni sezon (np. 2024)
    :param n_seasons: liczba sezonów wstecz (np. 5 → 2020–2024)
    :param return_full: jeśli True, zwraca też df_full (X + Player + Team + awards + y)
    :return: X, y 
    """
    all_dfs = []

    for season in range(last_season - n_seasons + 1, last_season + 1):
        print(f"Przetwarzanie sezonu {season}...")

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
        df = resolve_multi_team_simple_average(df_players, df_teams)
        df = df.merge(df_awards_signals, on="Player", how="left")
        df = df.merge(df_rookies[["Player", "is_rookie"]], on="Player", how="left")
        df = df.merge(df_awards_target, on="Player", how="left")

        # === 4. Czyszczenie ===
        df[["potw_count", "potm_count", "rookie_of_month_count", "is_rookie", "target"]] = \
            df[["potw_count", "potm_count", "rookie_of_month_count", "is_rookie", "target"]].fillna(0).astype(int)

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

