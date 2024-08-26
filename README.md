
## Authors

- [@m1sklick](https://github.com/m1sklick)


# LLVM IR to UXNtal compiler

This compiler creates UXNtal assembly language, which the Uxn virtual machine can run, from LLVM IR (Intermediate Representation). It interprets LLVM IR instructions and translates them into equivalent UXNtal code, including memory management, arithmetic operations, stack handling, and control flow (such as conditional branching).

Compilers also handle standard and system-specific function calls (such as 'putc' for output functions). It effectively manages tail recursion for recursive functions, but because UXNtal has a native call stack, non-tail recursion necessitates bespoke stack management. A '.tal' file that can be constructed and used on the Uxn VM is the end product.

A project presented in part fulfilment of the requirements of the
Degree of Master of Science at The University of Glasgow




## Run Locally

Clone the project

```bash
  git clone https://github.com/m1sklick/Project-Wim.git
```

Go to the project directory

```bash
  cd Project-Wim
```

Install dependencies
You should have a Python interpreter in your system. In order to check it run the following commands:
```bash
  pip --version
  python3 --version
```
The version used for development: 3.7.9

Install the 'llvmlite' library.

A lightweight wrapper for LLVM, 'llvmlite' offers a Python API for creating and modifying LLVM IR.

```bash
  pip install llvmlite
```

In order to use the compiler, firstly go to 'Project-Wim/Python Backend/src/' directory of the repository and then run the following command:

```bash
  python3 compiler.py file.ll
```
Here, you should replace file.ll with the actual file that contains LLVM IR code(see the tests folder)


## Running Tests

To run tests, run the following command

In your terminal go to 'Project-Wim/Python backend/src'
then run the following command

```bash
  python3 run_tests.py
```

The result should be:
```bash
LLVM IR output: *
UXNtal output: *
Test 0: Passed
LLVM IR output: *
UXNtal output: *
Test 1: Passed
LLVM IR output: *
UXNtal output: *
Test 2: Passed
LLVM IR output: *
UXNtal output: *
Test 3: Passed
LLVM IR output: *
UXNtal output: *
Test 4: Passed
LLVM IR output: *
UXNtal output: *
Test 5: Passed
LLVM IR output: *****
UXNtal output: *****
Test 6: Passed
```

