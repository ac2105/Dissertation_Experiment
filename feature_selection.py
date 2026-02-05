import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2
from scipy.sparse import csr_matrix
import os

# Path to your cleaned master file
file_path = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix_CLEAN.csv'

def feature_selection_sparse(top_k=20):
    print("Loading dataset...")
    # Read the data
    df = pd.read_csv(file_path)
    
    # 1. Prepare X and y
    # Drop non-numeric columns and columns with all zeros to prevent errors
    X_raw = df.drop(columns=['applications', 'label'])
    y = df['label'].values
    
    permission_names = X_raw.columns
    
    print("Converting to Sparse Matrix to save RAM...")
    # This turns your 6GB requirement into a tiny fraction of that
    X_sparse = csr_matrix(X_raw.values)
    
    # Clear raw data from memory to free up space
    del X_raw
    
    results = pd.DataFrame({'Permission': permission_names})

    # --- Chi-Square (Optimized for Sparse) ---
    print("Calculating Chi-Square scores...")
    chi_selector = SelectKBest(score_func=chi2, k=top_k)
    chi_selector.fit(X_sparse, y)
    results['Chi2_Score'] = chi_selector.scores_

    # --- Pearson Correlation Coefficient (Optimized for Sparse) ---
    print("Calculating Pearson Correlation...")
    # Standard correlation can be slow on sparse, so we use a matrix-based approach
    # Correlation = (Covariance of X,y) / (std_dev X * std_dev y)
    y_mean = y.mean()
    y_std = y.std()
    
    # Centering the data manually to maintain sparsity benefits
    X_means = np.array(X_sparse.mean(axis=0)).flatten()
    X_stds = np.sqrt(np.array(X_sparse.power(2).mean(axis=0)).flatten() - X_means**2)
    
    # Calculate correlation
    covariance = (X_sparse.transpose().dot(y) / len(y)) - (X_means * y_mean)
    # Avoid division by zero for permissions that never change
    correlations = np.divide(covariance, (X_stds * y_std), out=np.zeros_like(covariance), where=(X_stds * y_std)!=0)
    
    results['Pearson_Corr'] = correlations
    results['Abs_Pearson'] = np.abs(correlations)

    return results

# Run the analysis
results = feature_selection_sparse()

# --- Print Results to CMD ---
print("\n" + "="*50)
print("TOP 10 MALWARE PREDICTORS (Chi-Square)")
print(results.sort_values(by='Chi2_Score', ascending=False)[['Permission', 'Chi2_Score']].head(10))

print("\n" + "="*50)
print("TOP 10 MALWARE PREDICTORS (Pearson Correlation)")
# Positive correlation = Malware indicator, Negative = Benign indicator
print(results.sort_values(by='Pearson_Corr', ascending=False)[['Permission', 'Pearson_Corr']].head(10))