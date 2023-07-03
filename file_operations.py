# file_operations.py

import os
import subprocess
import shutil

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
            "You won't be able to copy\n")

        return

    print(f"\nThe size of the user directory is: {directory_size_gb:.2f} GB""\nStarting to copy!")
    print(f"\nCopying {source} to {dest}")

    # run rsync to copy the directory, existing files with the same name in the destination will be overwritten
    subprocess.run(['rsync', '-a', '--info=progress2', source + '/', dest], check=True)

    print("\nSuccessful copying. Thank you!")
