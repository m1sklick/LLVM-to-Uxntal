define i16 @main() {
entry:
    %x = add i16 20, 20
    br label %jump_to

skip:
    ret i16 0  ; Skip block ends here

jump_to:
    call i16 @putc(i16 %x)  ; Print the result of the addition (30)
    ret i16 0
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %x) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %x)
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1
