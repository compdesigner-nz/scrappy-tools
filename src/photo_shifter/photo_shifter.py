import os
import concurrent
import tkinter as tk
import pathlib
import shutil
from typing import List

def copy_file(file_path: str, new_path: str) -> None:
    shutil.copyfile(file_path, new_path)