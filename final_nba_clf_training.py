import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight

# === Load dataset ===
df = pd.read_csv("databases/nba_dataset_2010_2025.csv")

# Drop columns that are not used as model features
drop_cols = ["Player", "Team", "Pos", "season", "target"]

# Convert the multiclass target to a binary label: 1 if player received an award, 0 otherwise
df["target_binary"] = (df["target"] > 0).astype(int)

# Use only seasons before 2025 for training
train_mask = df["season"] < 2025

# Define feature matrix (X) and labels (y)
X_train = df[train_mask].drop(columns=drop_cols)
y_train_bin = df[train_mask]["target_binary"]      # Binary labels (award vs no award)
y_train_full = df[train_mask]["target"]            # Full multiclass labels (award category 1–5), 0 if no award


# === Stage 1: Binary classification, predicted players that have chances for award ===
model_bin = XGBClassifier(
    objective="binary:logistic", 
    eval_metric="logloss", 
    random_state=42
)

# Compute sample weights to balance classes in the binary classification task
sample_weight = compute_sample_weight("balanced", y_train_bin)

# Train the binary model
model_bin.fit(X_train, y_train_bin, sample_weight=sample_weight)


# === Stage 2: Stacking model for multiclass award type prediction ===

# The binary model acts as a filtering mechanism, identifying players with realistic potential for awards. 
# Once this potential is confirmed, the stacking classifier estimates the most probable specific award class (from five categories). 
# At this stage, we no longer consider the “no award” class — all inputs are assumed to be award-worthy.

# Map award categories from [1–5] to [0–4]
# This is needed because scikit-learn's predict_proba returns probabilities 
# in array index form: [class_0_prob, class_1_prob, ..., class_n_prob]
class_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}

# Filter data to include only players that were chosen by the binary model
X_train_stage2 = X_train[y_train_bin == 1]
y_train_stage2 = y_train_full[y_train_bin == 1].map(class_map)


# XGBoost as one of the base learners
xgb = XGBClassifier(
    objective="multi:softprob", 
    num_class=5, 
    eval_metric="mlogloss",
    n_estimators=200, 
    max_depth=6, 
    gamma=1, 
    colsample_bytree=0.7,
    learning_rate=0.1, 
    random_state=42
)

# Gradient Boosting as another base learner
gbc = GradientBoostingClassifier(
    n_estimators=200, max_depth=4, 
    learning_rate=0.01, 
    subsample=1.0, 
    random_state=42
)

# Logistic Regression as final estimator (meta-model), with feature scaling
logreg_pipe = make_pipeline(         # Logistic Regression with StandardScaler Pipeline
    StandardScaler(),
    LogisticRegression(
        max_iter=1000, 
        class_weight="balanced", 
        solver="lbfgs", 
        C=0.1, 
        random_state=42
    )
)


# Define stacking classifier
stacking_model = StackingClassifier(
    estimators=[("xgb", xgb), ("gbc", gbc)],
    final_estimator=logreg_pipe, stack_method="predict_proba",     # Use predicted class probabilities (not class labels) as inputs to final estimator
    passthrough=False,                                             # Do NOT pass original input features to the final estimator — only base model outputs are used. # Setting this to True would concatenate X with base model predictions before feeding into logreg_pipe.
    cv=3,                                                          # Perform 3-fold cross-validation to generate out-of-fold predictions from base models.   
    n_jobs=-1                                                      # Use all available CPU cores to train models in parallel
)

# Train the stacking model on the filtered data
stacking_model.fit(X_train_stage2, y_train_stage2)


# === Save trained models ===
joblib.dump(model_bin, "saved_models/model_bin_stage1.pkl")
joblib.dump(stacking_model, "saved_models/model_stacking_stage2.pkl")
