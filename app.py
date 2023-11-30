import shutil, os, fnmatch, json

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

    with open(path, 'r', encoding='utf-8') as file:
        # Load JSON data from the file
        data = json.load(file)
        return f"{((data['account_info'])[0])['full_name']} | {((data['account_info'])[0])['email']}"

def getting_files(file):
    appdata_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\")

    source_file_path = os.path.join(appdata_path, file)

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


def list_data(src):
    # src = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Preferences')
    profiles = list_profiles(src, 'Profile')
    print(profiles)
    
# list_profiles(chrome_path)

list_data(chrome_path)