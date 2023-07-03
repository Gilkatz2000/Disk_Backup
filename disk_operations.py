# disk_operations.py

import subprocess
import shutil
import pandas as pd

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
