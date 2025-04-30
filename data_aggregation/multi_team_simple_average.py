import numpy as np
import pandas as pd

def resolve_multi_team_simple_average(df_players, df_team_stats, verbose=True):
    """
    Liczy prostą średnią (nieważoną) statystyk drużynowych dla graczy z 2TM/3TM itd.
    """

    df_players["Team"] = df_players["Team"].astype(str)
    resolved_rows = []
    team_stats_cols = df_team_stats.columns.drop("Team")
    league_averages = df_team_stats[team_stats_cols].mean()


    for player, group in df_players.groupby("Player"):

        multi_team_row = group[group["Team"].str.match(r"^\d+TM$")]
        single_team_rows = group[~group["Team"].str.match(r"^\d+TM$")]


        if not multi_team_row.empty:
            if single_team_rows.empty:
                if verbose:
                    print(f"Gracz '{player}' ma '{multi_team_row.iloc[0]['Team']}', ale brak szczegółowych drużyn — pozostawiam bez zmian.")
                resolved_rows.append(multi_team_row.iloc[0])
                continue

            row = multi_team_row.iloc[0].copy()

            for stat in team_stats_cols:
                stat_values = []

                for _, g_row in single_team_rows.iterrows():
                    team = g_row["Team"]
                    team_info = df_team_stats[df_team_stats["Team"] == team]

                    if team_info.empty:
                        if verbose:
                            print(f"Brak danych drużyny '{team}' dla gracza '{player}'")
                        continue

                    stat_value = team_info[stat].values[0]
                    if not pd.isna(stat_value):
                        stat_values.append(stat_value)

                if stat_values:
                    row[stat] = np.mean(stat_values)  # zwykła średnia
                else:
                    row[stat] = league_averages[stat]

            resolved_rows.append(row)
        else:
            for _, single_row in single_team_rows.iterrows():
                single_row = single_row.copy()
                team = single_row["Team"]
                team_info = df_team_stats[df_team_stats["Team"] == team]
                
                if not team_info.empty:
                    for stat in team_stats_cols:
                        if pd.isna(single_row.get(stat)):
                            single_row[stat] = team_info.iloc[0][stat]
                else:
                    if verbose:
                        print(f"Brak danych drużyny '{team}' dla gracza '{player}'")
        
                resolved_rows.append(single_row)
    
    
    return pd.DataFrame(resolved_rows).reset_index(drop=True)