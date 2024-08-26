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
            value_int = hex(int(value))[2:]
            formatted_number = str(value_int).zfill(2)
        if(type == "i16"):
            value_int = hex(int(value))[2:]
            formatted_number = str(value_int).zfill(4)

        return "#" + formatted_number  # return formatted constant as hex
