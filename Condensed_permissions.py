import pandas as pd
import os
import csv
from tqdm import tqdm

csv_folder = r'C:\Users\Janshrut\Desktop\Sem2\datasets'
output_path = r'C:\Users\Janshrut\Desktop\Sem2\master_permission_matrix.csv'
csv_files = [
    'benign_permissionsSet1.csv', 'benign_permissionsSet2.csv', 
    'benign_permissionsSet3.csv', 'benign_permissionsSet4.csv',
    'malware_permissionsSet1.csv', 'malware_permissionsSet2.csv'
]

# Phase 1: Scan headers
print("Phase 1: Scanning headers...")
all_permissions = set()
found_files = []
for file_name in csv_files:
    file_path = os.path.join(csv_folder, file_name)
    if os.path.exists(file_path):
        found_files.append(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            header = next(csv.reader(f))
            perms = [c for c in header if c not in ['App_Name', 'applications', 'label', 'Unnamed: 0']]
            all_permissions.update(perms)

sorted_perms = sorted(list(all_permissions))
final_columns = ['applications'] + sorted_perms + ['label']
print(f"Total unique permissions: {len(sorted_perms)}")

# Phase 2: Writing with Progress Bar
print("Phase 2: Building Master Matrix...")
with open(output_path, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.DictWriter(f_out, fieldnames=final_columns)
    writer.writeheader()

    for file_path in found_files:
        file_name = os.path.basename(file_path)
        label = 1 if 'malware' in file_name.lower() else 0
        
        # Count rows for the progress bar
        num_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')) - 1
        
        # Use DictReader for speed and lower memory overhead
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
            reader = csv.DictReader(f_in)
            
            # This bar shows you exactly how fast it's moving
            for row in tqdm(reader, total=num_rows, desc=f"Processing {file_name}"):
                # 1. Start with a row of zeros
                output_row = {col: 0 for col in sorted_perms}
                
                # 2. Add application name and label
                output_row['applications'] = row.get('App_Name') or row.get('applications')
                output_row['label'] = label
                
                # 3. Only flip the '1's for permissions actually present
                for key, value in row.items():
                    if key in output_row and value == '1':
                        output_row[key] = 1
                
                writer.writerow(output_row)

print(f"\n✅ Done! Master file saved at: {output_path}")
