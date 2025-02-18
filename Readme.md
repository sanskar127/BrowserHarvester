# Browser Harvester

## Overview

**Browser Harvester** is an automated Python tool designed to extract various types of data from browser profiles across multiple web browsers on your system. It supports popular browsers such as Chrome, Firefox, Edge, and others. The script scans and retrieves data including browsing history, bookmarks, extensions, saved passwords, cookies, and more. All extracted data is stored in a structured **JSON** format, making it easy to analyze, store, or integrate into other applications.

## Key Features

- **Comprehensive Data Extraction:**
   - **Browsing History:** Extract URLs, visit timestamps, and related metadata.
   - **Bookmarks:** Retrieve titles, URLs, and folder structures.
   - **Extensions:** List all installed browser extensions with detailed information.
   - ~~**Saved Passwords:** Extract credentials (dependent on platform security and browser support).~~
   - ~~**Cookies:** Capture session cookies and other cookie data.~~
   - ~~**Cache & Local Storage:** Access cache, session storage, and local storage data (for supported browsers).~~

- **Cross-Browser Compatibility:**
   - Supports multiple browsers including:
     - Google Chrome
     - Microsoft Edge
     - ~~Mozilla Firefox~~
     - ~~Brave~~
     - ~~Opera~~
     - ~~Safari~~

- **Multiple Profiles Supported:** Capable of extracting data from all available browser profiles, whether single or multiple profiles are in use.

- **Automated & Easy-to-Use:** The script is fully automated with minimal setup. Just run it, and it will handle data extraction for you.

- **JSON Output:** All extracted data is saved in an organized **JSON** file, making it convenient for review, analysis, or importing into other tools.

## Usage Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sanskar127/BrowserHarvester.git
   ```

2. **Run the Script:**
   Launch the tool by running the following command:
   ```bash
   python3 browser_harvester.py
   ```

3. **Access the Output:**
   The tool will create a JSON file named `<target_name>.json` in the current directory. This file contains the extracted data, such as browsing history, bookmarks, and more.

---

## Contributing

We welcome contributions! If you'd like to suggest improvements, add new features, or fix bugs, feel free to submit a pull request or open an issue.

---

## Disclaimer

This tool is intended for ethical, legal, and investigative purposes only. Ensure you have explicit permission to access and analyze browser data. The authors and contributors are not responsible for any misuse, unauthorized access, or illegal activities.
