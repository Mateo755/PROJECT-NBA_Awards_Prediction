import json
import sys

TEAM_ORDER = {
    "first all-nba team": 0,
    "second all-nba team": 1,
    "third all-nba team": 2,
    "first rookie all-nba team": 3,
    "second rookie all-nba team": 4
}

BONUS_POINTS = {
    2: 5,
    3: 10,
    4: 20,
    5: 40
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def score_prediction(predicted, reference):
    total_score = 0
    breakdown = {}

    # Reverse map to check where each player is in the reference
    player_to_true_team = {}
    for team, players in reference.items():
        for player in players:
            player_to_true_team[player] = team

    for team_name, predicted_players in predicted.items():
        correct_count = 0
        team_score = 0

        for player in predicted_players:
            if player not in player_to_true_team:
                score = 0
            else:
                true_team = player_to_true_team[player]
                diff = abs(TEAM_ORDER[team_name] - TEAM_ORDER[true_team])
                if diff == 0:
                    score = 10
                elif diff == 1:
                    score = 8
                elif diff == 2:
                    score = 6
                else:
                    score = 0

                if diff == 0:
                    correct_count += 1

            team_score += score

        # Bonus for correct picks
        team_score += BONUS_POINTS.get(correct_count, 0)
        breakdown[team_name] = team_score
        total_score += team_score

    return total_score, breakdown

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: python evaluate.py <predictions.json> <ground_truth.json>")
    #     sys.exit(1)

    pred_path = "classification_result_2025.json"
    truth_path = "gt_results/real_results_season2025.json"

    pred_data = load_json(pred_path)
    true_data = load_json(truth_path)

    total, details = score_prediction(pred_data, true_data)

    print(f"Total score: {total}/450")
    for k, v in details.items():
        print(f"{k}: {v} points")
