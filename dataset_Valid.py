import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

# Paths
file_path = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix_OFFICIAL.csv'
strict_output = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix_FINAL.csv'
url = "https://developer.android.com/reference/android/Manifest.permission"

def perform_strict_cleaning():
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    # 1. Fetch and Deep Scan the Android Developer Page
    print("Step 1: Deep Scanning official Android Manifest.permission list...")
    try:
        # Headers help mimic a real browser to prevent being blocked
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=20)
        
        # use a Regular Expression to find all instances of 'android.permission.SOMETHING'
        # This is more reliable than looking for specific HTML tags
        raw_html = response.text
        official_google_list = set(re.findall(r'android\.permission\.[A-Z_0-9]+', raw_html))
        
        if not official_google_list:
            print("❌ Error: Could not extract permissions from the website. Check your internet connection.")
            return
            
        print(f"✅ Success! Found {len(official_google_list)} official permissions on Google's website.")
    except Exception as e:
        print(f"Failed to connect to Android docs: {e}")
        return

    # 2. Load your current matrix
    print("Step 2: Loading current master matrix...")
    df = pd.read_csv(file_path)
    all_columns = df.columns.tolist()
    
    # 3. Matching Logic
    # We clean the names and check for the intersection
    valid_perms = [col for col in all_columns if col.strip() in official_google_list]
    invalid_perms = [col for col in all_columns if col.startswith('android.permission.') 
                     and col.strip() not in official_google_list]

    # 4. Constructing the Valid Table
    # We MUST keep 'applications' and 'label'
    final_column_order = ['applications'] + sorted(valid_perms) + ['label']
    
    if len(valid_perms) == 0:
        print("\n❌ CRITICAL ERROR: Still no matches!")
        print(f"Your CSV has headers like: {all_columns[1:3]}")
        print("Please check if your CSV uses different capitalization or prefixes.")
        return

    df_strict = df[final_column_order]

    # 5. Save the final file
    try:
        df_strict.to_csv(strict_output, index=False)
        print("\n" + "="*50)
        print("              STRICT CLEANING COMPLETE")
        print("="*50)
        print(f"Official Perms RETAINED:         {len(valid_perms)}")
        print(f"Invalid/Custom Perms REMOVED:    {len(invalid_perms)}")
        print(f"Total Columns in New File:       {len(df_strict.columns)}")
        print(f"Saved to: {os.path.basename(strict_output)}")
        print("="*50)
    except PermissionError:
        print(f"❌ ERROR: Close {os.path.basename(strict_output)} in Excel and run again!")

if __name__ == "__main__":
    perform_strict_cleaning()