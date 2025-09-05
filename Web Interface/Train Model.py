import pandas as pd
from xgboost import XGBRegressor
import joblib

df = pd.read_excel("Results_AI.xlsx")
X = df[["Cement", "Fly ash", "Metakaolin", "Silica Fume", "Rice Husk Ash", "Curing age"]]
y = df["Compressive Strength"]

best_params = {
    "n_estimators": 284,
    "max_depth": 5,
    "learning_rate": 0.11815054182606834,
    "subsample": 0.6837242654182539,
    "colsample_bytree": 0.9912964250240169,
    "gamma": 1.006751684072039,
    "reg_alpha": 0.6041355893342345,
    "reg_lambda": 0.9654158595465725,
    "random_state": 42
}

model = XGBRegressor(**best_params)
model.fit(X, y)

joblib.dump(model, "final_model.pkl")
print("Model trained & saved as final_model.pkl")
