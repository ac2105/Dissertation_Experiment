import pandas as pd
import os
import csv
from tqdm import tqdm

csv_folder = r'C:\Users\Janshrut\Desktop\Sem2\datasets'
output_path = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix_CLEAN.csv'
csv_files = [
    'benign_permissionsSet1.csv', 'benign_permissionsSet2.csv', 
    'benign_permissionsSet3.csv', 'benign_permissionsSet4.csv',
    'malware_permissionsSet1.csv', 'malware_permissionsSet2.csv'
]

# Phase 1: Identify CLEAN unique permissions
print("Phase 1: Scanning and cleaning permission headers...")
clean_permissions = set()
found_files = []

for file_name in csv_files:
    file_path = os.path.join(csv_folder, file_name)
    if os.path.exists(file_path):
        found_files.append(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            header = next(csv.reader(f))
            for col in header:
                if col not in ['App_Name', 'applications', 'label', 'Unnamed: 0']:
                    # Extract only the last part (e.g., C2D_MESSAGE)
                    clean_name = col.split('.')[-1]
                    clean_permissions.add(clean_name)

sorted_clean_perms = sorted(list(clean_permissions))
# Condition 1: columns: applications, unique permissions, label
final_columns = ['applications'] + sorted_clean_perms + ['label']
print(f"Unique permissions reduced from ~48k to: {len(sorted_clean_perms)}")

# Phase 2: Building Master Matrix
print("Phase 2: Building Clean Master Matrix...")
with open(output_path, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=final_columns)
    writer.writeheader()

    for file_path in found_files:
        file_name = os.path.basename(file_path)
        # Condition 3: label, 0=benign, 1=malware
        current_label = 1 if 'malware' in file_name.lower() else 0
        
        num_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')) - 1
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            reader = csv.DictReader(f_in)
            for row in tqdm(reader, total=num_rows, desc=f"Processing {file_name}"):
                # Condition 2: Initialize with 0
                output_row = {col: 0 for col in sorted_clean_perms}
                output_row['applications'] = row.get('App_Name') or row.get('applications')
                output_row['label'] = current_label
                
                # Flip to 1 if the cleaned permission name matches
                for raw_perm, value in row.items():
                    if value == '1' and raw_perm not in ['App_Name', 'applications', 'label']:
                        clean_key = raw_perm.split('.')[-1]
                        if clean_key in output_row:
                            output_row[clean_key] = 1
                
                writer.writerow(output_row)

print(f"\n✅ SUCCESS! Cleaned dataset saved at: {output_path}")
