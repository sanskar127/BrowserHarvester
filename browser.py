import os
import json
import sqlite3
import fnmatch
from datetime import datetime, timedelta


class Browser:
    def __init__(self):
        # Target files and environment variables
        self.path = ""
        self._env = {
            "history": "History",
            "bookmarks": "Bookmarks",
            "user_info": "Preferences",
            "extensions": "Extensions"
        }

    def list_profiles(self) -> list:
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"Path not found: {self.path}")

            # Start the list with "Default"
            profiles = ["Default"]

            # Add profiles matching "Profile *"
            profiles.extend(entry for entry in os.listdir(self.path)
                            if os.path.isdir(os.path.join(self.path, entry)) and fnmatch.fnmatch(entry, "Profile *"))

            return profiles
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_history(self, profile):
        history = []
        history_path = os.path.join(self.path, profile, self._env["history"])
        if not os.path.exists(history_path):
            print(f"History file not found: {history_path}")
            return []

        try:
            with sqlite3.connect(history_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
                for url, title, last_visit_time in cursor.fetchall():
                    history.append({
                        'Title': title,
                        'Url': url,
                        'Last Visited': datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
                    })
            return history
        except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
            print(f"Error reading history database: {e}")
            return []

    def get_bookmarks(self, profile):
        bookmarks_path = os.path.join(self.path, profile, self._env["bookmarks"])
        if not os.path.exists(bookmarks_path):
            print(f"Bookmarks file not found: {bookmarks_path}")
            return []

        try:
            with open(bookmarks_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return [
                {
                    'id': entry.get('id', ''),
                    'title': entry.get('name', ''),
                    'url': entry.get('url', ''),
                    'date_added': datetime(1601, 1, 1) + timedelta(microseconds=int(entry.get('date_added', 0))),
                }
                for folder in ['bookmark_bar', 'other']
                for entry in data.get('roots', {}).get(folder, {}).get('children', [])
            ]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading bookmarks: {e}")
            return []

    def get_extensions(self, profile):
        extensions_path = os.path.join(self.path, profile, self._env["extensions"])
        if not os.path.exists(extensions_path):
            print(f"Extensions directory not found: {extensions_path}")
            return []

        extensions = []
        try:
            for extension in os.listdir(extensions_path):
                ext_path = os.path.join(extensions_path, extension)
                subdirs = [d for d in os.listdir(ext_path) if os.path.isdir(os.path.join(ext_path, d))]
                if not subdirs:
                    continue

                manifest_path = os.path.join(ext_path, subdirs[0], 'manifest.json')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    extensions.append({
                        'id': extension,
                        'title': data.get('name', ''),
                        'version': data.get('version', ''),
                        'permissions': data.get('permissions', []),
                    })
            return extensions
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading extensions: {e}")
            return []

    def profile_parser(self, profile):
        # Parse the profiles
        try:
            profile_path = os.path.join(self.path, profile, self._env["user_info"])
            with open(profile_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                account_info = data.get('account_info', [])
                return {
                    "is_default": profile == 'Default',
                    "account_id": account_info[0].get('account_id', ''),
                    "profile_name": account_info[0].get('given_name', ''),
                    "full_name": account_info[0].get('full_name', ''),
                    "email": account_info[0].get('email', ''),
                    "profile_img": account_info[0].get('last_downloaded_image_url_with_size', ''),
                    "lang": account_info[0].get('locale', '')
                } if account_info else {}

        except FileNotFoundError as e:
            print(f"Profile file not found: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from profile file: {e}")
        except KeyError as e:
            print(f"Key error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


class Chrome(Browser):
    def __init__(self, target_os):
        super().__init__()
        self.path = os.path.expanduser(
            "~\\AppData\\Local\\Google\\Chrome\\User Data\\" if target_os == 'nt' else "~/.config/google-chrome/"
        )


class Firefox(Browser):
    def __init__(self, target_os):
        super().__init__()
        self.path = os.path.expanduser(
            "~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\" if target_os == 'nt' else "~/.mozilla/firefox/"
        )


class Edge(Browser):
    def __init__(self, target_os):
        super().__init__()
        self.path = os.path.expanduser(
            "~\\AppData\\Local\\Microsoft\\Edge\\User Data\\" if target_os == 'nt' else "~/.config/microsoft-edge/"
        )


class Opera(Browser):
    def __init__(self, target_os):
        super().__init__()
        self.path = os.path.expanduser(
            "~\\AppData\\Roaming\\Opera Software\\Opera Stable\\" if target_os == 'nt' else "~/.config/opera/"
        )
