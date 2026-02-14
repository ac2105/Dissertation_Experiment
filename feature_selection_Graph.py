import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest, chi2
import os

# Path to your standardized master matrix
file_path = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix_OFFICIAL.csv'
graph_output = r'C:\Users\Janshrut\Desktop\Sem2\feature_selection_comparison.png'

def run_feature_iterations():
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print("Loading official dataset...")
    df = pd.read_csv(file_path)
    
    # 1. Prepare Features and Target
    X_raw = df.drop(columns=['applications', 'label'])
    y = df['label'].values
    
    # --- PRE-FILTER: IDENTIFY CONSTANT FEATURES ---
    # Permissions where every value is the same (all 0 or all 1)
    constant_features = [col for col in X_raw.columns if X_raw[col].std() == 0]
    
    if constant_features:
        print(f"\n--- Removed {len(constant_features)} Constant Permissions ---")
        for p in constant_features:
            print(f" - {p}")
        print("-------------------------------------------\n")
    
    # Keep only features with variance > 0
    X_all = X_raw.drop(columns=constant_features)
    feature_names = X_all.columns
    total_features = len(feature_names)
    
    print(f"Remaining active permissions for analysis: {total_features}")

    # 2. Pre-calculate Global Rankings
    print("Calculating Chi-Square and Pearson rankings...")
    
    # Chi-Square
    chi_selector = SelectKBest(score_func=chi2, k='all')
    chi_selector.fit(X_all, y)
    chi_ranked_features = [f for _, f in sorted(zip(chi_selector.scores_, feature_names), reverse=True)]

    # Pearson Correlation (Safe now because std dev is not 0)
    pearson_corrs = X_all.corrwith(pd.Series(y)).abs()
    pearson_ranked_features = pearson_corrs.sort_values(ascending=False).index.tolist()

    # 3. Define Iteration Steps
    ks = list(range(10, total_features + 1, 10))
    if total_features not in ks:
        ks.append(total_features)

    results = {'k': ks, 'Chi2_RF': [], 'Chi2_DT': [], 'Pearson_RF': [], 'Pearson_DT': []}

    print("Starting iterations with 70:30 split...")
    for k in ks:
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        dt = DecisionTreeClassifier(random_state=42)

        # Subset logic
        for algo_name, ranked_list in [("Chi2", chi_ranked_features), ("Pearson", pearson_ranked_features)]:
            X_subset = X_all[ranked_list[:k]]
            X_train, X_test, y_train, y_test = train_test_split(X_subset, y, test_size=0.30, random_state=42)
            
            # RF
            rf.fit(X_train, y_train)
            results[f'{algo_name}_RF'].append(accuracy_score(y_test, rf.predict(X_test)))
            
            # DT
            dt.fit(X_train, y_train)
            results[f'{algo_name}_DT'].append(accuracy_score(y_test, dt.predict(X_test)))
        
        print(f"Progress: k={k}/{total_features}")

    # 4. Visualization
    plt.figure(figsize=(14, 8))
    plt.plot(ks, results['Chi2_RF'], color='red', label='Chi2 + Random Forest')
    plt.plot(ks, results['Chi2_DT'], color='blue', label='Chi2 + Decision Tree')
    plt.plot(ks, results['Pearson_RF'], color='orange', label='Pearson + Random Forest')
    plt.plot(ks, results['Pearson_DT'], color='purple', label='Pearson + Decision Tree')

    plt.title('Accuracy vs Number of Permissions (Constant Features Removed)')
    plt.xlabel('Number of Permissions (k)')
    plt.ylabel('Accuracy Score')
    plt.legend(loc='lower right')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.savefig(graph_output)
    print(f"\n✅ SUCCESS! Graph saved at: {graph_output}")
    plt.show()

if __name__ == "__main__":
    run_feature_iterations()