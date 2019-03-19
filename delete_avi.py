import os
import sys

def list_all_folders_in_a_directory(directory):
    folder_list = (folder_name for folder_name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder_name)))
    return folder_list
    pass

def list_all_files_in_a_directory(directory):
    file_list = (file_name for file_name in os.listdir(directory)
         if os.path.isfile(os.path.join(directory, file_name)))
    return file_list
    pass

def delete_all_avi_files(current_dir):
    print("Delete .avi files:")
    file_list = list_all_files_in_a_directory(current_dir)
    for file_name in file_list:
        if ".avi" in file_name:
            print(os.path.join(current_dir, file_name))
            os.remove(os.path.join(current_dir, file_name))

    # Recursion
    folder_list = list_all_folders_in_a_directory(current_dir)
    for folder_name in folder_list:
        delete_all_avi_files(os.path.join(current_dir, folder_name))

if __name__ == '__main__':
    output_root_folder = '/home/dangmanhtruong95/NTHai/iDT_output/'
    delete_all_avi_files(output_root_folder)
