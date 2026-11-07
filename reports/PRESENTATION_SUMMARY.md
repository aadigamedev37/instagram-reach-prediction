# Presentation Summary

**Slide 1 — Title**
* Title: Instagram Post Reach Prediction and Optimal Posting Time Recommendation Using Data Analytics and Machine Learning
* Presenter: Tanishq
* Course: Applied Data Science Capstone

**Slide 2 — Problem Statement**
* Organic reach on Instagram is difficult to predict.
* Content creators often rely on guesswork to schedule posts.
* Without a data-driven approach, creators miss potential engagement.

**Slide 3 — Objectives**
* Analyze 50,000 historical Instagram posts.
* Understand the relationship between reach and features like content type, campaign type, and posting day.
* Build a Machine Learning pipeline to predict expected reach.
* Develop a recommendation engine that suggests the best day to post.

**Slide 4 — Proposed Solution**
* Input: Content metadata (Post Type, Hashtag Count, Campaign Type) + Temporal variables (Month, Day).
* Engine: A trained ensemble regression model (Random Forest).
* Output: A predicted Reach value, and a ranked recommendation of which day of the week maximizes this reach.

**Slide 5 — Dataset**
* Source: Public GitHub Repository (Sugar Cosmetics Instagram Analytics).
* Size: 50,000 records.
* Key Features: `Post Date`, `Post Type`, `Campaign Type`, `Hashtags`, `Reach`, `Likes`, `Comments`.
* Target Variable: `Reach`.

**Slide 6 — Data Preprocessing**
* Dropped missing values.
* Extracted temporal variables from `Post Date` (`day_of_week`, `is_weekend`, `month`).
* Handled categorical variables using `OneHotEncoder`.
* Scaled numerical variables using `StandardScaler`.

**Slide 7 — EDA / Visual Insights**
* Discovered specific content types (e.g., Reels/Video vs Image) perform differently.
* Observed fluctuating average reach across different days of the week.
* Demonstrated high correlation between Reach and subsequent engagement (Likes, Comments).

**Slide 8 — Feature Engineering**
* Rigorously removed post-publication metrics (Likes, Comments, Shares) to prevent **Data Leakage**.
* Converted raw hashtag strings into a quantitative `hashtag_count`.
* Engineered a binary `is_weekend` flag to capture behavioral shifts on Saturdays/Sundays.

**Slide 9 — ML Methodology**
* Problem Type: Supervised Regression.
* Evaluation Metrics: Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and R-squared (R²).
* Splitting: 80% Training Data, 20% Testing Data.
* Pipeline Approach: Combined preprocessing and modeling steps to ensure consistency.

**Slide 10 — Model Comparison**
* Evaluated Linear Regression, Decision Tree, Random Forest, and Gradient Boosting.
* Ensemble methods (Random Forest and Gradient Boosting) outperformed simpler models because they capture non-linear social media patterns better.

**Slide 11 — Optimal Posting Time Recommendation**
* For any proposed post, the engine simulates posting on all 7 days of the week.
* It predicts the expected reach for each scenario using the trained Random Forest model.
* It ranks the days and outputs the single highest-performing recommendation.

**Slide 12 — Dashboard**
* Built an interactive Streamlit UI.
* Users can explore the dataset, view KPI cards, and use the "Post Predictor".
* The dashboard instantly runs the ML pipeline in the background and visualizes the results cleanly.

**Slide 13 — Key Results**
* The system successfully predicts a continuous reach value using purely pre-publication features.
* The recommendation engine seamlessly integrates with the model to optimize scheduling decisions.

**Slide 14 — Limitations**
* The dataset lacked exact hourly timestamps (HH:MM), so the analysis was strategically adapted to optimize the **Day** rather than the exact hour.
* The model discovers historical associations but cannot mathematically guarantee future algorithmic account growth.

**Slide 15 — Conclusion & Future Scope**
* We proved that machine learning can replace guesswork in social media scheduling.
* Future scope includes integrating real-time Instagram API data for hourly granularity and using deep NLP for caption sentiment analysis.
