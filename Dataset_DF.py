import pandas as pd
import os

folder_path = r'C:\Users\Janshrut\Downloads\malware_complete_analysis_2\malware_complete_analysis_2'

# Get all files
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
print(f"Found {len(files)} files. Starting processing...")

data_list = []
count = 0

# Test with a limit first (e.g., [:500]) or remove [:500] to run all
for file_name in files:
    file_path = os.path.join(folder_path, file_name)
    permissions_found = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Based on your file content, we look for this specific prefix
                if 'RequiredPermission::' in line:
                    perm = line.split('RequiredPermission::')[-1].strip()
                    permissions_found.append(perm)
        
        if permissions_found:
            app_entry = {perm: 1 for perm in permissions_found}
            app_entry['App_Name'] = file_name
            data_list.append(app_entry)
            
    except Exception as e:
        pass # Silently skip files that can't be read

    count += 1
    if count % 1000 == 0:
        print(f"Processed {count}/{len(files)} files...")

# Create the DataFrame
if not data_list:
    print("Check: No 'RequiredPermission::' strings were found in any files.")
else:
    print("Building DataFrame... this may take a moment for 32k rows.")
    df = pd.DataFrame(data_list)
    df = df.fillna(0).set_index('App_Name').astype(int)
    
    print("\nSuccess! Final Dataframe Dimensions:", df.shape)
    print(df.head())
    
    # Optional: Save it so you don't have to run this long process again
    df.to_csv("malware_permissionsSet2.csv")