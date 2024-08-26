; LLVM code:

define i16 @main() {
entry:
  %counter = alloca i16
  store i16 0, i16* %counter

  %char = alloca i16
  store i16 42, i16* %char  ; ASCII code for '*'

  br label %loop_start

loop_start:
  %current_counter = load i16, i16* %counter

  %cmp = icmp eq i16 %current_counter, 5
  br i1 %cmp, label %loop_end, label %print_char

print_char:
  %char_to_print = load i16, i16* %char

  call i16 @putc(i16 %char_to_print)

  %new_counter = add i16 %current_counter, 1
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

; The compiler's output:
; |0000
; @counter $2
; @char $2
; @current_counter $2
; @cmp $1
; @char_to_print $2
; @new_counter $2
; |0100
; @main
; &entry
; #0000
; .counter STZ2
; #002a
; .char STZ2
; ;&loop_start JMP2
; &loop_start
; .counter LDZ2
; .current_counter STZ2
; .current_counter LDZ2
; #0005
; EQU2
; .cmp STZ
; .cmp LDZ
; ;&loop_end JCN2
; ;&print_char JMP2
; &print_char
; .char LDZ2
; .char_to_print STZ2
; .char_to_print LDZ2
; #18 DEO
; .current_counter LDZ2
; #0001
; ADD2
; .new_counter STZ2
; .new_counter LDZ2
; .counter STZ2
; ;&loop_start JMP2
; &loop_end
; BRK

