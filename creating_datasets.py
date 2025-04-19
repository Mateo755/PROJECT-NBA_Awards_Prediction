from get_table_by_id import get_table_by_id
import pandas as pd


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
    join_cols = [col for col in ["Player", "Pos", "Age", "Tm"]
                 if col in per_game.columns and col in advanced.columns]

    # 4. Merge
    df = pd.merge(per_game, advanced, on=join_cols, suffixes=('_per_game', '_adv'))

    # 5. Usuń statystyki łączone (TOT)
    if 'Tm' in df.columns:
        df = df[df['Tm'] != 'TOT']

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


    return df.reset_index(drop=True)

