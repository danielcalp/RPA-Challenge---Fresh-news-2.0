import os
import shutil

def remove_profile_files(profile_path: str = '5if5a9hx.project_profile') -> None:
    """
    Removes all files and directories in the specified profile path,
    except for the 'storage' directory, from which only the 'permanent' subdirectory is removed.

    Args:
        profile_path (str): The path to the profile directory. Defaults to '5if5a9hx.project_profile'.
    """
    main_file = 'storage'
    file_list = os.listdir(profile_path)

    for file_name in file_list:
        file_path = os.path.join(profile_path, file_name)
        
        if file_name != main_file:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
        else:
            permanent_path = os.path.join(file_path, 'permanent')
            if os.path.exists(permanent_path):
                shutil.rmtree(permanent_path)
