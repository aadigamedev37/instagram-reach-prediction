import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Instagram Reach Intelligence", page_icon="📈", layout="wide")

# Custom CSS for dark analytics aesthetic
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #4CAF50;
    }
    .metric-label {
        font-size: 14px;
        color: #B0B0B0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Instagram Reach Intelligence")
st.subheader("Data-driven posting time and reach prediction")
st.markdown("---")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load Data and Model
@st.cache_data
def load_data():
    data_path = BASE_DIR / "data" / "processed" / "processed_data.csv"
    if data_path.exists():
        return pd.read_csv(data_path)
    return None

@st.cache_resource
def load_model():
    model_path = BASE_DIR / "models" / "final_model.joblib"
    if model_path.exists():
        return joblib.load(model_path)
    return None

df = load_data()
model = load_model()

if df is not None and model is not None:
    # --- SECTION 1: KPI CARDS ---
    total_posts = len(df)
    avg_reach = int(df['Reach'].mean())
    best_day = df.groupby('day_name')['Reach'].mean().idxmax()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Total Posts Analyzed</div><div class='metric-value'>{total_posts:,}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Average Reach</div><div class='metric-value'>{avg_reach:,}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>Best Performing Day</div><div class='metric-value'>{best_day}</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- SECTION 2: DATA INSIGHTS ---
    st.header("Data Insights")
    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("Reach by Day")
        fig, ax = plt.subplots(figsize=(6,4))
        order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sns.barplot(x="day_name", y="Reach", data=df, order=order, ax=ax, palette="mako")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with colB:
        st.subheader("Reach by Post Type")
        fig2, ax2 = plt.subplots(figsize=(6,4))
        sns.barplot(x="Post Type", y="Reach", data=df, ax=ax2, palette="viridis")
        st.pyplot(fig2)
        
    st.markdown("---")
    
    # --- SECTION 3: POST PREDICTOR ---
    st.header("Post Predictor")
    st.write("Enter proposed post details to predict reach and find the optimal day to post.")
    
    with st.form("predictor_form"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            post_type = st.selectbox("Post Type", df["Post Type"].unique())
            campaign_type = st.selectbox("Campaign Type", df["Campaign Type"].unique())
            hashtag_count = st.number_input("Number of Hashtags", min_value=0, max_value=30, value=5)
        with p_col2:
            target_month = st.slider("Month of the Year", min_value=1, max_value=12, value=6)
            
        submit = st.form_submit_button("Predict Reach & Recommend Day")
        
    if submit:
        # Evaluate for all 7 days
        days_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        predictions = []
        
        for day_num, day_name in days_map.items():
            weekend_flag = 1 if day_num >= 5 else 0
            features = pd.DataFrame([{
                "day_of_week": day_num,
                "is_weekend": weekend_flag,
                "month": target_month,
                "Post Type": post_type,
                "Campaign Type": campaign_type,
                "hashtag_count": hashtag_count
            }])
            
            pred = model.predict(features)[0]
            predictions.append({"Day": day_name, "Predicted Reach": int(pred)})
            
        results_df = pd.DataFrame(predictions)
        results_df = results_df.sort_values("Predicted Reach", ascending=False).reset_index(drop=True)
        
        best_day_rec = results_df.iloc[0]["Day"]
        best_reach_rec = results_df.iloc[0]["Predicted Reach"]
        
        # --- SECTION 4 & 5: PREDICTION RESULT & RECOMMENDATION ---
        st.success("Prediction complete!")
        
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.markdown(f"### Recommended Posting Day: **{best_day_rec}**")
            st.markdown(f"### Maximum Predicted Reach: **{best_reach_rec:,}**")
            st.info(f"Based on historical data and model predictions, {best_day_rec} is the recommended posting day for the highest predicted reach. This is an estimate based on associated variables, not a guarantee of account growth.")
            
        with r_col2:
            st.write("Alternative Days:")
            st.dataframe(results_df.style.background_gradient(cmap="Greens"))
            
        # --- SECTION 6: TIME COMPARISON ---
        st.subheader("Predicted Reach Across the Week")
        fig3, ax3 = plt.subplots(figsize=(10,4))
        sns.lineplot(x="Day", y="Predicted Reach", data=results_df, marker="o", ax=ax3, sort=False, color="cyan")
        plt.grid(True, alpha=0.3)
        st.pyplot(fig3)
        
    st.markdown("---")
    
    # --- SECTION 7 & 8: DATA EXPLORER & INSIGHTS ---
    st.header("Data Explorer & Key Insights")
    st.write(f"The best performing content format historically is **{df.groupby('Post Type')['Reach'].mean().idxmax()}**.")
    st.write(f"The best performing day overall historically is **{best_day}**.")
    
    st.dataframe(df.head(100))
    st.download_button(
        label="Download Processed Data",
        data=df.to_csv(index=False),
        file_name='processed_instagram_data.csv',
        mime='text/csv'
    )
else:
    st.error("Data or model not found. Please ensure notebooks have been executed.")
