# user_input.py

import os

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