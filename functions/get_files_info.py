import os
import google.genai.types as types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(full_path)

        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'
        
        entries = []
        for entry in os.listdir(abs_target_dir):
            entry_path = os.path.join(abs_target_dir, entry)
            try:
                is_dir = os.path.isdir(entry_path)
                file_size = os.path.getsize(entry_path)
                entries.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            except Exception as e:
                entries.append(f"- {entry}: Error reading file info ({e})")

        return "\n".join(entries) if entries else "(empty directory)"
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
        
