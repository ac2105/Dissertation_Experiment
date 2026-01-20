import pandas as pd
import os

#Folder with the csv datasets
csv_folder=r'C:\Users\Janshrut\Desktop\Sem2\datasets'

#List of csv files containing the datasets
csv_files=['benign_permissionsSet1.csv', 'benign_permissionsSet2.csv', 
    'benign_permissionsSet3.csv', 'benign_permissionsSet4.csv',
    'malware_permissionsSet1.csv', 'malware_permissionsSet2.csv']

all_permissions=[]

for filename in csv_files:
    file_path=os.path.join(csv_folder,filename)
    
    if os.path.exists(file_path):
        #Read only the header to get permission names quickly
        df_temp=pd.read_csv(file_path,nrows=0)
        
        #Get all columns except the index 'App_Name'
        permissions=[col for col in df_temp.columns if col != 'App_Name']
        
        #Determine label based on filename
        label='malware' if 'malware' in filename.lower() else 'benign'
        
        for perm in permissions:
            all_permissions.append({'Permission':perm, 'Type':label})
    else:
        print(f"Warning: {filename} not found.")

# Create a DataFrame and remove duplicates
final_df = pd.DataFrame(all_permissions).drop_duplicates()

# Sort by Permission name for readability
final_df = final_df.sort_values(by=['Permission', 'Type'])

#Save the common permissions list
output_path=os.path.join(csv_folder,'common_permissions_labeled.csv')
final_df.to_csv(output_path,index=False)

print(f"Success! Labeled common permissions saved to: {output_path}")
print(final_df.head())