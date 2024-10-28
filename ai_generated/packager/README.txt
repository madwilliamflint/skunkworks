Packaging Script - README
Overview

This project provides a Python script (package.py) to create zip packages from files listed in a manifest file. The script offers robust command-line argument processing and handles various customization options.
Key Features

    Manifest File Parsing:

        Parses a manifest file (manifest.lst by default).

        Handles lines starting with # as attributes (e.g., project name, version, package type).

        Supports wildcards and recursive globbing (**).

    Package Attributes:

        # Project: Specifies the project name.

          - Optional (but recommended.)  If the project field is included and a specific zip 
            file name isn't specified, one will be generated using a "sanitized" version of 
            the project name as a base (with some other potential additions.)  The sanitization
            function replaces every character that is not a-z, A-Z, 0-9, '_' or '-' with an 
            underbar character '_'. 


        # Version: Specifies the version number.

          - Optional.  If it exists, the Version field will be appended to the base of the zip
            file name.  This value is not examined or parsed.  It's just included in to the
            string itself.

        # PackageType: If backup, prepends backup. to the filename.

          - Optional: (But must have a nonblank string of some sort.)

            if PackageType is included AND it's "backup" (case sensitive) then "backup." will
            be prepended to the zip filename generated.  I added this so that I could specify
            a full directory backup "manifest" file that wouldn't interfere with the "deploy"
            manifest. (In hindsight, a --backup switch might have been more appropriate.  But
            even I don't always want all files.  Particularly in the event that I keep prior
            packages in a subdirectory.)

        # BuildNumber: Appends the build number to the filename and increments it.

          - Optional! (but must have an unquoted integer value.)

            If "BuildNumber: N" exists, the script will append ".N" before the .zip AND rewrite
            the manifest file to increment that build number.  This is a strictly optional field.
            If it's not there then no build number field will be included, incremented, or
            referenced at all.

    File Naming:

        Automatically sanitizes filenames.

        Uses project name, version, and build number to generate the zip filename if not provided.

        Ensures .zip extension.

    Logging:

        Creates a package.log file containing package details.

        Includes project name, version, attributes, file details (size, last modified).

        Adds package.log to the zip file and deletes it afterward.

    Sample Manifest Generation:

        Generates a sample.manifest.lst file with blank header entries and a recursive list of files in the current directory.

        Returns an error if sample.manifest.lst already exists.

Command-Line Usage

python package.py [-m MANIFEST] [-o OUTPUT] [--generate-sample] [--help]

    -m, --manifest: Path to the manifest file (default: manifest.lst).

    -o, --output: Name of the output zip file.

    --generate-sample: Generate a sample manifest file.

    --help: Show this help message and exit.

Usage Examples:


Default Manifest (manifest.lst), Custom Zip:

       python package.py -o custom.zip

Custom Manifest, Default Zip Name:

       python package.py -m custom_manifest.lst

Custom Manifest and Custom Zip:

       python package.py -m custom_manifest.lst -o custom.zip

Generate Sample Manifest

         python package.py --generate-sample


Example of a simple manifest file with all the trimmings:


manifest.lst

# Project: MyProject
# Version: 1.0.0
# PackageType: whatever you want here
# BuildNumber: 1
# Author: Your Name

subdirectory\file1.txt
file_1.py
file_2.backup

This will generate a file called "myproject.1.0.0.1.zip" with 4 files in it.  

- The three specified above.
- package.log containing the details of the package itself.

Note:  When you re-examine "manifest.lst" you'll notice that the BuildNumber has incremented.


A simpler (but more interesting) sample for the same project.

backup.lst

# Project: MyProject
# Version: 1.0.0
# PackageType: backup
# BuildNumber: 1
# Author: Your Name

subdirectory\file1.txt
*

This will generate a file called "backup.myproject.1.0.0.1.zip" with all files in the current 
working directory in it.  Note that this IS recursive.  So EVERYTHING underneath the given 
cwd is stored in the zip file.



Notes:

        - The "header" sections described in the above examples are completely optional.  The 
          script can be run with a simple "one per line" list of files, including wildcards.

        
