import time
import requests

def read_file(filename):
    with open(filename, 'r') as file:
        return {line.split(',', 1)[0] for line in file}

def send_to_discord(webhook_url, message):
    """Send a message to a Discord webhook."""
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

def monitor_file(filename, webhook_url, interval=60):
    print(f"Monitoring changes to the start of lines in {filename}. Press Ctrl+C to stop.")
    
    try:
        current_lines = read_file(filename)
        
        while True:
            time.sleep(interval)
            new_lines = read_file(filename)

            added = new_lines - current_lines
            removed = current_lines - new_lines

            if added:
                added_message = "Connected: " + " ".join(line for line in added if line != "UNDEF")
                print(added_message)
                send_to_discord(webhook_url, added_message)

            if removed:
                removed_message = "Disconnected: " + " ".join(line for line in removed if line != "UNDEF")
                print(removed_message)
                send_to_discord(webhook_url, removed_message)

            current_lines = new_lines

    except KeyboardInterrupt:
        print("Stopped monitoring.")
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    filename = "/var/log/openvpn/status.log"
    webhook_url = "WEB_HOOK_URL"
    monitor_file(filename, webhook_url)
