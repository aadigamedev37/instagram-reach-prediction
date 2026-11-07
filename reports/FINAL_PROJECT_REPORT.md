# FINAL PROJECT REPORT

## 1. Title
Instagram Post Reach Prediction and Optimal Posting Time Recommendation Using Data Analytics and Machine Learning

## 2. Abstract
Maximizing organic reach on Instagram is a critical challenge for content creators and businesses. Due to algorithmic complexity, scheduling posts is often based on intuition rather than data. This project proposes a data-driven system that uses Machine Learning to predict the expected reach of a proposed post based on pre-publication features. Additionally, it features a recommendation engine that evaluates various temporal variables (e.g., day of the week) to suggest the optimal posting schedule. We analyzed a dataset of 50,000 Instagram posts, trained an ensemble regression model, and deployed an interactive Streamlit dashboard for real-time predictions.

## 3. Introduction
Social media platforms rely on sophisticated algorithms to distribute content. Reach—the number of unique users who see a post—is the primary metric for top-of-funnel brand awareness. Predicting reach allows creators to adjust their content strategy proactively.

## 4. Problem Statement
Content creators lack tools to accurately estimate the performance of an Instagram post before it goes live. This leads to sub-optimal posting schedules and wasted content potential. A predictive system is required to replace guesswork with data.

## 5. Motivation
Investing resources in content creation only to receive low reach is demoralizing and costly for businesses. Empowering creators with predictive analytics ensures a higher return on investment for their social media efforts.

## 6. Objectives
* Perform Exploratory Data Analysis (EDA) on a robust Instagram dataset.
* Identify the most significant factors influencing reach.
* Train and evaluate regression models.
* Build a recommendation engine to identify the best time/day to post.
* Deploy the solution via an interactive dashboard.

## 7. Existing Problem
Most existing tools either provide generic advice (e.g., "Post on Wednesdays at 11 AM") or require expensive enterprise subscriptions. Generic advice fails because optimal timing varies heavily based on the specific audience and content type.

## 8. Proposed System
We propose a custom Machine Learning pipeline that takes specific post attributes (Content Type, Hashtag Count, Campaign Type, Target Month) and evaluates them against historical patterns to dynamically predict reach and recommend the best posting day.

## 9. Dataset
We utilized the publicly available Sugar Cosmetics Instagram Analytics dataset from GitHub, consisting of 50,000 real-world posts.

## 10. Data Dictionary
* `Post Date`: The date the content was published.
* `Post Type`: Format of the content (Image, Video, Carousel, Story).
* `Campaign Type`: Marketing category.
* `Hashtags`: List of tags.
* `Reach`: (Target) Unique users who viewed the post.
* `Likes`, `Comments`, `Shares`, `Saves`: Post-publication engagement metrics.

## 11. Data Collection
Data was acquired via an open-source repository. To ensure integrity, the raw data was isolated and treated as immutable throughout the project lifecycle.

## 12. Data Cleaning
We removed duplicate rows and dropped records containing missing critical values (NaNs) to ensure the Machine Learning algorithms received complete numerical matrices.

## 13. Data Preprocessing
The `Post Date` column was parsed into a datetime object. Categorical variables (`Post Type`, `Campaign Type`) were transformed into numerical arrays using `OneHotEncoder`. Numerical inputs were scaled using `StandardScaler`.

## 14. Exploratory Data Analysis
Through visual analysis, we mapped the distribution of Reach (which is often right-skewed in social media). We also calculated average reach across the different days of the week, establishing a baseline understanding of audience responsiveness.

## 15. Feature Engineering
* **Temporal Features:** Extracted `day_of_week`, `is_weekend`, and `month`.
* **Content Features:** Calculated `hashtag_count` from raw string lists.
* **Leakage Prevention:** Removed `Likes`, `Comments`, and `Shares` from the feature set. Because these metrics are only known *after* publication, using them to predict future reach would constitute data leakage.

## 16. Machine Learning Methodology
We framed the task as a Supervised Regression problem. The dataset was split 80/20 (Train/Test). A scikit-learn `Pipeline` was utilized to tie preprocessing and modeling steps together.

## 17. Model Development
We developed four distinct models:
1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor
4. Gradient Boosting Regressor

## 18. Model Evaluation
Models were evaluated using Root Mean Squared Error (RMSE) and R-squared (R²). 

## 19. Model Comparison
Ensemble models (Random Forest, Gradient Boosting) significantly outperformed Linear Regression. Linear Regression struggled to capture the non-linear relationship between categorical features (like Post Type) and the target variable. Random Forest was selected for deployment.

## 20. Optimal Posting Time Methodology
Because the dataset provided dates without exact timestamps, the system was adapted to recommend the optimal Posting Day. The engine accepts the user's proposed post, duplicates the feature vector 7 times (for Monday through Sunday), and runs predictions. The day yielding the highest predicted reach is returned as the recommendation.

## 21. Results
The Machine Learning pipeline successfully predicted continuous reach values based strictly on pre-publication features. The recommendation algorithm successfully ranks days of the week, providing clear, actionable insights for the user.

## 22. Key Insights
* Content format is one of the strongest predictors of reach.
* There is variance in audience responsiveness depending on the day of the week.
* Using machine learning provides a highly individualized recommendation compared to generic internet advice.

## 23. Dashboard
An interactive Streamlit dashboard was developed featuring a dark analytics aesthetic. It includes KPI tracking, EDA visualizations, a live Post Predictor form, and a Data Explorer.

## 24. Limitations
* **Temporal Granularity:** The dataset lacked explicit hour/minute data, restricting recommendations to the day-level.
* **Causality:** The model identifies correlations (historical associations) but cannot guarantee future growth.

## 25. Future Scope
* **Real-time Ingestion:** Connect directly to the Instagram Graph API to scrape exact timestamps.
* **NLP Integration:** Use advanced Natural Language Processing to extract sentiment and topic clusters from raw caption text.

## 26. Conclusion
This project successfully demonstrated the application of Machine Learning to social media strategy. By adhering to rigorous data science principles (such as preventing data leakage), we built a robust, defensible system that provides actionable scheduling recommendations.

## 27. References
* Scikit-Learn Documentation
* Pandas and Numpy Documentation
* Streamlit Documentation
* Dataset: Neeraj08823/Sugar_cosmetics_Instagram_Analytics
