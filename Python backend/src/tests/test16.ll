define i16 @main() {
entry:
    %x = icmp eq i16 5, 5
    br i1 %x, label %equal, label %notequal

equal:
    call i16 @putc(i16 49)  ; Print '1' (ASCII code 49)
    ret i16 0

notequal:
    call i16 @putc(i16 48)  ; Print '0' (ASCII code 48)
    ret i16 0
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %r) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r)
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1
