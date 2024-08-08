# llvm_ir_to_ast.py
import llvmlite.binding as llvm
import json
import re

# Initialize LLVM
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class ASTNode:
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type
        self.attributes = kwargs

    def to_dict(self):
        node_dict = {
            'node_type': self.node_type,
            'attributes': {}
        }
        for k, v in self.attributes.items():
            if isinstance(v, ASTNode):
                node_dict['attributes'][k] = v.to_dict()
            elif isinstance(v, list):
                node_dict['attributes'][k] = [item.to_dict() if isinstance(item, ASTNode) else item for item in v]
            else:
                node_dict['attributes'][k] = v
        return node_dict

def extract_global_strings(ir_code):
    """
    Extract strings from global variables in the LLVM IR code.
    This method uses regex to find and extract constant strings from the IR text.
    """
    pattern = re.compile(r'@(?P<name>[\w.]+) = private unnamed_addr constant \[(?P<size>\d+) x i8\] c"(?P<value>.*?)"')
    matches = pattern.finditer(ir_code)

    global_strings = {}
    for match in matches:
        name = match.group('name')
        value = match.group('value')
        global_strings[name] = value
    return global_strings

def parse_llvm_ir(ir_code):
    module = llvm.parse_assembly(ir_code)
    module.verify()

    ast = ASTNode('Module', globals=[], functions=[])

    # Extract global strings
    global_strings = extract_global_strings(ir_code)
    for name, value in global_strings.items():
        ast.attributes['globals'].append(ASTNode('Global', name=name, value=value))

    # Capture functions and instructions
    for func in module.functions:
        func_node = ASTNode('Function', name=func.name, blocks=[])
        ast.attributes['functions'].append(func_node)

        for block in func.blocks:
            block_node = ASTNode('Block', name=block.name, instructions=[])
            func_node.attributes['blocks'].append(block_node)

            for inst in block.instructions:
                inst_node = ASTNode('Instruction', opcode=inst.opcode, operands=[str(op) for op in inst.operands])
                block_node.attributes['instructions'].append(inst_node)

    return ast

def llvm_ir_to_ast_json(ir_code, output_file):
    ast = parse_llvm_ir(ir_code)
    ast_dict = ast.to_dict()  # Convert AST to dictionary
    print(json.dumps(ast_dict, indent=4))  # Debug print to verify conversion
    with open(output_file, 'w') as f:
        json.dump(ast_dict, f, indent=4)

if __name__ == "__main__":
    llvm_ir_code = """
    @.str = private unnamed_addr constant [13 x i8] c"Hello World!\\00", align 1

    declare i32 @puts(i8* nocapture) nounwind

    define i32 @main() {
    entry:
        %0 = getelementptr [13 x i8], [13 x i8]* @.str, i32 0, i32 0
        call i32 @puts(i8* %0)
        ret i32 0
    }
    """
    output_file = 'ast.json'
    llvm_ir_to_ast_json(llvm_ir_code, output_file)
    print(f"AST has been saved to {output_file}")
