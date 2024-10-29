import os
import json
import sys
from datetime import datetime
import socket

CONFIG_FILE = 'track_changes.json'

def get_directory_state(directory):
    state = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            state[filepath] = {
                "mtime": os.stat(filepath).st_mtime,
                "size": os.stat(filepath).st_size
            }
    return state

def save_state(state, state_file, metadata):
    state_with_metadata = {
        "metadata": metadata,
        "state": state
    }
    with open(state_file, 'w') as f:
        json.dump(state_with_metadata, f, indent=4)

def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f).get('state', {})
    return {}

def archive_state(name, data_path):
    state_file = os.path.join(data_path, f'{name}_state.json')
    archive_dir = os.path.join(data_path, 'archive')
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_file = os.path.join(archive_dir, f'{name}_state_{timestamp}.json')
    if os.path.exists(state_file):
        os.rename(state_file, archive_file)

def compare_states(old_state, new_state):
    added = [file for file in new_state if file not in old_state]
    removed = [file for file in old_state if file not in new_state]
    modified = [file for file in new_state if file in old_state and 
                (new_state[file]['mtime'] != old_state[file]['mtime'] or new_state[file]['size'] != old_state[file]['size'])]
    return added, removed, modified

def monitor_directory(name, directory, data_path):
    state_file = os.path.join(data_path, f'{name}_state.json')
    
    # Load the old state before archiving
    old_state = load_state(state_file)
    # Archive the old state before saving the new one
    archive_state(name, data_path)
    
    new_state = get_directory_state(directory)
    
    added, removed, modified = compare_states(old_state, new_state)

    print(f"Monitoring {name} ({directory})")
    print("Added:")
    for file in added:
        print(f"  {file}")

    print("Removed:")
    for file in removed:
        print(f"  {file}")

    print("Modified:")
    for file in modified:
        print(f"  {file}")

    # Collect metadata
    metadata = {
        "run_timestamp": datetime.now().isoformat(),
        "job_name": name,
        "directory": directory,
        "machine_name": socket.gethostname()
    }

    # Save the new state after archiving the old state
    save_state(new_state, state_file, metadata)

def main(name=None):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    data_path = config.get("data_path", ".")

    if name:
        for monitor in config['monitoring']:
            if monitor['name'] == name:
                monitor_directory(monitor['name'], monitor['directory'], data_path)
                break
    else:
        for monitor in config['monitoring']:
            monitor_directory(monitor['name'], monitor['directory'], data_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
