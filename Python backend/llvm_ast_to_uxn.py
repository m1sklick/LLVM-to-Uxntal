import json

# Define a mapping from LLVM IR instructions to UXN assembly instructions
llvm_to_uxn_map = {
    'alloca': '',  # Stack allocation is implicit in UXN
    'store': 'STA',  # Store value to address
    'ret': 'BRK',  # Return from function
    'getelementptr': '',  # Handled separately
    'call': '',  # Calls will depend on function called, handled specially
}

# Convert string to UXN format
def string_to_uxn_string(string):
    # Convert string to hexadecimal representation for UXN
    return '"' + ' '.join(f'{ord(c):02x}' for c in string) + '"'

# Generate UXN assembly for global strings
def generate_uxn_globals(globals_list):
    uxn_globals = []
    for global_item in globals_list:
        if global_item['node_type'] == 'Global':
            name = global_item['attributes']['name']
            value = global_item['attributes']['value'].replace('\\00', '\0')
            uxn_string = string_to_uxn_string(value)
            uxn_globals.append(f"@{name}\n    {uxn_string}")
    return uxn_globals

# Define a function to convert LLVM operands to UXN format if needed
def convert_operands_to_uxn(opcode, operands):
    if opcode == 'store':
        # Assuming operands are [value, destination]
        value = operands[0]
        destination = operands[1]
        return f"{value} ;{destination}"  # STA requires value, address format
    elif opcode == 'getelementptr':
        # Handle by providing the address for the string
        return f";{operands[0].split()[0].replace('@', '')}"  # Load base address
    elif opcode == 'call':
        # Call operations translate to UXN subroutine invocations
        func_name = operands[0].strip().split()[1]
        if "puts" in func_name:
            return "print-text"  # Call the print-text routine
        return ''  # Default handling
    elif opcode == 'ret':
        return ''  # No operands needed for return
    else:
        return ' '.join(operands)  # Default case

def llvm_instruction_to_uxn(instruction):
    opcode = instruction['attributes']['opcode']
    operands = instruction['attributes']['operands']

    if opcode == 'getelementptr':
        # Handle GEP directly as it's about loading an address
        return f"LDA {convert_operands_to_uxn(opcode, operands)} JSR print-text"
    elif opcode == 'call':
        # Directly handle function calls
        uxn_function = convert_operands_to_uxn(opcode, operands)
        if uxn_function:
            return f"JSR {uxn_function}"
        else:
            return ''
    
    uxn_instruction = llvm_to_uxn_map.get(opcode, 'NOP')  # Default to NOP if not found
    uxn_operands = convert_operands_to_uxn(opcode, operands)

    return f"{uxn_instruction} {uxn_operands}".strip()

def traverse_ast(node, assembly_code):
    node_type = node['node_type']

    if node_type == 'Module':
        for global_item in node['attributes']['globals']:
            assembly_code.extend(generate_uxn_globals([global_item]))
        for function in node['attributes']['functions']:
            traverse_ast(function, assembly_code)
    elif node_type == 'Function':
        assembly_code.append(f"@{node['attributes']['name']} ( -> )")
        for block in node['attributes']['blocks']:
            traverse_ast(block, assembly_code)
    elif node_type == 'Block':
        assembly_code.append(f"; Block: {node['attributes']['name']}")
        for instruction in node['attributes']['instructions']:
            uxn_instruction = llvm_instruction_to_uxn(instruction)
            if uxn_instruction:
                assembly_code.append(uxn_instruction)

def ast_to_uxn_assembly(ast):
    assembly_code = ["|10 @Console &vector $2 &write $1", "|100"]
    traverse_ast(ast, assembly_code)
    # Add a print-text subroutine to handle the 'puts' call
    assembly_code.append("""
@print-text ( str* -- )
    &while
        LDAk .Console/write DEO
        INC2 LDAk ?&while
    POP2
    JMP2r
    """.strip())
    return assembly_code

def read_ast_json(file_path):
    with open(file_path, 'r') as f:
        ast = json.load(f)
    return ast

def write_uxn_assembly(file_path, assembly_code):
    with open(file_path, 'w') as f:
        for line in assembly_code:
            f.write(line + '\n')

if __name__ == "__main__":
    input_file_path = 'ast.json'
    output_file_path = 'output.uxn'

    ast = read_ast_json(input_file_path)
    assembly_code = ast_to_uxn_assembly(ast)
    write_uxn_assembly(output_file_path, assembly_code)

    print(f"UXN assembly code has been saved to {output_file_path}")
