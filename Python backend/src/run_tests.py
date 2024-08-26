import subprocess
import time

# Define the file names
llvm_files = [f"tests/example{i}.ll" for i in range(7)]
uxntal_files = [f"tests/example{i}.tal" for i in range(7)]
rom_files = [f"tests/example{i}.rom" for i in range(7)]

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
for i in range(7):
    # Run "lli" command to get the expected output from LLVM IR
    llvm_output = run_command(f"lli {llvm_files[i]}")
    print("LLVM IR output: " + llvm_output)

    # Run "uxnasm" to compile UXNtal code to a ROM file
    run_command(f"./uxnasm {uxntal_files[i]} {rom_files[i]}")

    # Run "uxncli" and interact with it
    process = subprocess.Popen(f"./uxncli {rom_files[i]}", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Allow it to run for a few seconds (or however long you need to capture the output)
    time.sleep(2)  # Run for 2 seconds

    # Send 'q' to quit the process
    process.stdin.write('q\n')
    process.stdin.flush()

    # Capture output from the running uxncli process
    uxntal_output, _ = process.communicate()
    print("UXNtal output: " + uxntal_output)

    # Compare outputs
    if llvm_output == uxntal_output.strip():
        print(f"Test {i}: Passed")
    else:
        print(f"Test {i}: Failed")
