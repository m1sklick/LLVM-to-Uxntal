from llvmlite import binding
import re

# Initialization
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

# Sample LLVM IR code for testing
with open('example0.ll', 'r') as file:
    llvm_ir = file.read()

# Parse the LLVM IR using llvmlite binding
module = binding.parse_assembly(llvm_ir)
module.verify()

# Utility function to get the operand value
def get_operand_value(operand):
    if hasattr(operand, 'name') and operand.name:
        print("Operand.name: " + operand.name)
        return f".{operand.name}"  # Return as memory reference
    elif hasattr(operand, 'constant'):
        print("Operand constant: " + operand.constant)
        return f"#{format(operand.constant, '04x')}"  # Format constant as hex
    else:
        # Splitting the operand into type and value, since we only have .type attribute in operand, 
        # but we don't have .constant or .value attribute to get value, we have to use spslit() method of stirng to get that value
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
        'ret': 'BRK'
    }

    uxntal_code = []

    # print(dir(instruction))

    if 'call i16 @putc' in str(instruction): # Translate the console output instruction
        output = []
        registers = re.findall(r'%([a-zA-Z]\w*)', str(instruction)) # Extract registers from console display function
        for reg in registers:
            output.append(f".{reg} LDZ2")
        output.append("#18 DEO")
        return output

    if instruction.opcode in op_map:
        uxntal_op = op_map[instruction.opcode]
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            if "ret" not in str(instruction): # Ignore ret statement, since we only need to replace that to BRK
                if operand_value.startswith('#'):
                    uxntal_code.append(operand_value)
                else:
                    uxntal_code.append(f"{operand_value}")
        uxntal_code.append(uxntal_op)

        # Store the result back to a register (memory location)
        if hasattr(instruction, 'name') and instruction.name:
            result_register = f".{instruction.name}"
            uxntal_code.append(f"{result_register} STZ2")
    return uxntal_code

# Function to translate control flow instructions
def translate_control_flow(instruction):
    if instruction.opcode == 'br':
        # Handle unconditional branches
        target = instruction.operands[0]
        return [f"JMP ;{target}"]
    elif instruction.opcode == 'cond_br':
        # Handle conditional branches
        condition, true_target, false_target = instruction.operands
        cond_value = get_operand_value(condition)
        return [f"{cond_value} JCN ;{true_target} ;{false_target}"]
    return []

# Function to translate memory instructions
def translate_memory(instruction):
    uxntal_code = []
    if instruction.opcode == 'load':
        # Load from memory address
        address = get_operand_value(instruction.operands[0])
        uxntal_code.append(f"{address} LDZ2")
    elif instruction.opcode == 'store':
        # Store to memory address
        print(instruction.opcode)
        value, address = instruction.operands
        uxntal_code.append(f"{get_operand_value(value)} STZ2 {get_operand_value(address)}")
    return uxntal_code

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
                    defined_registers.append(uxntal_register)
                
    return defined_registers

# Main function to convert LLVM IR to Uxntal
def llvm_to_uxntal(module):
    register_declarations = add_registers(module)  # Memory declarations go here
    uxntal_code = ["|0100"] # Start of the program counter
    for function in module.functions:
        if function.name in ['printf', 'putc']:
            continue  # Ignore the functions @printf and @putc
        for block in function.blocks:
            for instruction in block.instructions:
                uxntal_instruction = translate_instruction(instruction)
                uxntal_control_flow = translate_control_flow(instruction)
                uxntal_memory = translate_memory(instruction)
                
                uxntal_code.extend(uxntal_instruction)
                uxntal_code.extend(uxntal_control_flow)
                uxntal_code.extend(uxntal_memory)


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
