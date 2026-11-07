import pandas as pd
import numpy as np
import joblib

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class PostingRecommendationEngine:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = BASE_DIR / "models" / "final_model.joblib"
        self.model = joblib.load(model_path)
        
    def recommend(self, post_type, campaign_type, hashtag_count, month=1, is_weekend=0):
        """
        Evaluates the expected reach for each day of the week given the post characteristics.
        """
        days = {
            0: "Monday", 
            1: "Tuesday", 
            2: "Wednesday", 
            3: "Thursday", 
            4: "Friday", 
            5: "Saturday", 
            6: "Sunday"
        }
        
        predictions = []
        for day_num, day_name in days.items():
            # Override is_weekend based on day_num
            weekend_flag = 1 if day_num >= 5 else 0
            
            # Create feature vector matching model training
            features = pd.DataFrame([{
                "day_of_week": day_num,
                "is_weekend": weekend_flag,
                "month": month,
                "Post Type": post_type,
                "Campaign Type": campaign_type,
                "hashtag_count": hashtag_count
            }])
            
            pred_reach = self.model.predict(features)[0]
            predictions.append({
                "Day": day_name,
                "Predicted Reach": int(pred_reach)
            })
            
        results_df = pd.DataFrame(predictions)
        results_df["Rank"] = results_df["Predicted Reach"].rank(method="min", ascending=False).astype(int)
        results_df = results_df.sort_values("Rank").reset_index(drop=True)
        
        best_day = results_df.iloc[0]["Day"]
        best_reach = results_df.iloc[0]["Predicted Reach"]
        
        recommendation = {
            "Recommended Posting Day": best_day,
            "Predicted Reach": best_reach,
            "Explanation": f"Based on historical data and model predictions, {best_day} is the recommended posting day for the highest predicted reach.",
            "All Predictions": results_df.to_dict("records")
        }
        return recommendation

if __name__ == "__main__":
    engine = PostingRecommendationEngine()
    rec = engine.recommend(post_type="Image", campaign_type="Tutorial", hashtag_count=5, month=6)
    print("Recommendation:")
    print(rec["Recommended Posting Day"], "-", rec["Predicted Reach"])
    print(rec["Explanation"])
    print("\nAlternative Days:")
    for alt in rec["All Predictions"]:
        print(f"{alt['Day']} | Reach: {alt['Predicted Reach']} | Rank: {alt['Rank']}")
