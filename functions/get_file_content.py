import os
from functions.config import MAX_FILE_LENGTH
import google.genai.types as types

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        normalized = "\n".join(line.lstrip() for line in content.splitlines())

        if len(normalized) > MAX_FILE_LENGTH:
            normalized = normalized[:MAX_FILE_LENGTH] + f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]'

        return normalized

    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory."
            )
        },
    ),
)
