import shutil
import os
import fnmatch
import json
import sqlite3
from datetime import datetime, timedelta

def get_chrome_path():
    """Returns the expanded path to the Chrome user data directory."""
    return os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\")

# Lists profiles with names similar to the input name.
def list_profiles(directory_path, input_name):
    try:
        entries = os.listdir(directory_path)
        count = 1

        # Use fnmatch to filter folders with names similar to the input name
        folders = [entry for entry in entries if os.path.isdir(os.path.join(directory_path, entry))
                   and fnmatch.fnmatch(entry, f"{input_name} {count}")
                   and (count := count + 1)]

        return ['Default'] + folders

    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for directory '{directory_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Extracts user information (full name and email) from a Chrome Preferences file.
def extract_user_info(Preferences):
    try:
        with open(Preferences, 'r', encoding='utf-8') as file:
            data = json.load(file)
            account_info = data.get('account_info', [])
            if account_info:
                return {
                "account_id" : account_info[0].get('account_id', ''),
                "full_name" : account_info[0].get('full_name', ''),
                "email" : account_info[0].get('email', ''),
                "profile_img" : account_info[0].get('last_downloaded_image_url_with_size', ''),
                "locale" : account_info[0].get('locale', '')
                }
            else:
                return {}
    except FileNotFoundError:
        print(f"Error: File '{Preferences}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from file '{Preferences}'.")
    except KeyError as e:
        print(f"Error: Key not found in Preferences file '{Preferences}': {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Unknown | Unknown"

# Copies a specified file from the source directory to a destination directory.
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

# Retrieves a list of profiles.
def profiles(src):
    profiles_value = list_profiles(src, 'Profile')
    profiles = {}

    for profile in profiles_value:
        user_info = extract_user_info(f"{src}{profile}\\Preferences")
        
        # Check if 'full_name' is present in the dictionary
        if 'full_name' in user_info:
            full_name = user_info["full_name"]
            email = user_info["email"]
        else:
            full_name = "Unknown"
            email = "Unknown"

        profiles[f"{full_name} | {email}"] = profile

    return profiles

def extract_history(history_path):
    """Extracts browsing history information from the Chrome history database."""
    try:
        # Connect to the Chrome history database
        connection = sqlite3.connect(history_path)
        cursor = connection.cursor()

        # Execute a query to retrieve history data
        query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC"
        cursor.execute(query)

        # Fetch all the results
        history_data = cursor.fetchall()
        result = []

        for row in history_data:
            url, title, last_visit_time = row
            last_visit_time = datetime(1601, 1, 1) + timedelta(seconds=last_visit_time)
            
            entry = {
                'Title': title,
                'Url': url,
                'Last Visited': last_visit_time
            }
            result.append(entry)

        connection.close()
        # Remove the temporary history file
        if os.path.exists('Report\\History'):
            os.remove('Report\\History')

        return result

    except sqlite3.Error as e:
        print(f"Error reading Chrome history database: {e}")
    finally:
        # Close the database connection
        if connection:
            connection.close()

def generate_report():
    print("Report Generated Successfully!")

def export_report(file_name, body):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(body)
            print("File Exported Successfully")
    
    except FileNotFoundError:
        print(f"Error: {FileNotFoundError} in {file_name} File!")
    except PermissionError:
        print(f"Error: Permission denied. Make sure you have the necessary permissions.")


def setup(selected_index, src):
    """Sets up the script by copying the history file and extracting history information."""
    get_profiles = profiles(src)
    selected_profile = get_profiles[selected_index]
    
    Copy(f"{src}{selected_profile}\\", "Report", 'History')
    history = extract_history('Report\\History')
    
    export_report("Report\\Report.txt", str(history))
    # print(type(str_history))
    
if __name__ == "__main__":
    print("Current Browser: Google Chrome")
    print("Choose Profiles Exists:")
    print()

    profile_names = list(profiles(get_chrome_path()).keys())
    count = 1

    for count, name in enumerate(profile_names, start=1):
        print(f"{count}. {name}")

    user_input = int(input("Input index: "))
    
    setup(profile_names[user_input+1], get_chrome_path())
    
    # export_report("Report\\Report.md", "# Hello There This is used to testing the write method in python")
    # print(profile_names[user_input])

    # print(set_profiles(get_chrome_path()))
    # set_profiles(get_chrome_path())

    # user_info = set_profiles(get_chrome_path())

    # print(user_info)
    # get_profiles(get_chrome_path())
