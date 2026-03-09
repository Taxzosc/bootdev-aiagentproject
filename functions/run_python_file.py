import os
import subprocess
from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]

        if args != None:
            command.extend(args)
        
        process_result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_string = ""
        if process_result.returncode != 0:
            output_string += f"Process exited with code {process_result.returncode}\n"
        if not process_result.stderr and not process_result.stdout:
            output_string += f"No output produced\n"
        if process_result.stdout:
            output_string += f"STDOUT: {process_result.stdout}"
        if process_result.stderr:
            output_string += f"\nSTDERR: {process_result.stderr}"
            
        return output_string
        

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file with the given args if they are given(args defaults to None), within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file which will be run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Arguements given to the function",
            ),
        },
        required=["file_path"],
    ),
)

    # if process_result.stderr == None or process_result.stdout == None:
    # i had this in my code and it still passed. 
    # learned that if a function has an agruement that is default to  =none, func(args=None)
    # one should not write if args = None, but instead if args. == None still works but the other way simply
    # skips the line if the args is given a falsiness