*  xas99.py -R bin2hex.asm -L bin2hex.lst

  AORG >8302
PAD0    EQU >835C

  MOV R11,R2
  MOVB @PAD0,R1
  SRL  R1,4
  BL   @!
  MOVB @PAD0,R1
  ANDI R1,>0F00
  MOV R2,R11
!:
  AI   R1,'0'*256
  CI   R1,('9'+1)*>100
  JL   !
  AI   R1,>700
!
  MOVB  R1,@>FFFE(R15)  write byte to VDP
  RT
