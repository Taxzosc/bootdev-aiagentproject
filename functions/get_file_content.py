import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            read_file = f.read(MAX_CHARS)
            if f.read(1):
                read_file += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return read_file

    except Exception as e:
        return f"Error: {e}"