import os
import shutil

def remove_profile_files():
    profile_path = '5if5a9hx.project_profile\\'
    file_list = os.listdir(profile_path)
    main_file = 'storage'
    print(file_list)
    for file in file_list:
        file_path = os.path.join(profile_path, file)
        if file != main_file:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        else:
            shutil.rmtree(file_path + '\\permanent')
