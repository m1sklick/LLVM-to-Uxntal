from operands import get_operand_value

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
                    type = str(instruction.type)
                    if type == "i16" or type == "i16*":
                        uxntal_register = f"@{register_name} $2"
                    elif type == "i1" or type == "i8" or type == "i1*" or type == "i8*":
                        uxntal_register = f"@{register_name} $1"
                    else: 
                        print("Something wrong with adding registers, may be the register type is not supported!")
                        uxntal_register = "Error!!!"
                    if uxntal_register not in defined_registers:
                        defined_registers.append(uxntal_register)
                elif instruction.opcode == 'store':
                    # Handle 'store' opcode
                    for operand in instruction.operands:
                        operand_value = get_operand_value(operand)
                        if not operand_value.startswith('#'): # operand should not be an immediate value, it should be a name of the register
                            register_name = operand_value
                            uxntal_register = f"@{register_name} $2"
                            if uxntal_register not in defined_registers:
                                defined_registers.append(uxntal_register)

    return defined_registers