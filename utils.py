# Modules
import socket, platform, http.client, subprocess


class Target:
    def __init__(self):
        try:
            self.info = {
                "target_name": platform.node(),
                "private_ip": socket.gethostbyname(socket.gethostname()),
                "public_ip": self.get_public_ip()
            }
        except Exception as e:
            print(e)

    @staticmethod
    def get_public_ip():
        try:
            conn = http.client.HTTPSConnection("api.ipify.org")
            conn.request("GET", "/")
            response = conn.getresponse()
            public_ip = response.read().decode()
            conn.close()
            return public_ip
        except Exception as e:
            return f"Error fetching public IP: {e}"

    def browser_list(self):
        pass

class Windows(Target):
    def __init__(self):
        # call parent constructor
        super().__init__()

        script = r'''
        $os = Get-CimInstance -ClassName Win32_OperatingSystem
        Write-host "$($os.Caption) $($os.OSArchitecture) $($os.BuildNumber)"
        '''

        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", script],
                capture_output=True, text=True, check=True
            )
            self.info["target_machine"] = result.stdout.strip()
        except Exception as e:
            self.info["target_machine"] = f"Error fetching OS info: {e}"

    def browser_list(self):
        script = r'''
        $browserKeys = @(
            "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
            "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
            "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
        )

        $browserNames = @("Chrome", "Firefox", "Edge", "Opera")

        $browserIdentifiers = @{
            "Chrome" = "chrome"
            "Firefox" = "firefox"
            "Edge" = "edge"
            "Opera" = "opera"
        }

        $identifiers = @()

        foreach ($keyPath in $browserKeys) {
            Get-ItemProperty $keyPath | ForEach-Object {
                foreach ($browser in $browserNames) {
                    if ($_.DisplayName -like "*$browser*" -and $_.DisplayName -notlike "*WebView*") {
                        $identifiers += $browserIdentifiers[$browser]
                    }
                }
            }
        }

        $identifiers -join " "
        '''

        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", script],
                capture_output=True, text=True, check=True
            )
            parsed_list = result.stdout.strip()
            return parsed_list.split()
        except Exception as e:
            return [f"Error fetching browser list: {e}"]


class Unix(Target):
    def __init__(self):
        # call parent constructor
        super().__init__()

        script = r'''
        #!/bin/bash

        # Get the OS name and version
        os_name=$(lsb_release -d | awk -F'\t' '{print $2}')

        # Get the architecture
        architecture=$(uname -m)

        # Print the desired format
        echo "$os_name $architecture"
        '''

        try:
            result = subprocess.run(
                ["bash", "-c", script],
                capture_output=True, text=True, check=True
            )
            self.info["target_machine"] = result.stdout.strip()
        except Exception as e:
            self.info["target_machine"] = f"Error fetching OS info: {e}"

    def browser_list(self):
        script = r'''
            #!/bin/bash

            # List of common browsers
            browsers=("chrome" "firefox" "opera" "edge")

            # Variable to hold installed browsers
            installed_browsers=""

            # Loop through each browser
            for browser in "${browsers[@]}"; do
                # Check if the browser is installed
                if which $browser > /dev/null 2>&1; then
                    # Add the browser name to the list of installed browsers
                    installed_browsers+="$browser "
                fi
            done

            # Print all installed browsers, trimming any trailing space
            echo "$installed_browsers"
        '''

        try:
            result = subprocess.run(
                ["bash", "-c", script],
                capture_output=True, text=True, check=True
            )
            parsed_list = result.stdout.strip()
            return parsed_list.split()
        except Exception as e:
            return [f"Error fetching browser list: {e}"]
