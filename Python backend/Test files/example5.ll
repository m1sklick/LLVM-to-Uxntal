define i16 @main() {
entry:
  %x = alloca i16
  store i16 15, i16* %x

  %x_val = load i16, i16* %x

  %cmp = icmp sgt i16 %x_val, 10

  br i1 %cmp, label %if.then, label %if.else

if.then:
  call i16 @putc(i16 89)                    ; ASCII code for 'Y'
  br label %end

if.else:
  call i16 @putc(i16 78)                    ; ASCII code for 'N'
  br label %end

end:
  ret i16 0
}

; The hardest part is the printing. You can ignore everything below this line.

declare dso_local i16 @printf(i8*, ...)

define i16 @putc(i16 %r1) {
    call i16 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i16 %r1)
    ret i16 0
}

@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1
