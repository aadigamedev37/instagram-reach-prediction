import os
import subprocess

def run_command(command, cwd=None):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Error executing: {command}")
        exit(1)

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    notebooks_dir = os.path.join(root_dir, "notebooks")
    
    print("--- 1. Generating Notebooks ---")
    run_command("python src/create_notebooks.py", cwd=root_dir)
    
    print("--- 2. Executing Notebooks sequentially ---")
    notebooks = [
        "01_Data_Analysis.ipynb",
        "02_Data_Preprocessing.ipynb",
        "03_EDA_Feature_Engineering.ipynb",
        "04_Model_Development_Evaluation.ipynb",
        "05_Model_Analysis_Insights.ipynb",
        "06_Final_Visualizations.ipynb",
        "07_Final_Analytics.ipynb"
    ]
    
    for nb in notebooks:
        print(f"\\nExecuting {nb}...")
        nb_path = os.path.join("notebooks", nb)
        run_command(f'python -m papermill -k python3 --cwd "{notebooks_dir}" "{nb_path}" "{nb_path}"', cwd=root_dir)
        
    print("\\n--- 3. Testing Recommendation Engine ---")
    run_command("python src/recommendation.py", cwd=root_dir)
    
    print("\\nProject execution completed successfully!")
    print("To launch the dashboard, run: streamlit run app/app.py")

if __name__ == "__main__":
    main()
