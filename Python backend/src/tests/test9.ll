define i16 @main() {
    %num = alloca i16
    store i16 42, i16* %num
    %r2 = load i16, i16* %num
    call i16 @putc(i16 %r2)
    ret i16 0
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %r2) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r2)
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1
