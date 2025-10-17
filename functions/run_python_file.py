import os
import subprocess
import google.genai.types as types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(full_path)

        if not abs_target_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_target_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        completed = subprocess.run(["python", abs_target_path] + args, capture_output=True, text=True, cwd=abs_working_dir, timeout=30)

        output_parts = []
        stdout_text = completed.stdout.strip()
        stderr_text = completed.stderr.strip()

        if stdout_text:
            output_parts.append(f"STDOUT:\n{stdout_text}")
        if stderr_text:
            output_parts.append(f"STDERR:\n{stderr_text}")
        if completed.returncode != 0:
            output_parts.append(f"Process exited with code {completed.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)
    
    except subprocess.TimeoutExpired:
        return "Error: Python file execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file.",
            ),
        },
    ),
)
