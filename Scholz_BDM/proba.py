# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:23:50 2017

@author: internet
"""

import os

def rename_file():
    # get file names from a folder
    file_list = os.listdir(r"C:\Users\win10\Pictures\prank")
    print(file_list)
    
rename_file()

file_name = "48athen"
print(file_name)

new_file_name = file_name.strip("0123456789")
print(new_file_name)

import os
save_path = os.getcwd()
print("Current working directory is: "+save_path)

os.chdir(r"c:\DEV\Python\Scholz_BDM")
new_directory = os.getcwd()
print("New working directory is: "+new_directory)    