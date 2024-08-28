define i16 @main() {
entry:
    ; Allocate memory for an i16 value
    %value = alloca i16
    
    ; Store the constant 42 into the allocated memory
    store i16 42, i16* %value
    
    ; Load the value from memory into a register
    %loaded_value = load i16, i16* %value
    
    ; Return the loaded value directly
    ret i16 %loaded_value
}
