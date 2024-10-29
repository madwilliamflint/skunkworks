import json
import os
import hashlib
from collections import defaultdict

def load_state(state_file):
    with open(state_file, 'r') as f:
        state_data = json.load(f)
    return state_data['state']

def compute_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_file_duplicates(state, deep_compare=False):
    file_map = defaultdict(list)
    duplicates = []

    for file, details in state.items():
        file_key = (os.path.basename(file), details['size'])
        file_map[file_key].append((file, details.get('sha256')))

    for file_key, files in file_map.items():
        if len(files) > 1:
            if deep_compare:
                hash_map = defaultdict(list)
                for f, existing_hash in files:
                    if existing_hash:
                        file_hash = existing_hash
                    else:
                        file_hash = compute_hash(f)
                    hash_map[file_hash].append(f)
                for file_hash, hashed_files in hash_map.items():
                    if len(hashed_files) > 1:
                        duplicates.append(hashed_files)
            else:
                duplicates.append([f for f, _ in files])

    return duplicates

def find_subdirectory_duplicates(state):
    subdir_map = defaultdict(list)
    subdir_duplicates = []

    for file in state.keys():
        subdir = os.path.dirname(file)
        subdir_map[subdir].append(file)

    for subdir, files in subdir_map.items():
        for other_subdir, other_files in subdir_map.items():
            if subdir != other_subdir and set(files) == set(other_files):
                subdir_duplicates.append((subdir, other_subdir))

    return subdir_duplicates

def main(state_file, deep_compare=False):
    state = load_state(state_file)
    
    file_duplicates = find_file_duplicates(state, deep_compare)
    subdir_duplicates = find_subdirectory_duplicates(state)

    print("Duplicate files:")
    for duplicate_set in file_duplicates:
        print(f"  {' | '.join(duplicate_set)}")

    print("Duplicate subdirectories:")
    for subdir1, subdir2 in subdir_duplicates:
        print(f"  {subdir1} and {subdir2}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python compare_trees.py <state_file> [--deep-compare]")
    else:
        state_file = sys.argv[1]
        deep_compare = "--deep-compare" in sys.argv
        main(state_file, deep_compare)
