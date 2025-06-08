import sys
import pandas as pd
import json
import joblib

# === Load dataset ===
df = pd.read_csv("databases/nba_dataset_2010_2025.csv")

# Drop columns that are not used as model features
drop_cols = ["Player", "Team", "Pos", "season", "target"]

# Convert the multiclass target to a binary label: 1 if player received an award, 0 otherwise
df["target_binary"] = (df["target"] > 0).astype(int)

# Use only features of season 2025 for final prediction
test_mask = df["season"] == 2025

# Extract test data (features only), and also store corresponding player names and rookie status
X_test = df[test_mask].drop(columns=drop_cols)
players_test = df[test_mask]["Player"].reset_index(drop=True)
is_rookie = df[test_mask]["is_rookie"].reset_index(drop=True)

# === Load pre-trained models ===
# Stage 1: Binary classificator, predicts players that have chances for award
model_bin = joblib.load("saved_models/model_bin_stage1.pkl")

# Multi-class classifier (stacked): predicts specific team/award class for selected players
model_stacking = joblib.load("saved_models/model_stacking_stage2.pkl")

# === Stage 1 ===
stage1_preds = model_bin.predict(X_test)


# === Stage 2 ===

# Maps probability array indices (0 to 4) back to class labels (1 to 5)
inverse_class_map = {i: i + 1 for i in range(5)}


# Filter data to include only players that were chosen by the binary model
X_test_stage2 = X_test[stage1_preds == 1].reset_index(drop=True)
players_stage2 = players_test[stage1_preds == 1].reset_index(drop=True)
is_rookie_stage2 = is_rookie[stage1_preds == 1].reset_index(drop=True)

# Predict award/team probabilities for selected players
prob_stage2 = model_stacking.predict_proba(X_test_stage2)

# === Build output DataFrame with predictions ===
# Create DataFrame with probabilities for each award class
df_pred = pd.DataFrame(prob_stage2, columns=[inverse_class_map[i] for i in range(5)])
df_pred["Player"] = players_stage2
df_pred["is_rookie"] = is_rookie_stage2
df_pred["all_nba_score"] = df_pred[[1, 2, 3]].sum(axis=1)

# Custom scoring to select All-NBA players based on summed probabilities between teams
top15 = df_pred.sort_values("all_nba_score", ascending=False).head(15).copy()

# Sort top 15 by probability for each team to get draft rankings
ranks = {
    "first all-nba team": top15.sort_values(1, ascending=False)["Player"].tolist(),
    "second all-nba team": top15.sort_values(2, ascending=False)["Player"].tolist(),
    "third all-nba team": top15.sort_values(3, ascending=False)["Player"].tolist()
}

# Initialize result structure
results = {team: [] for team in ranks}
used_players = set()

# Select 5 unique players for each All-NBA team
while any(len(results[team]) < 5 for team in results):
    for team in ["first all-nba team", "second all-nba team", "third all-nba team"]:
        for player in ranks[team]:
            if player not in used_players:
                results[team].append(player)
                used_players.add(player)
                break



# === Rookie Awards Processing ===
# Filter predictions for rookies only
rookies_df = df_pred[df_pred["is_rookie"] == 1].copy()

# Sort rookies by probabilities for rookie teams
rookie_ranks = {
    "first rookie all-nba team": rookies_df.sort_values(4, ascending=False)["Player"].tolist(),
    "second rookie all-nba team": rookies_df.sort_values(5, ascending=False)["Player"].tolist()
}

# Initialize rookie results
results.update({team: [] for team in rookie_ranks})
used_rookies = set()

# Select 5 unique rookies for each rookie team
while any(len(results[team]) < 5 for team in rookie_ranks):
    for team in ["first rookie all-nba team", "second rookie all-nba team"]:
        for player in rookie_ranks[team]:
            if player not in used_rookies:
                results[team].append(player)
                used_rookies.add(player)
                break



# === Save results to output json file ===
# File path is passed as a command-line argument
output_path = sys.argv[1]
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
