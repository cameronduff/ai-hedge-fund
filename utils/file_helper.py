import os
import shutil


def clear_directory(directory_path: str):
    """
    Deletes all contents (files and folders) inside the specified directory.

    Args:
        directory_path (str): Path to the target directory.
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist.")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"'{directory_path}' is not a directory.")

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # remove file or symlink
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # remove subdirectory
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")
