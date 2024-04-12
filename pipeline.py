import os
import subprocess

raw_data_path = 'samples/data_raw.fif'

python_files = [
    "scripts/1_0_clean_raw.py",
    "scripts/1_5_create_epochs.py",
    "scripts/2_0_clean_epochs.py",
    "scripts/2_5_create_ica.py",
    "scripts/3_0_clean_ica.py"
]

if __name__ == "__main__":
    for file in python_files:
        os.system("python " + file)