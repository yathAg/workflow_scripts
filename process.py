import os
import shutil
import zipfile
import datetime

"""
This script automates the process of handling ZIP files from two user-provided directories.
It creates a new working directory named `zip1_zip2_todaysdate`, copies the ZIP files there,
extracts them, creates a new empty merged folder, and waits for user input before compressing
the merged folder into a new ZIP archive. Finally, it cleans up the extracted directories.

Example Directory Structure After Running the Script in `foo`:
If today’s date is `2025-03-09`, the structure will look like this:

foo/
│── zip1_zip2_2025-03-09/
│   │── zip1.zip
│   │── zip2.zip
│   │── zip1_extracted/
│   │── zip2_extracted/
│   │── zip1_zip2_merge/
│   │── zip1_zip2_merge.zip

- **`zip1.zip` & `zip2.zip`** → Copied from their respective folders
- **`zip1_extracted/` & `zip2_extracted/`** → Extracted contents
- **`zip1_zip2_merge/`** → Created but left empty as per your request
- **`zip1_zip2_merge.zip`** → Final compressed archive after key press

"""

# Prompt user for folder paths
folder1 = input("Enter the first folder path: ").strip('"')
folder2 = input("Enter the second folder path: ").strip('"')

# Ensure paths are treated correctly (handle Windows paths)
folder1 = os.path.normpath(folder1)
folder2 = os.path.normpath(folder2)

# Get today's date for the folder name
today_date = datetime.datetime.now().strftime('%Y-%m-%d')
working_directory = os.path.join(os.getcwd(), f"zip1_zip2_{today_date}")
os.makedirs(working_directory, exist_ok=True)

# Get the zip files inside the folders
zip1 = next((f for f in os.listdir(folder1) if f.endswith('.zip')), None)
zip2 = next((f for f in os.listdir(folder2) if f.endswith('.zip')), None)

if not zip1 or not zip2:
    print("One or both zip files not found.")
    exit(1)

# Copy zip files to the working directory
zip1_path = os.path.join(working_directory, zip1)
zip2_path = os.path.join(working_directory, zip2)
shutil.copy(os.path.join(folder1, zip1), zip1_path)
shutil.copy(os.path.join(folder2, zip2), zip2_path)

# Extract both zip files
extracted_folder1 = os.path.join(working_directory, zip1.replace(".zip", ""))
extracted_folder2 = os.path.join(working_directory, zip2.replace(".zip", ""))

with zipfile.ZipFile(zip1_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder1)

with zipfile.ZipFile(zip2_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder2)

# Create a new merged folder
merged_folder = os.path.join(working_directory, f"{zip1.replace('.zip', '')}_{zip2.replace('.zip', '')}_merge")
os.makedirs(merged_folder, exist_ok=True)

print("Press any key to compress the merged folder...")
input()

# Compress the merged folder
shutil.make_archive(merged_folder, 'zip', merged_folder)

# Clean up extracted folders
shutil.rmtree(extracted_folder1)
shutil.rmtree(extracted_folder2)

print("Process completed successfully.")