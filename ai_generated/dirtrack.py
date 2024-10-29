import os
import json
from datetime import datetime

# Directory to monitor
DIRECTORY_TO_MONITOR = 'c:/users/mpwilson/srctree/python/skunkworks'
STATE_FILE = 'c:/users/mpwilson/data.dev/dirtrack/directory_state.json'

def get_directory_state(directory):
    state = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            state[filepath] = os.stat(filepath).st_mtime
    return state

def save_state(state, state_file):
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4)

def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return {}

def compare_states(old_state, new_state):
    added = [file for file in new_state if file not in old_state]
    removed = [file for file in old_state if file not in new_state]
    modified = [file for file in new_state if file in old_state and new_state[file] != old_state[file]]
    return added, removed, modified

def main():
    new_state = get_directory_state(DIRECTORY_TO_MONITOR)
    old_state = load_state(STATE_FILE)

    added, removed, modified = compare_states(old_state, new_state)

    print("Added:")
    for file in added:
        print(f"  {file}")

    print("Removed:")
    for file in removed:
        print(f"  {file}")

    print("Modified:")
    for file in modified:
        print(f"  {file}")

    save_state(new_state, STATE_FILE)

if __name__ == "__main__":
    main()
