; LLVM code:

define i16 @main() {
  %result = call i16 @add_registers()

  call i16 @putc(i16 %result)

  ret i16 0
}

define i16 @add_registers() {
  %r1 = add i16 0, 20
  %r2 = add i16 0, 22

  %r3 = add i16 %r1, %r2

  ret i16 %r3
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i32 @printf(i8*, ...)

define i16 @putc(i16 %r3) {
    call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r3)
  
    ; Return 0
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1


; The compiler's output:
; |0000
; @result $2
; @r1 $2
; @r2 $2
; @r3 $2
; |0100
; @main
; ;add_registers JSR2
; .result STZ2
; .result LDZ2
; #18 DEO
; BRK
; @add_registers
; #0000
; #0020
; ADD2
; .r1 STZ2
; #0000
; #0022
; ADD2
; .r2 STZ2
; .r1 LDZ2
; .r2 LDZ2
; ADD2
; .r3 STZ2
; .r3 LDZ2
; JMP2r
