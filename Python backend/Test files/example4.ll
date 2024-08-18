; Declare printf function
declare dso_local i32 @printf(i8*, ...)

; Define main function
define i16 @main() { ; |0100
  ; Call function to perform addition and get the result
  %result = call i16 @add_registers()

  ; Call putc function to print the result
  call i16 @putc(i16 %result)

  ; Return 0 to signify end of program
  ret i16 0
}

; Define add_registers function
define i16 @add_registers() {
  ; Initialize r1 and r2 to 1
  %r1 = add i16 0, 1
  %r2 = add i16 0, 1

  ; Add r1 and r2, store the result in r3
  %r3 = add i16 %r1, %r2

  ; Return r3
  ret i16 %r3
}

; Define putc function to print result
define i16 @putc(i16 %r3) {
    ; Call printf to print the integer value of r3
    call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r3)
  
    ; Return 0
    ret i16 0
}

; Define constant string format for printf
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
