import json

# Define a mapping from LLVM IR instructions to UXN assembly instructions
llvm_to_uxn_map = {
    'alloca': 'PSH 0',  # Allocate space on the stack (placeholder value)
    'store': 'STA',     # Store value to address
    'ret': 'BRK'        # Return from function
}

# Define a function to convert LLVM operands to UXN format if needed
def convert_operands_to_uxn(opcode, operands):
    if opcode == 'alloca':
        return ''  # No additional operands for stack allocation
    elif opcode == 'store':
        # Assume operands are [value, destination]
        value = operands[0].split()[1]  # Extract the actual value without type
        destination = operands[1].split()[0]  # Extract destination without additional details
        return f"{value}, {destination}"  # Format for STA
    elif opcode == 'ret':
        return ''  # No operands needed for return
    else:
        return ' '.join(operands)  # Default case

def llvm_instruction_to_uxn(instruction):
    opcode = instruction['attributes']['opcode']
    operands = instruction['attributes']['operands']

    uxn_instruction = llvm_to_uxn_map.get(opcode, 'NOP')  # Default to NOP if not found
    uxn_operands = convert_operands_to_uxn(opcode, operands)

    return f"{uxn_instruction} {uxn_operands}".strip()

def traverse_ast(node, assembly_code):
    node_type = node['node_type']

    if node_type == 'Module':
        for function in node['attributes']['functions']:
            traverse_ast(function, assembly_code)
    elif node_type == 'Function':
        assembly_code.append(f"; Function: {node['attributes']['name']}")
        for block in node['attributes']['blocks']:
            traverse_ast(block, assembly_code)
    elif node_type == 'Block':
        assembly_code.append(f"; Block: {node['attributes']['name']}")
        for instruction in node['attributes']['instructions']:
            uxn_instruction = llvm_instruction_to_uxn(instruction)
            assembly_code.append(uxn_instruction)

def ast_to_uxn_assembly(ast):
    assembly_code = []
    traverse_ast(ast, assembly_code)
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
