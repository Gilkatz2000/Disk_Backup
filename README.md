# README.md
# Project Overview

This project is a script-based tool developed in Python for managing disk operations, specifically targeting the backup and retrieval of directories in your system. This tool makes sure it's run as root, identifies and mounts a disk labeled as "Disk Backup", prompts user interaction for directory selection and system name, allows the user to choose between backup or retrieval operations, checks the disk space, and finally, carries out the chosen operation. The system is divided into four main python files each focusing on a different functionality.

# File Descriptions
main.py

This is the primary entry point of the application, which handles the control flow of the program. It orchestrates the different functionalities implemented in other modules such as disk operations, user input, and file operations. The script needs to be run with root permissions, and if it's not, it reruns itself with sudo.
disk_operations.py

This file includes functions to interact with the disk system:

    detect_and_mount_disk(): This function identifies a disk with a specific label 'Disk Backup', unmounts it if it's already mounted, and mounts it at '/mnt'.
    check_disk_space(): This function checks the disk usage of the system and the backup disk and presents the data as a pandas DataFrame.

user_input.py

This file is responsible for handling user interactions:

    choose_directory(): This function prompts the user to enter a directory name to copy, which should exist in '/home' directory.
    input_system_name(): This function asks the user to input a system name where the directory name will be stored.
    choose_operation(): This function lets the user choose between copying from the current system to Disk Backup (option 1) or vice versa (option 2).

file_operations.py

This file contains functions to manage file operations:

    copy_directory(directory, system_name, choice): Depending on the user's choice, this function copies a directory from the current system to Disk Backup (if choice is '1') or from Disk Backup to the current system (if choice is '2'). It checks for sufficient free space before the copying process and uses rsync command to perform the copying.

# Usage

    Run python3 main.py with root privileges in the terminal.
    Follow the prompts to provide necessary inputs such as directory name, system name, and operation choice.
    The chosen operation will be executed, and informative outputs will be displayed in the terminal.

# Dependencies

The script uses the following Python libraries, which need to be installed in the Python environment:

    os: Provides a way of using system dependent functionality.
    sys: Used to exit the program and access command-line arguments.
    subprocess: Used to run new applications or programs through Python code by creating new processes.
    shutil: Provides a number of high-level operations on files and collections of files.
    pandas: Used for creating and printing a DataFrame of system and backup disk usage.

The script also requires sudo access and utilities such as lsblk, findfs, umount, mount, du, and rsync available in the system.

# Requirements
System Requirements

    Unix-based operating system: The script is designed to function with Unix-based systems. It uses various Unix-specific commands which may not be available or function differently on other operating systems.

Software Requirements

    Python 3.6 or above: The script is written in Python, and it uses some features and functionalities which are available in Python 3.6 and later versions. You can download it from the official Python website.

    Bash utilities: The following utilities should be pre-installed and available in the system's PATH. They are typically included by default in most Unix-based systems.
        sudo: Provides temporary privileges for administrative tasks.
        lsblk: Lists information about all or the specified block devices.
        findfs: Finds a filesystem by label or UUID.
        umount: Unmounts file systems.
        mount: Mounts a filesystem.
        du: Estimates and reports file and directory space usage.
        rsync: A fast, versatile, remote (and local) file-copying tool.

Python Libraries

You will need the following Python libraries installed. You can install these packages using pip, a package manager for Python. Here's how to install them:

bash

pip install pandas

    os: This is a standard Python library and it doesn't require separate installation.
    sys: This is a standard Python library and it doesn't require separate installation.
    subprocess: This is a standard Python library and it doesn't require separate installation.
    shutil: This is a standard Python library and it doesn't require separate installation.
    pandas: A powerful data manipulation library. This needs to be installed separately as mentioned above.

# Permissions

The script needs to be run with root permissions. This is important because mounting and unmounting filesystems, as well as certain types of file copying operations, typically require root privileges.
Disk Requirements

The script requires a disk labeled 'Disk Backup' to be attached to the system for the backup and restore operations. The disk should have enough free space to accommodate the directory being backed up. Similarly, the system should have sufficient free space if a directory is being restored from the backup disk. The script checks for available space before performing operations and will abort if there's not enough space.

# Note

This tool is developed to function specifically with Unix-based systems. Its functionality might not be fully compatible or may require modifications to work with other types of operating systems.
