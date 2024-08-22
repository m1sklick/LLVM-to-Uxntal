define i16 @main() {
entry:
  %x = alloca i16
  store i16 15, i16* %x

  %x_val = load i16, i16* %x

  %cmp = icmp sgt i16 %x_val, 10

  br i1 %cmp, label %ifthen, label %ifelse

ifthen:
  %r1 = mul i16 u0x0007, u0x0006
  call i16 @putc(i16 %r1)
  br label %end

ifelse:
  %r2 = mul i16 u0x0007, u0x0005
  call i16 @putc(i16 %r2)
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


; The compiler's output:
; |0000
; @x $2
; @x_val $2
; @cmp $2
; @r1 $2
; @r2 $2
; |0100
; @main
; @entry
; #0015
; .x STZ2
; .x LDZ2
; .x_val STZ2
; .x_val LDZ2
; #0010
; GTH2
; .cmp STZ2
; .cmp LDZ2
; ,ifthen JCN
; ;ifelse JSR2
; @ifthen
; #0007
; #0006
; MUL2
; .r1 STZ2
; .r1 LDZ2
; #18 DEO
; ;end JSR2
; @ifelse
; #0007
; #0005
; MUL2
; .r2 STZ2
; .r2 LDZ2
; #18 DEO
; ;end JSR2
; @end
; BRK
