*  xas99.py -R bin2hex.asm -L bin2hex.lst

  AORG >8300
PAD0    EQU >835C

; PAD0 contains the byte to be shown.
; Special character set used where 0..9 is followed by A..F directly.
HEXBASECH EQU >E0         ; Base character for hex display
  DATA $+2
  MOVB @PAD0,R1
  SRL  R1,4
  AI   R1,256*HEXBASECH
  MOVB  R1,@>FFFE(R15)  write byte to VDP
  MOVB @PAD0,R1
  ANDI R1,>0F00
  AI   R1,256*HEXBASECH
  MOVB  R1,@>FFFE(R15)  write byte to VDP
  RT

;  MOV R11,R2
;  MOVB @PAD0,R1
;  SRL  R1,4
;  BL   @!
;  MOVB @PAD0,R1
;  ANDI R1,>0F00
;  MOV R2,R11
;!:
;  AI   R1,'0'*256
;  CI   R1,('9'+1)*>100
;  JL   !
;  AI   R1,>700
;!
;  MOVB  R1,@>FFFE(R15)  write byte to VDP
;  RT
