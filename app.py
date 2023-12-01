import shutil, os, fnmatch, json, sqlite3
from datetime import datetime, timedelta

chrome_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\")

def list_profiles(directory_path, input_name):
    count = 1
    try:
        entries = os.listdir(directory_path)

        # Use fnmatch to filter folders with names similar to the input name
        folders = [entry for entry in entries if os.path.isdir(os.path.join(directory_path, entry))
                            and fnmatch.fnmatch(entry, f"{input_name} {count}")
                            and (count := count + 1)
                            ]

        return folders

    except FileNotFoundError:
        print(f"Error: Directory '{directory_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for directory '{directory_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def pref_id(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            account_info = data.get('account_info', [])
            if account_info:
                full_name = account_info[0].get('full_name', '')
                email = account_info[0].get('email', '')
                return f"{full_name} | {email}"
            else:
                return "Unknown | Unknown"
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON from file '{path}'.")
    except KeyError as e:
        print(f"Error: Key not found in Preferences file '{path}': {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Unknown | Unknown"

def getting_files(file, src):

    source_file_path = os.path.join(src, file)

    destination_directory = "Report"

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    destination_file_path = os.path.join(destination_directory, file)

    try:
        # Copy the file
        shutil.copy(source_file_path, destination_file_path)
        print(f"File '{file}' copied successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def set_profiles(src):
    profiles_value = list_profiles(src, 'Profile')
    profiles = {'Default': 'Default'}

    for profile in profiles_value:
        profiles[pref_id(f"{chrome_path}{profile}\\Preferences")] = profile
        
    return profiles

def extract_history(history):

    try:
        # Connect to the Chrome history database
        connection = sqlite3.connect(history)
        cursor = connection.cursor()

        # Execute a query to retrieve history data
        query = "SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC"
        cursor.execute(query)

        # Fetch all the results
        history_data = cursor.fetchall()
        result = []

        for row in history_data:
            url, title, last_visit_time = row
            last_visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
            # print(f"URL: {url}\nTitle: {title}\nLast Visit Time: {last_visit_time}\n")
            list = {
                'Title' : title,
                'Url' : url,
                'Last Visited' : last_visit_time
            }
            result.append(list)
        
        connection.close()
        if os.path.exists('Report\\History'):
            os.remove('Report\\History')
        
        return result

    except sqlite3.Error as e:
        print(f"Error reading Chrome history database: {e}")

    finally:
        # Close the database connection
        if connection:
            connection.close()

def setup(input, src):
    profiles = ['Default']
    profiles += list_profiles(src, 'Profile')
    getting_files('History', f"{src}{profiles[input]}\\")
    history = extract_history('Report\\History')
    
    print(history)

if __name__ == "__main__":
    count = 1
    print("Current Browser: Google Chrome")
    print("Choose Profiles Exists:")
    print()
    
    for profile in set_profiles(chrome_path).keys():
        print(f"{count}. {profile}")
        count = count + 1
    
    input = int(input("Input index: "))
    
    setup(input, chrome_path)
        