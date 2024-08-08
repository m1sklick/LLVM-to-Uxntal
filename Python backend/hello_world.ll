@.str = private unnamed_addr constant [13 x i8] c"Hello World!\00", align 1

declare i32 @puts(i8* nocapture) nounwind

define i32 @main() {
entry:
    %0 = getelementptr [13 x i8], [13 x i8]* @.str, i32 0, i32 0
    call i32 @puts(i8* %0)
    ret i32 0
}
