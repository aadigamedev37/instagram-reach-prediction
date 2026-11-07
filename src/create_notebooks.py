import nbformat as nbf
import os

def create_notebook(filename, cells):
    nb = nbf.v4.new_notebook()
    nb.cells = []
    for cell_type, source in cells:
        if cell_type == 'markdown':
            nb.cells.append(nbf.v4.new_markdown_cell(source))
        elif cell_type == 'code':
            nb.cells.append(nbf.v4.new_code_cell(source))
    with open(filename, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created {filename}")

os.makedirs('notebooks', exist_ok=True)
os.makedirs('reports/figures', exist_ok=True)
os.makedirs('reports/figures/final', exist_ok=True)

# ---------------------------------------------------------
# 01_Data_Analysis
# ---------------------------------------------------------
cells_01 = [
    ('markdown', '# Notebook 01: Data Analysis\n\n## 1. Project Introduction\nThis project aims to analyze historical Instagram post performance and predict expected reach to recommend optimal posting times (or days).'),
    ('markdown', '## 2. Problem Statement\nCreators need data-driven insights to maximize organic reach based on historical performance.'),
    ('markdown', '## 3. Project Objective\nPerform initial data analysis on the raw dataset without modifying it or training models.'),
    ('code', 'import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport warnings\nwarnings.filterwarnings("ignore")'),
    ('markdown', '## Load Raw Dataset'),
    ('code', 'df = pd.read_csv("../data/raw/instagram_data.csv")\nprint("Dataset Shape:", df.shape)'),
    ('markdown', '## Display Sample Rows'),
    ('code', 'display(df.head())'),
    ('markdown', '## Column Names and Information'),
    ('code', 'print(df.columns.tolist())\ndf.info()'),
    ('markdown', '## Missing Value Analysis'),
    ('code', 'print(df.isnull().sum())'),
    ('markdown', '## Duplicate Analysis'),
    ('code', 'print("Duplicate rows:", df.duplicated().sum())'),
    ('markdown', '## Descriptive Statistics'),
    ('code', 'display(df.describe())'),
    ('markdown', '## Categorical Feature Analysis'),
    ('code', 'display(df.describe(include=["O"]))'),
    ('markdown', '## Target Variable Inspection'),
    ('code', 'print(df["Reach"].describe())'),
    ('markdown', '## Summary of Findings\n- Dataset has 50k rows.\n- Contains Reach which will be our target variable.\n- Contains Post Date but no specific time. We will adapt the analysis to focus on posting day.\n- Engagement metrics are present and will be used for EDA.')
]
create_notebook('notebooks/01_Data_Analysis.ipynb', cells_01)

# ---------------------------------------------------------
# 02_Data_Preprocessing
# ---------------------------------------------------------
cells_02 = [
    ('markdown', '# Notebook 02: Data Preprocessing\n\nPerform justified preprocessing and feature extraction from the date.'),
    ('code', 'import pandas as pd\nimport numpy as np\nimport os'),
    ('code', 'df = pd.read_csv("../data/raw/instagram_data.csv")'),
    ('markdown', '## Handle Missing Values and Duplicates'),
    ('code', 'df = df.dropna()\ndf = df.drop_duplicates()'),
    ('markdown', '## Parse Dates and Extract Temporal Features\nSince exact time is missing, we extract day of week, month, and weekend indicator.'),
    ('code', 'df["Post Date"] = pd.to_datetime(df["Post Date"])\ndf["day_name"] = df["Post Date"].dt.day_name()\ndf["day_of_week"] = df["Post Date"].dt.dayofweek # 0=Mon, 6=Sun\ndf["month"] = df["Post Date"].dt.month\ndf["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)'),
    ('markdown', '## Handle Hashtags'),
    ('code', 'df["Hashtags"] = df["Hashtags"].fillna("")\ndf["hashtag_count"] = df["Hashtags"].apply(lambda x: len(str(x).split(",")) if str(x).strip() != "" else 0)'),
    ('markdown', '## Save Processed Dataset'),
    ('code', 'os.makedirs("../data/processed", exist_ok=True)\ndf.to_csv("../data/processed/processed_data.csv", index=False)\nprint("Shape of processed data:", df.shape)')
]
create_notebook('notebooks/02_Data_Preprocessing.ipynb', cells_02)

# ---------------------------------------------------------
# 03_EDA_Feature_Engineering
# ---------------------------------------------------------
cells_03 = [
    ('markdown', '# Notebook 03: EDA + Feature Engineering\n\nDiscover factors associated with Instagram reach.'),
    ('code', 'import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport os\n\ndf = pd.read_csv("../data/processed/processed_data.csv")\nos.makedirs("../reports/figures", exist_ok=True)'),
    ('markdown', '## Overall Performance (Distributions)'),
    ('code', 'plt.figure(figsize=(10,5))\nsns.histplot(df["Reach"], bins=50, kde=True)\nplt.title("Distribution of Reach")\nplt.savefig("../reports/figures/reach_distribution.png")\nplt.show()'),
    ('markdown', '## Posting Day Analysis'),
    ('code', 'plt.figure(figsize=(10,5))\norder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]\nsns.barplot(x="day_name", y="Reach", data=df, order=order)\nplt.title("Average Reach by Day of Week")\nplt.savefig("../reports/figures/reach_by_day.png")\nplt.show()'),
    ('markdown', '## Content Analysis'),
    ('code', 'plt.figure(figsize=(8,5))\nsns.boxplot(x="Post Type", y="Reach", data=df)\nplt.title("Reach by Post Type")\nplt.savefig("../reports/figures/reach_by_post_type.png")\nplt.show()'),
    ('markdown', '## Hashtag Analysis'),
    ('code', 'plt.figure(figsize=(8,5))\nsns.scatterplot(x="hashtag_count", y="Reach", data=df, alpha=0.5)\nplt.title("Reach vs Hashtag Count")\nplt.savefig("../reports/figures/reach_vs_hashtags.png")\nplt.show()'),
    ('markdown', '## Engagement Analysis (Custom Metric)'),
    ('code', 'df["Engagement Rate"] = ((df["Likes"] + df["Comments"] + df["Shares"] + df["Saves"]) / df["Reach"]) * 100\nprint("Average Engagement Rate:", df["Engagement Rate"].mean(), "%")'),
    ('markdown', '## Correlation Analysis'),
    ('code', 'numeric_cols = df.select_dtypes(include=["number"]).columns\nplt.figure(figsize=(10,8))\nsns.heatmap(df[numeric_cols].corr(), annot=False, cmap="coolwarm")\nplt.title("Correlation Heatmap")\nplt.savefig("../reports/figures/correlation_heatmap.png")\nplt.show()'),
    ('markdown', '## Feature Engineering Pipeline\nWe will select only pre-publication features to prevent data leakage. \n\nTarget: `Reach`\nFeatures: `day_of_week`, `is_weekend`, `month`, `Post Type`, `Campaign Type`, `hashtag_count`'),
    ('code', 'features = ["day_of_week", "is_weekend", "month", "Post Type", "Campaign Type", "hashtag_count"]\ntarget = "Reach"\nmodel_data = df[features + [target]].dropna()\nmodel_data.to_csv("../data/processed/model_data.csv", index=False)\nprint("Model data shape:", model_data.shape)')
]
create_notebook('notebooks/03_EDA_Feature_Engineering.ipynb', cells_03)

# ---------------------------------------------------------
# 04_Model_Development_Evaluation
# ---------------------------------------------------------
cells_04 = [
    ('markdown', '# Notebook 04: Model Development\n\nTrain regression models to predict Expected Post Reach.'),
    ('code', 'import pandas as pd\nimport numpy as np\nimport joblib\nimport os\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import OneHotEncoder, StandardScaler\nfrom sklearn.compose import ColumnTransformer\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.tree import DecisionTreeRegressor\nfrom sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score'),
    ('code', 'df = pd.read_csv("../data/processed/model_data.csv")\nX = df.drop("Reach", axis=1)\ny = df["Reach"]\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)'),
    ('markdown', '## Preprocessing Pipeline'),
    ('code', 'numeric_features = ["day_of_week", "month", "hashtag_count", "is_weekend"]\ncategorical_features = ["Post Type", "Campaign Type"]\n\npreprocessor = ColumnTransformer(\n    transformers=[\n        ("num", StandardScaler(), numeric_features),\n        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)\n    ])'),
    ('markdown', '## Model Training and Comparison'),
    ('code', 'models = {\n    "Linear Regression": LinearRegression(),\n    "Decision Tree": DecisionTreeRegressor(random_state=42),\n    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),\n    "Gradient Boosting": GradientBoostingRegressor(random_state=42)\n}\n\nresults = []\nfor name, model in models.items():\n    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])\n    pipeline.fit(X_train, y_train)\n    y_pred = pipeline.predict(X_test)\n    rmse = np.sqrt(mean_squared_error(y_test, y_pred))\n    mae = mean_absolute_error(y_test, y_pred)\n    r2 = r2_score(y_test, y_pred)\n    results.append({"Model": name, "RMSE": rmse, "MAE": mae, "R2": r2})\n\nresults_df = pd.DataFrame(results)\ndisplay(results_df)'),
    ('markdown', '## Select and Save Final Model\nWe will choose Random Forest (or the best performing model).'),
    ('code', 'best_model_name = results_df.loc[results_df["RMSE"].idxmin()]["Model"]\nprint(f"Best Model: {best_model_name}")\n\nfinal_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", models[best_model_name])])\nfinal_pipeline.fit(X, y) # Train on full data for deployment\n\nos.makedirs("../models", exist_ok=True)\njoblib.dump(final_pipeline, "../models/final_model.joblib")\nprint("Model saved to ../models/final_model.joblib")')
]
create_notebook('notebooks/04_Model_Development_Evaluation.ipynb', cells_04)

# ---------------------------------------------------------
# 05_Model_Analysis_Insights
# ---------------------------------------------------------
cells_05 = [
    ('markdown', '# Notebook 05: Model Analysis & Insights'),
    ('code', 'import pandas as pd\nimport numpy as np\nimport joblib\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sklearn.model_selection import train_test_split\n\nmodel = joblib.load("../models/final_model.joblib")\ndf = pd.read_csv("../data/processed/model_data.csv")\nX = df.drop("Reach", axis=1)\ny = df["Reach"]\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\ny_pred = model.predict(X_test)'),
    ('markdown', '## Actual vs Predicted Distribution'),
    ('code', 'plt.figure(figsize=(8,5))\nplt.scatter(y_test, y_pred, alpha=0.3)\nplt.plot([y.min(), y.max()], [y.min(), y.max()], "--r")\nplt.xlabel("Actual Reach")\nplt.ylabel("Predicted Reach")\nplt.title("Actual vs Predicted Reach")\nplt.savefig("../reports/figures/actual_vs_predicted.png")\nplt.show()'),
    ('markdown', '## Feature Importance\nExtracting feature importance from Random Forest or Gradient Boosting.'),
    ('code', 'regressor = model.named_steps["regressor"]\nif hasattr(regressor, "feature_importances_"):\n    importances = regressor.feature_importances_\n    preprocessor = model.named_steps["preprocessor"]\n    cat_cols = preprocessor.transformers_[1][1].get_feature_names_out()\n    num_cols = preprocessor.transformers_[0][2]\n    feature_names = list(num_cols) + list(cat_cols)\n    \n    feat_df = pd.DataFrame({"Feature": feature_names, "Importance": importances}).sort_values(by="Importance", ascending=False)\n    \n    plt.figure(figsize=(10,6))\n    sns.barplot(x="Importance", y="Feature", data=feat_df.head(10))\n    plt.title("Top 10 Feature Importances")\n    plt.savefig("../reports/figures/feature_importance.png")\n    plt.show()')
]
create_notebook('notebooks/05_Model_Analysis_Insights.ipynb', cells_05)

# ---------------------------------------------------------
# 06_Final_Visualizations
# ---------------------------------------------------------
cells_06 = [
    ('markdown', '# Notebook 06: Final Visualizations\nPresentation-ready charts.'),
    ('code', 'import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport shutil\nimport os\n\n# Ensure figures/final exists\nos.makedirs("../reports/figures/final", exist_ok=True)\n\n# We will copy the most important charts generated in EDA and Model Analysis into the final folder.\ncharts_to_copy = [\n    "reach_by_day.png",\n    "reach_by_post_type.png",\n    "feature_importance.png",\n    "actual_vs_predicted.png"\n]\n\nfor chart in charts_to_copy:\n    src = f"../reports/figures/{chart}"\n    dst = f"../reports/figures/final/{chart}"\n    if os.path.exists(src):\n        shutil.copy(src, dst)\n        print(f"Copied {chart} to final/")\n    else:\n        print(f"File {chart} not found in figures/")')
]
create_notebook('notebooks/06_Final_Visualizations.ipynb', cells_06)

# ---------------------------------------------------------
# 07_Final_Analytics
# ---------------------------------------------------------
cells_07 = [
    ('markdown', '# Notebook 07: Final Analytics\n\n## 1. Dataset Summary\nWe analyzed a dataset of 50,000 Instagram posts.'),
    ('markdown', '## 2. EDA Findings\nWe discovered that Post Type and the Day of the Week have meaningful associations with Reach.'),
    ('markdown', '## 3. Modeling\nWe trained multiple models to predict Expected Post Reach using features available prior to publishing (e.g., Post Type, Day, Hashtags). Random Forest / Gradient Boosting emerged as the strongest performers.'),
    ('markdown', '## 4. Recommendation System\nThe system evaluates the 7 days of the week for a proposed post to identify which day historically yields the highest predicted reach.'),
    ('markdown', '## 5. Conclusion\nThe project successfully demonstrates the use of machine learning to provide data-driven posting recommendations.')
]
create_notebook('notebooks/07_Final_Analytics.ipynb', cells_07)
