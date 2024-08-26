import sys
import os
import execute

def main():
    # Check if a filename argument was provided
    if len(sys.argv) != 2:
        print("Usage: compiler.py file.ll")
        sys.exit(1)
    
    # Get the filename from the command-line argument
    filename = sys.argv[1]
    
    # Read the content of the file
    try:
        with open(filename, 'r') as file:
            llvm_ir = file.read()
            # Do something with the llvm_ir (e.g., print it)
            
            uxntal_code = execute.run_compiler(llvm_ir)

            real_name, extension = os.path.splitext(filename)

            with open(f"{real_name}.tal", 'w') as file:
                for line in uxntal_code:
                    file.write(line + '\n')
            
            print(f"The generated UXNtal code is written to {real_name}.tal")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
