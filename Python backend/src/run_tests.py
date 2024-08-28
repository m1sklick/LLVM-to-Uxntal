import subprocess
import time

# Define the file names
llvm_files = [f"tests/test{i}.ll" for i in range(1, 22)]
uxntal_files = [f"tests/test{i}.tal" for i in range(1, 22)]
rom_files = [f"tests/test{i}.rom" for i in range(1, 22)]

passed_counter = 0
failed_counter = 0

# Function to run a CLI command and return its output
def run_command(command, timeout=None):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}")
        return None

# Loop through each test file
for i in range(1, 22):
    print(f"Test {i}:")
    # Run "lli" command to get the expected output from LLVM IR
    llvm_output = run_command(f"lli {llvm_files[i-1]}")
    print("LLVM IR output: " + llvm_output)

    # Run Compiler
    run_command(f"python3 compiler.py {llvm_files[i-1]}")

    # Run "uxnasm" to compile UXNtal code to a ROM file
    run_command(f"./uxnasm {uxntal_files[i-1]} {rom_files[i-1]}")

    # Run "uxncli" and interact with it
    process = subprocess.Popen(f"./uxncli {rom_files[i-1]}", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Send 'q' to quit the process and capture output from the running uxncli process
    uxntal_output, _ = process.communicate('q\n')
    print("UXNtal output: " + uxntal_output)

    # Compare outputs
    if llvm_output == uxntal_output.strip():
        passed_counter+=1
        print(f"Passed")
    else:
        failed_counter+=1
        print(f"Failed")

print(f"In total Passed: {passed_counter} and Failed: {failed_counter}")
print(f"Percentage of tests passed: {passed_counter/21*100}%")
