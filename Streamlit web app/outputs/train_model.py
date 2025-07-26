
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
df = pd.read_csv("results.csv")

# Drop matches with missing scores
df = df.dropna(subset=["home_score", "away_score"])

# Create match result label
def get_result(row):
    if row["home_score"] > row["away_score"]:
        return 0  # Home Win
    elif row["home_score"] == row["away_score"]:
        return 1  # Draw
    else:
        return 2  # Away Win

df["result"] = df.apply(get_result, axis=1)

# Encode team names
teams = list(set(df["home_team"]) | set(df["away_team"]))
team_to_id = {team: idx for idx, team in enumerate(teams)}
df["home_team"] = df["home_team"].map(team_to_id)
df["away_team"] = df["away_team"].map(team_to_id)

# Features and target
X = df[["home_team", "away_team"]]
y = df["result"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model and mappings
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("team_mapping.pkl", "wb") as f:
    pickle.dump(team_to_id, f)
