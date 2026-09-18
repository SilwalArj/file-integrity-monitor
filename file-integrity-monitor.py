import hashlib
import os
import json

BASELINE_FILE = "baseline.json"

def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (FileNotFoundError, PermissionError) as error:
        print(f"Error reading '{filepath}': {error}")
        return None

def get_files(directory):

    files = []

    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                files.append(filepath)

    except (FileNotFoundError, PermissionError) as error:
        print(f"Error accessing directory: {error}")

    return files

def create_baseline(directory):

    baseline = {}

    files = get_files(directory)

    if not files:
        print("No files found.")
        return

    for filepath in files:
        file_hash = calculate_hash(filepath)

        if file_hash:
            baseline[filepath] = file_hash

    with open(BASELINE_FILE, "w") as file:
        json.dump(baseline, file, indent=4)

    print(f"Baseline created successfully")
    print(f"Files monitored: {len(baseline)}")

def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        print("No baseline found. Create a baseline first.")
        return None

    try:
        with open(BASELINE_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Baseline file is corrupted.")
        return None

def check_integrity(directory):

    baseline = load_baseline()

    if baseline is None:
        return

    current_files = get_files(directory)
    current_hashes = {}

    for filepath in current_files:
        file_hash = calculate_hash(filepath)

        if file_hash:
            current_hashes[filepath] = file_hash

    modified = []
    added = []
    deleted = []
    unchanged = []

    for filepath, original_hash in baseline.items():
        if filepath not in current_hashes:
            deleted.append(filepath)

        elif current_hashes[filepath] != original_hash:
            modified.append(filepath)

        else:
            unchanged.append(filepath)

    for filepath in current_hashes:
        if filepath not in baseline:
            added.append(filepath)

    print("=" * 45)
    print("INTEGRITY CHECK RESULTS")
    print("=" * 45)

    print(f"Unchanged : {len(unchanged)}")
    print(f"Modified: {len(modified)}")
    print(f"Added: {len(added)}")
    print(f"Deleted: {len(deleted)}")

    if modified:
        print("[!] Modified files:")

        for filepath in modified:
            print(f" -{filepath}")

    if added:
        print("[+] New files:")

        for filepath in added:
            print(f" - {filepath}")

    if deleted:
        print("[-] Deleted files:")

        for filepath in deleted:
            print(f"- {filepath}")

    if not modified and not added and not deleted:
        print("No changes detected.")

def main():
    print("=" * 45)
    print("      FILE INTEGRITY MONITOR")
    print("=" * 45)
    print("Instructions:")
    print("- Enter a file or directory path.")
    print("- For a directory, all files inside it will be monitored.")
    print("- Create a baseline before checking for changes.")
    print("=" * 45)

    while True:

        print("\n1.Create baseline")
        print("2.Check for changes")
        print("3. Exit")

        choice = input("\n Choose an option:")

        if choice == "1":

            directory =  input("Enter directory path: ")

            if not os.path.isdir(directory):
                print("Invalid directory.")
                continue

            create_baseline(directory)

        elif choice == "2":

            directory = input("Enter directory path:")

            if not os.path.isdir(directory):
                print("Invaild directory")
                continue

            check_integrity(directory)

        elif choice == "3":

            print("Exiting File Integrity Monitor.")
            break

        else:
            print("Invalid chocie.")

if __name__ == "__main__":
    main()
    