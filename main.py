# main.py

import os
import sys
from disk_operations import detect_and_mount_disk, check_disk_space
from user_input import choose_directory, input_system_name, choose_operation
from file_operations import copy_directory

# main function
def main():
    # check if the script is being run as root, if not, re-run with sudo
    if os.geteuid() != 0:
        print("\nThis script must be run as root, re-running with sudo...")
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
        return

    # detect and mount the disk, if unsuccessful, return
    if not detect_and_mount_disk():
        return

    # choose a directory
    directory = choose_directory()

    # enter system name
    system_name = input_system_name()

    # choose an operation
    choice = choose_operation()

    # check disk space
    check_disk_space()

    # copy the directory based on the chosen operation
    copy_directory(directory, system_name, choice)

if __name__ == '__main__':
    main()
