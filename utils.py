import os
import tempfile


def create_temp_directory():
    """
    Create a temporary directory for downloads.
    """
    return tempfile.mkdtemp()


def ensure_directory(path):
    """
    Create a directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)


def get_file_name(path):
    """
    Return only the file name from a full path.
    """
    return os.path.basename(path)
