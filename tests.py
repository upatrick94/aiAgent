from functions.run_python_file import run_python_file

def run_tests():
    print('run_python_file("calculator", "main.py"):')
    result = run_python_file("calculator", "main.py")
    print(result, "\n")

    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result, "\n")

    print('run_python_file("calculator", "tests.py"):')
    result = run_python_file("calculator", "tests.py")
    print(result, "\n")

    print('run_python_file("calculator", "../main.py"):')
    result = run_python_file("calculator", "../main.py")
    print(result, "\n")

    print('run_python_file("calculator", "nonexistent.py"):')
    result = run_python_file("calculator", "nonexistent.py")
    print(result, "\n")

    print('run_python_file("calculator", "lorem.txt"):')
    result = run_python_file("calculator", "lorem.txt")
    print(result, "\n")

if __name__ == "__main__":
    run_tests()
