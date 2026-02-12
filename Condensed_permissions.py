import pandas as pd
import os
import csv
from tqdm import tqdm

csv_folder = r'C:\Users\Janshrut\Desktop\Sem2\datasets'
output_path = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix_OFFICIAL.csv'
csv_files = [
    'benign_permissionsSet1.csv', 'benign_permissionsSet2.csv', 
    'benign_permissionsSet3.csv', 'benign_permissionsSet4.csv',
    'malware_permissionsSet1.csv', 'malware_permissionsSet2.csv'
]

# Phase 1: Identify ONLY official Android Permissions
print("Phase 1: Scanning and Filtering for official Android permissions")
official_perm = set()
found_files = []

for filename in csv_files:
    filepath = os.path.join(csv_folder, filename)
    if os.path.exists(filepath):
        found_files.append(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            header = next(csv.reader(f))
            for col in header:
                if col.startswith('android.permission.'):
                    official_perm.add(col)
                    
sorted_perms = sorted(list(official_perm))
final_cols = ['applications'] + sorted_perms + ['label']
print(f"Filtering complete. Official permissions found: {len(sorted_perms)}")

# Phase 2: Building the Matrix
print("Phase 2: Building Standardized Matrix...")
with open(output_path, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=final_cols)
    writer.writeheader()
    
    for file_path in found_files:
        filename = os.path.basename(file_path)
        current_label = 1 if 'malware' in filename.lower() else 0
        
        num_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')) - 1
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            reader = csv.DictReader(f_in)
            for row in tqdm(reader, total=num_rows, desc=f"Processing {filename}"):
                output_row = {col: 0 for col in sorted_perms}
                output_row['applications'] = row.get('App_Name') or row.get('applications')
                output_row['label'] = current_label
                
                for p in sorted_perms:
                    if row.get(p) == '1':
                        output_row[p] = 1
                writer.writerow(output_row)

# --- NEW: Phase 3: Final De-duplication ---
print("\nPhase 3: Removing duplicate application entries...")
final_df = pd.read_csv(output_path)
original_count = len(final_df)

# Drop rows where the 'applications' name is identical
final_df.drop_duplicates(subset=['applications'], keep='first', inplace=True)
new_count = len(final_df)

final_df.to_csv(output_path, index=False)
print(f"Success! Removed {original_count - new_count} duplicate rows.")
print(f"Final dataset saved at: {output_path}")
