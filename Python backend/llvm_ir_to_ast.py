import llvmlite.binding as llvm
import json

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

def parse_llvm_ir(ir_code):
    module = llvm.parse_assembly(ir_code)
    module.verify()

    ast = ASTNode('Module', functions=[])

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
    define i32 @main() {
    entry:
      %0 = alloca i32, align 4
      store i32 0, i32* %0, align 4
      ret i32 0
    }
    """
    output_file = 'ast.json'
    llvm_ir_to_ast_json(llvm_ir_code, output_file)
    print(f"AST has been saved to {output_file}")
