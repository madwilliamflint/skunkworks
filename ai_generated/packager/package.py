import os
import sys
import zipfile
import datetime
import re
import glob
import argparse

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def normalize_path(path):
    return os.path.normpath(path)

def generate_sample_manifest(manifest_file="sample.manifest.lst"):
    if os.path.exists(manifest_file):
        print(f"Error: Sample manifest file '{manifest_file}' already exists.")
        sys.exit(1)
    headers = [
        "# Project: projectname",
        "# Version: 0.0.1",
        "# PackageType: sample",
        "# BuildNumber: 1",
        "# Author: Me, myself, and I",
    ]
    with open(manifest_file, 'w') as mf:
        for header in headers:
            mf.write(f"{header}\n")
        for root, dirs, files in os.walk("."):
            for name in files:
                mf.write(f"{os.path.join(root, name)}\n")
    print(f"Sample manifest file '{manifest_file}' generated successfully.")

def parse_manifest(manifest_file):
    with open(manifest_file, 'r') as mf:
        lines = [line.strip() for line in mf.readlines()]
        project_name = version = ""
        package_type = ""
        build_number = None
        attributes = {}
        files = set()
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("# Project:"):
                project_name = line.split(":")[1].strip()
                if project_name == '':
                    project_name = None
            elif line.startswith("# Version:"):
                version = line.split(":")[1].strip()
                if version == '':
                    version = None
            elif line.startswith("# PackageType:"):
                package_type = line.split(":")[1].strip()
                if package_type == '':
                    package_type = None
            elif line.startswith("# BuildNumber:"):
                build_number = int(line.split(":")[1].strip())
                lines[i] = f"# BuildNumber: {build_number + 1}"
                if build_number == '':
                    build_number = None
            elif line.startswith("#"):
                # Had to turn this in to a key value pair.
                (k,v) = [token.strip() for token in line[1:].split(':',2)]
                if len(k) and len(v):
                    attributes[k] = v

                #attributes.append(line.strip().split(': '))
                #attributes.append(line)
            elif line and not line.startswith("#"):
                # Expand wildcards
                if "**" in line:
                    matched_files = glob.glob(line, recursive=True)
                else:
                    matched_files = glob.glob(line, recursive=False)

                # Should take care of dupes.
                normalized_files = {normalize_path(f) for f in matched_files}
                files.update(normalized_files)

                #files.extend(matched_files)
        return project_name, version, package_type, build_number, attributes, files, lines

def print_usage(error_text=None):
        
    usage = """    Usage: python package.py [-m MANIFEST] [-o OUTPUT] [--generate-sample] [--help]
    
    Create a zip package from files listed in a manifest.
    
    Options:
      -m, --manifest       Path to the manifest file (default: manifest.lst)
      -o, --output         Name of the output zip file
      --generate-sample    Generate a sample manifest file
      --help               Show this help message and exit
    """

    if error_text:
        usage = "\nERROR: {0}\n\n".format(error_text) + usage

    print(usage)

def print_usage_no_project():
    text = """
    No zip filename was specified and the Project field in the manifest 
    file is either missing or blank.  I need to call this SOMEthing.  

    Maybe generate a sample manifest and try again?

"""
    print_usage()
    sys.exit(1)

        
def create_zip(zip_name, manifest_file,dest_dir):
    project_name, version, package_type, build_number, attributes, files, updated_lines = parse_manifest(manifest_file)

    print("create_zip('{0}','{1}','{2}')".format(zip_name,manifest_file,dest_dir))
    # Use sanitized project name and version if zip_name is not provided

    if not zip_name:
        if project_name is None:
            print_usage_no_project()
        zip_name = sanitize_filename(f"{project_name}_{version}")
    
    # Append build number if it exists
    if build_number is not None:
        zip_name += f".{build_number}"
    
    # Prepend "backup." if PackageType is backup
    if package_type and package_type.lower() == "backup":
        zip_name = "backup." + zip_name
    
    # Ensure .zip extension
    zip_name += ".zip"

    # Full path for the zip file
    zip_name = os.path.join(dest_dir, zip_name)    
    print("Zip name [{0}]".format(zip_name))
    
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        with open('package.log', 'w') as logf:
            logf.write(f"Project: {project_name}\n")
            logf.write(f"Version: {version}\n")
            logf.write(f"Package created on: {datetime.datetime.now()}\n")
            for key in attributes:
                logf.write("{0}: {1}\n".format(key,attributes[key]))
                #logf.write(f"{attr}\n")
            logf.write("\nFiles included in the package:\n")
            logf.write("File Path, Size (bytes), Last Modified\n\n")

            for file_path in files:
                if os.path.exists(file_path):
                    print(f"Adding {file_path} to {zip_name}")
                    zipf.write(file_path, arcname=file_path)
                    file_info = os.stat(file_path)
                    logf.write(f"{file_path}, {file_info.st_size}, {datetime.datetime.fromtimestamp(file_info.st_mtime)}\n")
                else:
                    print(f"File {file_path} not found, skipping.")

        zipf.write('package.log')

    print(f"Zip file {zip_name} created successfully.")
    print(f"Project: {project_name}, Version: {version}")
    
    # Update manifest file with incremented build number
    with open(manifest_file, 'w') as mf:
        # Somewhere in the generation, this thing started adding newlines BACK in. 
        # I refuse to chase that nonsense down, so I'm doing THIS silliness now.
        stripped = [line for line in updated_lines if line.strip()]
        mf.write('\n'.join(stripped) + '\n')

    # Remove the package.log file
    os.remove('package.log')

def file_exists(filename):
    return os.path.isfile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a zip package from files listed in a manifest.")
    parser.add_argument('-m', '--manifest', type=str, default='manifest.lst', help='Path to the manifest file.')
    parser.add_argument('-o', '--output', type=str, help='Name of the output zip file.')
#    parser.add_argument('--generate-sample', action='store_true', help='Generate a sample manifest file.')
    parser.add_argument('--generate-sample', nargs='?', const='sample.manifest.lst', type=str, help='Generate a sample manifest file, optionally specify a filename')
    parser.add_argument('-d', '--destination', type=str, default='.', help='Destination directory for the zip file (default: current working directory)')

    args = parser.parse_args()

    # Pulling the command line arguments into the namespace is a little too damned cute for it's own good.
    # I'd really rather it be in an explicit dictionary so no games were being played.  But whatever.

    if args.generate_sample:
        generate_sample_manifest(args.generate_sample)
        sys.exit(0)
        
    try:
        #print("Manifest file reading as [{0}]".format(args.manifest))
        if not file_exists(args.manifest):
            print_usage("Default manifest file [{0}] does not exist and none other was specified.".format(args.manifest))
            sys.exit(1)
        
        if args.generate_sample:
            generate_sample_manifest(args.manifest)
        else:
            print("Creating zip...")
            create_zip(args.output, args.manifest,args.destination)

    except Exception as e:
        print("An error occurred: [{0}]".format(e))
        print("\n")
        print_usage()
        sys.exit(1)
