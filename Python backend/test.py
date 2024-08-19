from llvmlite import binding
import re

# Initialization
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

# Sample LLVM IR code for testing
with open('example4.ll', 'r') as file:
    llvm_ir = file.read()

# Parse the LLVM IR using llvmlite binding
module = binding.parse_assembly(llvm_ir)
module.verify()

# Utility function to get the operand value
def get_operand_value(operand):
    if hasattr(operand, 'name') and operand.name:
        return f"{operand.name}" # Return as memory reference
    if hasattr(operand, 'constant'):
        print("Operand constant: " + operand.constant)
        # return f"#{format(operand.constant, '04x')}"  # Format constant as hex
    else:
        # Splitting the operand into type and value, since we only have .type attribute in operand, 
        # but we don't have .constant or .value attribute to get value, we have to use split() method of stirng to get that value
        type, value = str(operand).split()
        if(type == "i1" or type == "i8"):
            value_int = int(value)
            formatted_number = str(value_int).zfill(2)
        if(type == "i16"):
            value_int = int(value)
            formatted_number = str(value_int).zfill(4)

        return "#" + formatted_number  # return formatted constant as hex
    
# List to track registers used in LLVM IR
registers = set()

# Function to translate a single LLVM instruction to Uxntal
def translate_instruction(instruction):
    op_map = {
        'add': 'ADD2',
        'sub': 'SUB2',
        'mul': 'MUL2',
        'div': 'DIV2',
    }

    uxntal_code = []

    # print(instruction.opcode)
    # print(instruction)

    
    # Handle 'ret' instruction
    if instruction.opcode == 'ret':
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            #Handle return in the main function
            if operand_value == '#00' or operand_value == "#0000":
                uxntal_code.append("BRK")
            #Handle returns in other functions
            else:
                uxntal_code.append(f".{operand_value} LDZ2")



    # Handle call instruction

    if instruction.opcode == 'call':
        if 'call i16 @putc' in str(instruction): # Translate the console output instruction
            output = []
            registers = re.findall(r'%([a-zA-Z]\w*)', str(instruction)) # Extract registers from console display function
            for reg in registers:
                output.append(f".{reg} LDZ2")
            output.append("#18 DEO")
            return output
        else:
            # print("hiadakjd: " + str(instruction))
            # print(instruction.name)
            for operand in instruction.operands:
                operand_value = get_operand_value(operand)
                uxntal_code.append(f";{operand_value} JSR2")
                uxntal_code.append(f".{instruction.name} STZ2")



    if instruction.opcode in op_map:
        uxntal_op = op_map[instruction.opcode]
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            # print(str(instruction) + " ---- " + operand_value + " ---- " + instruction.opcode) # for debugging!!!
            if hasattr(operand, 'name') and operand.name:
                uxntal_code.append(f".{operand_value} LDZ2")
            elif "ret" not in str(instruction): # Ignore ret statement, since we only need to replace that to BRK
                # if operand_value.startswith('#'):
                #     uxntal_code.append(operand_value)
                # else:
                uxntal_code.append(f"{operand_value}")
        uxntal_code.append(uxntal_op)

        # Store the result back to a register (memory location)
        if hasattr(instruction, 'name') and instruction.name:
            result_register = f".{instruction.name}"
            uxntal_code.append(f"{result_register} STZ2")

    # Handle store opcode separately, putting value into the register and storing it immediately
    if instruction.opcode == "store":
        # Regex pattern to capture the data type, value, and register name
        pattern = r"store\s+(\w+)\s+(\d+),\s+\w+\*\s+@(\w+)"
        # Find the matches
        match = re.search(pattern, str(instruction))

        # Push value into the stack
        if match:
            data_type, value, register_name = match.groups()
            if(data_type == "i1" or data_type == "i8"):
                value_int = int(value)
                formatted_number = str(value_int).zfill(2)
            if(data_type == "i16"):
                value_int = int(value)
                formatted_number = str(value_int).zfill(4)
            uxntal_code.append(f"#{formatted_number}")
            uxntal_code.append(f".{register_name} STZ2")

    # Handle load opcode separately, load register to the stack, then store it from the stack to another register
    if instruction.opcode == 'load':
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            if hasattr(operand, 'name') and operand.name:
                uxntal_code.append(f".{operand_value} LDZ2")
            uxntal_code.append(f".{instruction.name} STZ2")

    return uxntal_code

# # Function to translate control flow instructions
# def translate_control_flow(instruction):
#     if instruction.opcode == 'br':
#         # Handle unconditional branches
#         target = instruction.operands[0]
#         return [f"JMP ;{target}"]
#     elif instruction.opcode == 'cond_br':
#         # Handle conditional branches
#         condition, true_target, false_target = instruction.operands
#         cond_value = get_operand_value(condition)
#         return [f"{cond_value} JCN ;{true_target} ;{false_target}"]
#     return []

# # Function to translate memory instructions
# def translate_memory(instruction):
#     uxntal_code = []
#     if instruction.opcode == 'load':
#         # Load from memory address
#         address = get_operand_value(instruction.operands[0])
#         uxntal_code.append(f"{address} LDZ2")
#     elif instruction.opcode == 'store':
#         # Store to memory address
#         print(instruction.opcode)
#         value, address = instruction.operands
#         uxntal_code.append(f"{get_operand_value(value)} STZ2 {get_operand_value(address)}")
#     return uxntal_code

# This function just adds needed registers
def add_registers(module):
    defined_registers = ["|0000"]

    for function in module.functions:
        if function.name in ['printf', 'putc']:
            continue  # Ignore the functions @printf and @putc
        for block in function.blocks:
            for instruction in block.instructions:
                # Check if we even have registers(avoid immediate variables)
                if hasattr(instruction, 'name') and instruction.name:
                    register_name = instruction.name
                    uxntal_register = f"@{register_name} $2"
                    # TODO add the one for 1 byte registers
                    defined_registers.append(uxntal_register)
                elif instruction.opcode == 'store':
                    # Regex to capture the type and register name
                    pattern = r"store\s+(\w+)\s+\d+,\s+\w+\*\s+@(\w+)"
                    # Find the matches
                    match = re.search(pattern, str(instruction))
                    data_type, register_name = match.groups()
                    # print(f"Data Type: {data_type}")
                    # print(f"Register Name: {register_name}")
                    uxntal_register = f"@{register_name} $2"
                    defined_registers.append(uxntal_register)
                
                
    return defined_registers

# Main function to convert LLVM IR to Uxntal
def llvm_to_uxntal(module):
    register_declarations = add_registers(module)  # Memory declarations go here
    uxntal_code = ["|0100"] # Start of the program counter
    for function in module.functions:
        if function.name in ['printf', 'putc']:
            continue  # Ignore the functions @printf and @putc
        uxntal_code.append(f"@{function.name}") # define a function
        for block in function.blocks:
            for instruction in block.instructions:
                uxntal_instruction = translate_instruction(instruction)
                
                uxntal_code.extend(uxntal_instruction)
        if function.name != "main":
            uxntal_code.append("JMP2r") # jump back from our function if the function is not main

    uxntal_code = register_declarations + uxntal_code # adding declared registers to our uxntal_code

    return uxntal_code

# Translate the LLVM IR module to Uxntal
uxntal_code = llvm_to_uxntal(module)
print("The UXNtal_code.uxn file is generated")
with open('UXNtal_code.uxn', 'w') as file:
    for line in uxntal_code:
        file.write(line + '\n')
print("The generated UXNtal code:")
for line in uxntal_code:
    print(line)
