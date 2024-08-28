define i16 @main() {
entry:
    %x = add i16 15, 16
    %condition = icmp eq i16 %x, 30
    br i1 %condition, label %is_equal, label %not_equal

is_equal:
    call i16 @putc(i16 49)  ; Print '1' if condition is true (30 == 30)
    ret i16 0

not_equal:
    call i16 @putc(i16 48)  ; Print '0' if condition is false (Should not happen)
    ret i16 0
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %r) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r)
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1
