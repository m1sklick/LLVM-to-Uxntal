; LLVM version of 
; |0000
; @x $2
; |0100
; #0006 .x STZ2 
; .x LDZ2 #0007 MUL2
; #18 DEO 
; BRK

; We first translate this into a register-based version:

; |0000
; @x $2
; |0100
; #0006 .x STZ2 
; .x LDZ2 .r1 STZ2
; .r1 LDZ2 #0007 MUL2 .r2 STZ2
; .r2 LDZ2 #18 DEO
; BRK

@x = global i16 u0x0000 ; @x $2

define i8 @main() { ; |0100
    store i16 u0x0006, i16* @x ; #0006 .x STZ2 
    %r1 = load i16, i16* @x ; .x LDZ2 .r1 STZ2
    %r2 = mul i16 u0x0007,%r1 ; .r1 LDZ2 #0007 MUL2 .r2 STZ2
    call i16 @putc(i16 %r2) ; .r2 LDZ2 #18 DEO
    ret i8 0 ; BRK
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %r1) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r1)
  
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1