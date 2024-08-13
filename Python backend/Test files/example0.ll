; LLVM version of 
; |0100 
; #0006 #0007 MUL2 #18 DEO 
; BRK

define i16 @main() { ; |0100

  %r1 = mul i16 u0x0007, u0x0006
  call i16 @putc(i16 %r1); #18 DEO
  ret i16 0 ; BRK
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %r1) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r1)
  
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1