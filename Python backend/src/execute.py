from llvmlite import binding
import re

from registers import add_registers
from instructions import translate_instruction


def run_compiler(llvm_ir):
    # Initialization
    binding.initialize()
    binding.initialize_native_target()
    binding.initialize_native_asmprinter()

    # Parse the LLVM IR using llvmlite binding
    module = binding.parse_assembly(llvm_ir)
    module.verify()

    # Main function to convert LLVM IR to Uxntal
    def llvm_to_uxntal(module):
        register_declarations = add_registers(module)  # Memory declarations go here
        uxntal_code = ["|0100"] # Start of the program counter
        for function in module.functions:
            if function.name in ['printf', 'putc']:
                continue  # Ignore the functions @printf and @putc
            uxntal_code.append(f"@{function.name}") # define a function
            for block in function.blocks:
                if str(block.name) != "":
                    uxntal_code.append(f"&{block.name}")
                for instruction in block.instructions:
                    uxntal_instruction = translate_instruction(instruction, module)
                    
                    uxntal_code.extend(uxntal_instruction)
            if function.name != "main":
                uxntal_code.append("JMP2r") # jump back from our function if the function is not main

        uxntal_code = register_declarations + uxntal_code # adding declared registers to our uxntal_code

        return uxntal_code

    # Translate the LLVM IR module to Uxntal
    uxntal_code = llvm_to_uxntal(module)
    return uxntal_code