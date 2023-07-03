# import required libraries
import os
import shutil
import subprocess
import sys
import pandas as pd
from pathlib import Path

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


# function to detect and mount the disk
def detect_and_mount_disk():
    # get a list of all partitions
    partitions = subprocess.check_output(['lsblk', '-o', 'LABEL']).decode().split('\n')
    
    # if 'Disk Backup' not in partitions, print error and return False
    if 'Disk Backup' not in partitions:
        print("\nDisk Label is not detected")
        return False

    print("\nDisk Backup is detected")

    # get the path of the disk
    disk_path = subprocess.check_output(['findfs', 'LABEL=Disk Backup']).decode().strip()

    # unmount the disk (if it is already mounted)
    subprocess.run(['umount', disk_path], check=False)

    # mount the disk at /mnt
    subprocess.run(['mount', disk_path, '/mnt'], check=True)

    print("Disk Backup is mounted")
    return True


# function to choose a directory
def choose_directory():
    while True:
        # get user input for directory name
        directory = input("\nEnter directory name to copy: ")

        # construct the path
        path = os.path.join('/home', directory)

        # if the directory exists, return the path
        if os.path.isdir(path):
            return path

        print("\nInvalid directory, please try again.")


# function to input system name
def input_system_name():
    system_name = input("\nWhich system name do you want to store the directory name? ")
    return system_name


# function to choose an operation
def choose_operation():
    while True:
        print("Please choose the operation:")
        print("1. Copy from current system to Disk Backup")
        print("2. Copy from Disk Backup to current system")
        
        # get user input for the choice
        choice = input("\nEnter your choice (1 or 2): ")

        # if the choice is valid, return it
        if choice in ['1', '2']:
            return choice

        print("\nInvalid choice, please enter 1 or 2.")


def check_disk_space():
    # get the disk usage for the system and the backup disk
   
    system_usage = shutil.disk_usage('/')
    backup_usage = shutil.disk_usage('/mnt')

    # convert the disk usages to gigabytes
    system_usage_gb = [i / (1024**3) for i in system_usage]
    backup_usage_gb = [i / (1024**3) for i in backup_usage]

    # create a pandas DataFrame
    df = pd.DataFrame({
        'Running System': ['Total: {:.2f} GB'.format(system_usage_gb[0]),
                           'Used: {:.2f} GB'.format(system_usage_gb[1]),
                           'Free: {:.2f} GB'.format(system_usage_gb[2])],
        'Disk Backup': ['Total: {:.2f} GB'.format(backup_usage_gb[0]),
                        'Used: {:.2f} GB'.format(backup_usage_gb[1]),
                        'Free: {:.2f} GB'.format(backup_usage_gb[2])]
    }, index=['Total', 'Used', 'Free'])

    # print the DataFrame
    print("\nDisk Space Usage:")
    print(df)

# function to copy directory
def copy_directory(directory, system_name, choice):
    # if choice is '1', set source as chosen directory and destination to '/mnt/home/{system_name}/{user_directory}'
    if choice == '1':
        source = directory
        dest = os.path.join('/mnt/home', system_name, os.path.basename(directory))
        if not os.path.exists(dest):
            os.makedirs(dest)
    # if choice is '2', set source as '/mnt/home/{system_name}/{user_directory}' and destination as '/home/NewUser/{system_name}/{user_directory}'
    else:
        source = os.path.join('/mnt/home', system_name, os.path.basename(directory))
        if not os.path.exists(source):
            print(f"\nThe directory {source} doesn't exist on the backup disk.")
            return
        dest = os.path.join('/home/NewUser', system_name, os.path.basename(directory))
        if not os.path.exists(dest):
            os.makedirs(dest)

    # Get size of the directory in GB
    directory_size_output = subprocess.run(['du', '-sb', source], stdout=subprocess.PIPE)
    directory_size_gb = int(directory_size_output.stdout.decode('utf-8').split()[0]) / (1024**3)

    # Get free disk space in GB
    if choice == '1':
        free_space_output = shutil.disk_usage('/mnt')
    else:
        free_space_output = shutil.disk_usage('/home/NewUser')
    free_space_gb = free_space_output.free / (1024**3)

    # If directory size is greater than available space - 10GB, print error message and return
    if directory_size_gb > free_space_gb - 10:  # leaving 10GB buffer space
        print("\nCan't copy directory because there is not enough free space to copy directory. "
            "Please check manually on Terminal (sudo gparted) command and check if there is unallocated space... "
            "If there is unallocated space on the source disk, you can extend the main partition size. "
            "Run the script again. If the directory size is still larger than the free space that remains,"
            "You won't be able to copy")

        return

    print(f"\nThe size of the directory is: {directory_size_gb:.2f} GB")
    print(f"\nCopying {source} to {dest}")

    # run rsync to copy the directory, existing files with the same name in the destination will be overwritten
    subprocess.run(['rsync', '-a', '--info=progress2', source + '/', dest], check=True)

    print("\nSuccessful copying. Thank you!")

# run the main function if the script is run directly
if __name__ == '__main__':
    main()
