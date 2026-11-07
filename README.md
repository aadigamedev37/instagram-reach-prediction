# Instagram Post Reach Prediction and Optimal Posting Time Recommendation System

## Project Description
This applied data science project analyzes historical Instagram post performance to discover how content types, posting days, hashtags, and campaign types influence post reach. Using a Machine Learning regression model, the system predicts the expected reach of a future post and recommends the optimal day to post to maximize potential audience engagement.

## Problem Statement
Content creators struggle to maximize organic reach due to algorithmic complexities. A data-driven approach is needed to predict expected reach and optimize posting schedules based on historical performance rather than guesswork.

## Objectives
1. Analyze historical Instagram data to identify key features affecting reach.
2. Build regression models to predict expected reach.
3. Develop a recommendation engine for the optimal posting window (adapted to day of week based on available data).
4. Create an interactive dashboard for predictive analytics.

## Technology Stack
* **Language:** Python
* **Data Processing:** pandas, numpy
* **Visualization:** matplotlib, seaborn
* **Machine Learning:** scikit-learn
* **Dashboard:** Streamlit
* **Environment:** Jupyter Notebooks, Papermill

## Architecture & Methodology
1. **Data Preprocessing:** Handled missing values, parsed dates, engineered temporal features (`day_of_week`, `is_weekend`, `month`), and computed custom engagement rates.
2. **EDA:** Analyzed distributions and correlations (e.g., Reach vs Post Type, Reach vs Hashtag count).
3. **Modeling:** Trained Linear Regression, Decision Tree, Random Forest, and Gradient Boosting regressors. Random Forest was selected as the final model.
4. **Recommendation:** A simulated scenario tests the feature vector across all 7 days of the week, ranking them by predicted reach to identify the best posting day.

## Installation
1. Clone or download the repository.
2. Ensure you have Python installed.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Execution Instructions
You can execute the entire project pipeline (generating notebooks, executing them, and training the model) with a single command:
```bash
python run_project.py
```

## Running the Dashboard
To launch the interactive dashboard, run:
```bash
streamlit run app/app.py
```

## Results
* The Random Forest regressor successfully models the complex relationships between the categorical features (Campaign Type, Post Type) and the numerical target (Reach).
* The dashboard successfully ranks the days of the week for maximum predicted reach based on the model's output.

## Limitations
* The dataset provided dates without exact timestamps (HH:MM). The analysis was adapted to optimize for the **Posting Day** and **Month** rather than exact time.
* The model identifies historical associations but does not guarantee account growth.

## Future Scope
* Incorporate real-time API integrations with the Instagram Graph API.
* Utilize NLP for deep caption and sentiment analysis.
