from operands import get_operand_value
from registers import add_registers
import re

# Function to translate a single LLVM instruction to Uxntal
def translate_instruction(instruction, module):
    op_map = {
        'add': 'ADD2',
        'sub': 'SUB2',
        'mul': 'MUL2',
        'div': 'DIV2',
    }

    # Getting a map of register names and their datasize
    registers = add_registers(module)
    del registers[0]
    map_registers = {}
    for item in registers:
        key, value = item.split()  # Split each item by space
        key = key.lstrip('@')      # Remove the '@' symbol
        value = value.lstrip('$')  # Remove the '$' symbol
        map_registers[key] = value

    uxntal_code = []
    # print(str(instruction) + " --- " + str(instruction.opcode))

    # Handle 'ret' instruction
    if instruction.opcode == 'ret':
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            #Handle return in the main function
            if operand_value == '#00' or operand_value == "#0000":
                uxntal_code.append("BRK")
            #Handle returns in other functions
            else:
                data_size = map_registers.get(operand_value)
                if data_size == "2":
                    uxntal_code.append(f".{operand_value} LDZ2")
                if data_size == "1":
                    uxntal_code.append(f".{operand_value} LDZ")

    # Handle call instruction
    if instruction.opcode == 'call':
        if 'call i16 @putc' in str(instruction): # Translate the console output instruction
            output = []
            operand_value = None
            for operand in instruction.operands:
                operand_value = get_operand_value(operand)
                if operand_value.startswith("#"):
                    output.append(operand_value)
                else:
                    if operand_value != "putc": # ignore putc operand
                        data_size = map_registers.get(operand_value)
                        if data_size == "2":
                            output.append(f".{operand_value} LDZ2")
                        if data_size == "1":
                            output.append(f".{operand_value} LDZ")
            output.append("#18 DEO")
            return output
        else: # Translate call fo the function
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
                data_size = map_registers.get(operand_value)
                if data_size == "2":
                    uxntal_code.append(f".{operand_value} LDZ2")
                if data_size == "1":
                    uxntal_code.append(f".{operand_value} LDZ")
            elif "ret" not in str(instruction): # Ignore ret statement, since we only need to replace that to BRK
                # if operand_value.startswith('#'):
                #     uxntal_code.append(operand_value)
                # else:
                uxntal_code.append(f"{operand_value}")
        uxntal_code.append(uxntal_op)

        # Store the result back to a register (memory location)
        if hasattr(instruction, 'name') and instruction.name:
            result_register = f"{instruction.name}"
            data_size = map_registers.get(instruction.name)
            if data_size == "2":
                uxntal_code.append(f".{result_register} STZ2")
            if data_size == "1":
                uxntal_code.append(f".{result_register} STZ")

        

    # Handle store opcode separately, putting value into the register and storing it immediately
    if instruction.opcode == "store":
        data_type, value, register_name = None, None, None

        for operand in instruction.operands: # load the used values
            operand_value = get_operand_value(operand)

            if operand_value.startswith('#'):
                value = str(operand_value)
                data_type = str(operand.type)
            elif not operand_value.startswith('#'):
                register_name = str(operand_value)

        if data_type == None and value == None and register_name != None:
            data_type = str(operand.type)
            for operand in instruction.operands: # load the used values
                if str(get_operand_value(operand)) != register_name:
                    operand_value = get_operand_value(operand)
            data_size = map_registers.get(operand_value)
            if data_size == "2":
                value = (f".{operand_value} LDZ2")
            if data_size == "1":
                value = (f".{operand_value} LDZ")
            

        if data_type != None and value != None and register_name != None:
            if data_type == "i1" or data_type == "i8" or data_type == "i1*" or data_type == "i8*":
                uxntal_code.append(value)
                data_size = map_registers.get(register_name)
                if data_size == "2":
                    uxntal_code.append(f".{register_name} STZ2")
                if data_size == "1":
                    uxntal_code.append(f".{register_name} STZ")
            if data_type == "i16" or data_type == "i16*":
                uxntal_code.append(value)
                data_size = map_registers.get(register_name)
                if data_size == "2":
                    uxntal_code.append(f".{register_name} STZ2")
                if data_size == "1":
                    uxntal_code.append(f".{register_name} STZ")
            
    if instruction.opcode == 'load':     # Handle load opcode separately, load register to the stack, then store it from the stack to another register
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            if hasattr(operand, 'name') and operand.name:
                data_size = map_registers.get(operand_value)
                if data_size == "2":
                    uxntal_code.append(f".{operand_value} LDZ2")
                if data_size == "1":
                    uxntal_code.append(f".{operand_value} LDZ")
            data_size = map_registers.get(instruction.name)
            if data_size == "2":
                uxntal_code.append(f".{instruction.name} STZ2")
            if data_size == "1":
                uxntal_code.append(f".{instruction.name} STZ")

    if instruction.opcode == 'icmp':    # Handle conditions
        for operand in instruction.operands:
            operand_value = get_operand_value(operand)
            if hasattr(operand, 'name') and operand.name:
                data_size = map_registers.get(operand_value)
                if data_size == "2":
                    uxntal_code.append(f".{operand_value} LDZ2")
                if data_size == "1":
                    uxntal_code.append(f".{operand_value} LDZ")
            else:
                uxntal_code.append(operand_value)

        pattern = r"icmp\s+(\w+)"   # Define the regular expression pattern to find the word after "icmp" which will show us what type of comparison is this
        match = re.search(pattern, str(instruction))
        if match:   # Check if a match was found
            comp_type = match.group(1)
            if comp_type == "sgt":
                uxntal_code.append("GTH2")
            elif comp_type == "slt":
                uxntal_code.append("LTH")
            elif comp_type == "eq":
                uxntal_code.append("EQU2")
            elif comp_type == "ne":
                uxntal_code.append("NEQ2")
        else:
            print("Something is wrong with translation of icmp opcode")

        # store the result of comparison in the register
        data_size = map_registers.get(instruction.name)
        if data_size == "2":
            uxntal_code.append(f".{instruction.name} STZ2")
        if data_size == "1":
            uxntal_code.append(f".{instruction.name} STZ")

    if instruction.opcode == 'br':  # Handle br opcode
        operand_list = []
        for operand in instruction.operands:
            operand_list.append(operand.name)        
        if len(operand_list) == 1:
            uxntal_code.append(f";&{operand_list[0]} JMP2")
        elif len(operand_list) == 3:
            for operand in instruction.operands:
                if hasattr(operand, 'name') and operand.name:
                    if str(operand.type) != 'label':
                        operand_value = get_operand_value(operand)
                        data_size = map_registers.get(operand_value)
                        if data_size == "2":
                            uxntal_code.append(f".{operand_value} LDZ2")
                        if data_size == "1":
                            uxntal_code.append(f".{operand_value} LDZ")
            uxntal_code.append(f";&{operand_list[2]} JCN2")
            uxntal_code.append(f";&{operand_list[1]} JMP2")
                        
    return uxntal_code