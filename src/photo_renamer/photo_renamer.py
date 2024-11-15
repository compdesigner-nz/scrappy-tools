from os import path
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL.ExifTags import TAGS
import exiftool
from pymediainfo import MediaInfo
from tqdm import tqdm


def get_files_in_director(directory: str) -> List[str]:
    if (not path.exists(directory)):
        raise FileNotFoundError(f"Directory {directory} not found")
    files = os.listdir(directory)
    files = [os.path.join(directory, file) for file in files]
    files = [file for file in files if path.isfile(file)]
    print(f"There are {len(files)} files in the directory {directory}")
    return [path.join(directory, file) for file in files]


def generate_unique_name_from_count(custom_prefix: str, current_name: str, current_index: int) -> str:
    if (current_name.startswith(custom_prefix)):
        return current_name
    if (custom_prefix == ""):
        raise ValueError("The custom prefix must not be empty")
    if (current_name == ""):
        raise ValueError("The current name must not be empty")
    if (current_index < 0):
        raise ValueError(
            "The current index must be greater than or equal to 0")
    extension: str = path.splitext(current_name)[1].strip(".")
    if (extension == ""):
        raise ValueError("The file must have an extension")
    return f"{custom_prefix}_{current_index}.{extension}"


def rename_file(index_file, directory, custom_prefix):
    index, file = index_file
    new_name = generate_unique_name_from_count(custom_prefix, file, index)
    os.rename(file, path.join(directory, new_name))


def rename_files_in_directory(directory: str, custom_prefix: str) -> None:
    files = get_files_in_director(directory)
    print(f"Renaming {len(files)} files in the directory {directory}")
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(tqdm(executor.map(lambda index_file: rename_file(index_file,
             directory, custom_prefix), enumerate(files)), total=len(files)))


def ask_user_for_prefix() -> str:
    prefix: str = ""
    while True:
        prefix = input("Enter a custom prefix: ")
        if (prefix != ""):
            return prefix
        prefix = None
        print("The prefix must not be empty")


def ask_user_for_directory() -> str:
    directory: str = ""
    while True:
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        if directory:
            return directory
        print("No directory selected")


def get_raw_photo_metadata(file_path: str) -> dict | None:
    if (not path.exists(file_path)):
        raise FileNotFoundError(f"File {file_path} not found")
    metadata = {}
    if file_path.lower().endswith('.cr3'):
        with exiftool.ExifToolHelper(executable="C:/Program Files/exiftool/exiftool.exe") as et:
            data = et.get_metadata(file_path)
            for d in data:
                for k, v in d.items():
                    metadata[k] = v
            metadata["created_date"] = metadata["QuickTime:CreateDate"]
            return metadata
    return None


def get_mp4_metadata(file_path: str) -> dict | None:
    """
    Get metadata from a mp4 file
    Args:
        file_path (str): The filepath of the mp4 file

    Raises:
        FileNotFoundError: thrown if the file is not found
        ValueError: thrown if the parser is invalid

    Returns:
        dict: a dictionary of metadata
    """
    if (not path.exists(file_path)):
        raise FileNotFoundError(f"File {file_path} not found")
    metadata = {}
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == "Video" or track.track_type == "Audio":
            print(f"Track type: {track.track_type}")
            for key, value in track.to_data().items():
                metadata[key] = value
    metadata["created_date"] = metadata["encoded_date"]
    return metadata


def get_image_metadata(file_path: str) -> dict:
    """
    Get metadata from an image file (jpg, png, jpeg, etc)

    Args:
        file_path (str): The file path

    Raises:
        FileNotFoundError: thrown if the file does not exist

    Returns:
        dict: a dictionary of metadata
    """
    if (not path.exists(file_path)):
        raise FileNotFoundError(f"File {file_path} not found")
    metadata = {}
    with Image.open(file_path) as img:
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value
    metadata["created_date"] = metadata["DateTime"]
    return metadata


def get_file_metadata(file_path: str) -> dict:
    """
    Get metadata from a series of file types
    Args:
        file_path (str): The path of the file

    Raises:
        FileNotFoundError: Thrown if the file does not exist
        ValueError: Thrown if the file extension type is not supported

    Returns:
        dict: The metadata as a dictionary
    """
    if (not path.exists(file_path)):
        raise FileNotFoundError(f"File {file_path} not found")
    extension = path.splitext(file_path)[1].lower().strip(".")
    match extension:
        case "cr3":
            return get_raw_photo_metadata(file_path)
        case "mp4":
            return get_mp4_metadata(file_path)
        case "jpg":
            return get_image_metadata(file_path)
        case "jpeg":
            return get_image_metadata(file_path)
        case "png":
            return get_image_metadata(file_path)
        case _:
            raise ValueError(f"Unsupported file extension {extension}")


if __name__ == "__main__":
    directory = ask_user_for_directory()
    custom_prefix = ask_user_for_prefix()
    rename_files_in_directory(directory, custom_prefix)
