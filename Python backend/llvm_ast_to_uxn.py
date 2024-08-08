# llvm_ast_to_ux.py
import json

# Define a mapping from LLVM IR instructions to UXN assembly instructions
llvm_to_uxn_map = {
    'getelementptr': '',  # Specific handling required
    'call': '',           # Specific handling required
    'ret': 'BRK'          # Return from function
}

# Convert global variables to Uxntal strings
def convert_global_to_uxn(global_node):
    if global_node['node_type'] == 'Global':
        name = global_node['attributes']['name']
        value = global_node['attributes']['value'].strip('"')
        uxn_string = f'@{name[1:]}\n\t"{value}" 00'
        return uxn_string
    return ''

# Define a function to convert LLVM operands to UXN format if needed
def convert_operands_to_uxn(opcode, operands):
    if opcode == 'getelementptr':
        # Operand structure: [type, pointer, index1, index2]
        return ''  # Handled specifically in the context
    elif opcode == 'call':
        # Operand structure: [function, args]
        function_name = operands[0].split('@')[-1]  # Extract function name
        return function_name
    elif opcode == 'ret':
        return ''  # No operands needed for return
    else:
        return ' '.join(operands)  # Default case

def llvm_instruction_to_uxn(instruction):
    opcode = instruction['attributes']['opcode']
    operands = instruction['attributes']['operands']

    if opcode == 'call' and '@puts' in operands[0]:
        return 'print-text'
    
    uxn_instruction = llvm_to_uxn_map.get(opcode, 'NOP')  # Default to NOP if not found
    uxn_operands = convert_operands_to_uxn(opcode, operands)

    return f"{uxn_instruction} {uxn_operands}".strip()

def traverse_ast(node, assembly_code):
    node_type = node['node_type']

    if node_type == 'Module':
        assembly_code.append('|10 @Console &vector $2 &write $1\n|100\n')
        for global_var in node['attributes']['globals']:
            global_code = convert_global_to_uxn(global_var)
            assembly_code.append(global_code)
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
