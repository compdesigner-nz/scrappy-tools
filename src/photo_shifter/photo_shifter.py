import os
import concurrent
import shutil
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog


def ask_user_for_directory() -> str:
    directory: str = ""
    while True:
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        if directory:
            return directory
        print("No directory selected")


def ask_user_for_files(ext: str | None = None) -> list[str]:
    """
    Ask the user for files with a specific extension

    Args:
        ext (str): The extension of the files

    Returns:
        list[str]: _description_
    """
    files = []
    while True:
        root = tk.Tk()
        root.withdraw()
        files: list[str] = None
        if ext is None:
            files = filedialog.askopenfilenames()
        else:
            files = filedialog.askopenfilenames(
                filetypes=[(f"{ext} files", f"*.{ext}")])
        if files is not None:
            return files


def copy_file(file_path: str, new_path: str) -> None:
    shutil.copy2(file_path, new_path)


def copy_directory(old_directory_path: str, new_directory_path: str) -> None:
    """
    Use concurrent.futures.ThreadPoolExecutor to copy all files from a directory to another directory

    Args:
        old_directory_path (str): The old directory
        new_directory_path (str): The new directory

    Raises:
        FileNotFoundError: _description_
    """
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
    if not os.path.isdir(old_directory_path):
        raise FileNotFoundError(f"{old_directory_path} is not a directory")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        files = [file for file in os.listdir(old_directory_path) if os.path.isfile(
            os.path.join(old_directory_path, file))]
        list(tqdm(executor.map(lambda file: copy_file(os.path.join(
            old_directory_path, file), os.path.join(new_directory_path, file)), files), total=len(files), desc="Copying files"))


def copy_multiple_files(files: list[str], new_directory_path: str) -> None:
    """
    Use concurrent.futures.ThreadPoolExecutor to copy all files from a directory to another directory

    Args:
        files (list[str]): The files to copy
        new_directory_path (str): The new directory

    Raises:
        FileNotFoundError: _description_
    """
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(lambda file: copy_file(file, os.path.join(
            new_directory_path, os.path.basename(file))), files), total=len(files), desc="Copying files"))


if (__name__ == "__main__"):
    files: list[str] = ask_user_for_files()
    new_directory = ask_user_for_directory()
    copy_multiple_files(files, new_directory)
