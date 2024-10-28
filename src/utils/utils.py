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


def ask_user_for_files(ext: str = None) -> list[str]:
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
        files: list[str] = []
        if ext is None:
            files = filedialog.askopenfilenames()
        else:
            files = filedialog.askopenfilenames(
                filetypes=[(f"{ext} files", f"*.{ext}")])
        if files:
            return files
        print("No files selected")
