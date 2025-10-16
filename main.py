import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    print(response.text)
    usage = response.usage_metadata
    if(args.verbose == True):
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()
