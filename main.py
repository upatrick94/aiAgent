import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file])
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for step in range(20):
        if args.verbose:
            print(f"\n--- Iteration {step + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
            ),
        )

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=args.verbose)

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                messages.append(function_call_result)

            continue

        if response.text:
            print("\nFinal response:")
            print(response.text)
            break

    else:
        print("Reached iteration limit (20) without final response.")

    usage = response.usage_metadata
    if args.verbose and usage:
        print(f"\nUser prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")



if __name__ == "__main__":
    main()
