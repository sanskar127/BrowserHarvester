import os, json
from datetime import datetime
from utils import Windows, Unix
from browser import Chrome, Firefox, Edge, Opera

TARGET_CLASS_MAP = {
    'nt' : Windows(),
    'posix': Unix()
}

BROWSER_CLASS_MAP = {
    'chrome': Chrome(os.name),
    'firefox': Firefox(os.name),
    'edge': Edge(os.name),
    'opera': Opera(os.name)
}

# BROWSER_MAP = {
#     'chrome': "Google Chrome",
#     'firefox': "Mozilla Firefox",
#     'edge': "Microsoft Edge",
#     'opera': "Opera"
# }

# Use streaming output for report generation
def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def export(target_file: str, information_dict: dict):
    try:
        output_file = target_file + ".json"
        with open(output_file, 'w', encoding='utf-8') as file:
            # Convert the dictionary to a JSON-formatted string
            data = json.dumps(information_dict, ensure_ascii=False, default=default_serializer)
            file.write(data + '\n')
        print("File Exported Successfully")

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        
def main():
    data: dict = {}
    try:
        # Gathering Target Information
        target: Windows | Unix = TARGET_CLASS_MAP.get(os.name)
        data["target"] = target.info
        data["browser"] = []

        for entry in target.browser_list():
            browser = BROWSER_CLASS_MAP.get(entry)

            profiles = []
            for profile in browser.list_profiles():
                profiles.append({ str(profile) : {
                    "profile_info": browser.profile_parser(profile),
                    "extensions": browser.get_extensions(profile),
                    "history": browser.get_history(profile),
                    "bookmarks": browser.get_bookmarks(profile)
                }})
            data["browser"].append({ str(entry): profiles})

    except Exception as e:
        print(e)
        ...

    filename = data["target"]["target_name"]
    export("thinkbook14", data)

if __name__ == "__main__":
    main()
