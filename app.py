import os
import fnmatch
import json
import sqlite3
import shutil
from datetime import datetime, timedelta

def list_profiles(directory_path, input_name):
    try:
        entries = os.listdir(directory_path)
        count = 1

        folders = (entry for entry in entries if
                   os.path.isdir(os.path.join(directory_path, entry)) and
                   fnmatch.fnmatch(entry, f"{input_name} {count}") and
                   (count := count + 1))

        return ['Default'] + list(folders)

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Use a generator function for extracting user info
def extract_user_info(Preferences):
    try:
        with open(Preferences, 'r', encoding='utf-8') as file:
            data = json.load(file)
            account_info = data.get('account_info', [])
            return {
                "account_id": account_info[0].get('account_id', ''),
                "full_name": account_info[0].get('full_name', ''),
                "email": account_info[0].get('email', ''),
                "profile_img": account_info[0].get('last_downloaded_image_url_with_size', ''),
                "locale": account_info[0].get('locale', '')
            } if account_info else {}

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        return {}

# Use a generator function for extracting history
def extract_history(history_path):
    try:
        connection = sqlite3.connect(history_path)
        cursor = connection.cursor()

        query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC"
        cursor.execute(query)

        for row in cursor.fetchall():
            url, title, last_visit_time = row

            last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
            # except OverflowError:
                # Handle overflow gracefully, set a default value, or skip the entry
                # last_visit_time = datetime(1970, 1, 1)

            yield {
                'Title': title,
                'Url': url,
                'Last Visited': last_visit_time
            }

    except sqlite3.Error as e:
        print(f"Error reading Chrome history database: {e}")
    finally:
        if connection:
            connection.close()

# Use streaming output for report generation
def export_report(file_name, history_generator):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            for entry in history_generator:
                file.write(str(entry) + '\n')
        
        # Remove the temporary history file
        if os.path.exists('Report\\History'):
            os.remove('Report\\History')
        print("File Exported Successfully")
    
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")

def Copy(src, dest, file_name):
    source_file_path = os.path.join(src, file_name)
    destination_directory = dest

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    destination_file_path = os.path.join(destination_directory, file_name)

    try:
        shutil.copy(source_file_path, destination_file_path)
        print(f"File '{file_name}' copied successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# ... Other functions remain unchanged ...

browser_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\")

if __name__ == "__main__":
    print("Current Browser: Google Chrome")
    print("Choose Profiles Exists:\n")

    profile_names = list_profiles(browser_path, 'Profile')
    
    for count, name in enumerate(profile_names, start=1):
        print(f"{count}. {name}")

    user_input = int(input("Input index: ")) - 1
    
    selected_profile = profile_names[user_input]
    copy_source = os.path.join(browser_path, selected_profile)
    
    Copy(copy_source, "Report", 'History')
    history_generator = extract_history(os.path.join("Report", "History"))
    export_report(os.path.join("Report", "Report.md"), history_generator)
