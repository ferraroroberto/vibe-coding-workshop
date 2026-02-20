import os

def setup_environment():
    """
    Sets up the environment for the 'Hello World' exercise.
    Since this is a pure Python exercise with no external data,
    we just verify the folder exists and maybe create a blank starter file.
    """
    
    # Create a blank 'hello.py' file if it doesn't exist
    # This helps the student get started immediately.
    file_name = 'hello.py'
    
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write("# Write your code here\n")
            f.write("# 1. Print 'Hello World'\n")
            f.write("# 2. Calculate Profit (Revenue - Cost)\n")
            f.write("# 3. Loop 1 to 5\n")
        print(f"Created '{file_name}' to help you get started.")
    else:
        print(f"'{file_name}' already exists. You are ready to go!")

    print("Environment setup complete. Open 'hello.py' and start coding!")

if __name__ == "__main__":
    setup_environment()
