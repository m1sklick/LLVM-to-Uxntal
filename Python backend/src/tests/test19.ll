define i16 @main() {
entry:
  %counter = alloca i16
  store i16 35, i16* %counter

  br label %loop_start

loop_start:
  %current_counter = load i16, i16* %counter

  %cmp = icmp eq i16 %current_counter, 0
  br i1 %cmp, label %loop_end, label %print_char

print_char:
  call i16 @putc(i16 %current_counter)

  %new_counter = sub i16 %current_counter, 1
  store i16 %new_counter, i16* %counter

  br label %loop_start

loop_end:
  ret i16 0
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %char) {
    ; Call printf to print the character
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %char)

    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1
