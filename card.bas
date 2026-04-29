REM === JDS - 25 YEARS AT AMPLIFY ===
REM   2001 - 2026.  No fanfare.

BORDER 0
PAPER 0
INK 7
CLS

REM ---- Splash the SCREEN$ data into screen memory ----
ASM
    di
    ld hl, scr_data
    ld de, 16384
    ld bc, 6912
    ldir
    ei
    jp scr_after
scr_data:
    INCBIN "card.scr"
scr_after:
END ASM

REM ---- Hold the splash on its own for ~4 seconds ----
PAUSE 200

REM ---- BOOT-STYLE SELF-CHECK ----
PAPER 0: BRIGHT 1

INK 6: PRINT AT 16, 0; "> SELFCHECK..."
PAUSE 35

INK 7: PRINT AT 17, 2; "POMP DETECTOR ";
GOSUB 9000
INK 2: PRINT "FAIL"
BEEP 0.05, -12

INK 7: PRINT AT 18, 2; "B.S. DETECTOR ";
GOSUB 9000
INK 4: PRINT " OK "
BEEP 0.05, 4

INK 7: PRINT AT 19, 2; "LISP CORE     ";
GOSUB 9000
INK 6: PRINT " HOT"
BEEP 0.05, 8

INK 7: PRINT AT 20, 2; "JVM           ";
GOSUB 9000
INK 2: PRINT "WONTFIX"
BEEP 0.05, -18

INK 7: PRINT AT 21, 2; "SCHEMA OBJET  ";
GOSUB 9000
INK 4: PRINT " v25"
BEEP 0.05, 7

INK 7: PRINT AT 22, 2; "ODDITY GEN.   ";
GOSUB 9000
INK 5: PRINT " INF"
BEEP 0.05, 10

REM ---- The Spectrum thinks, then states a fact. ----
PAUSE 80

INK 7: PRINT AT 23, 0; "> ";
INK 7: FLASH 1: PRINT "_";: FLASH 0
PAUSE 150

REM Erase the cursor, then type the line one char at a time.
PRINT AT 23, 2; " ";

DIM line$ AS STRING
LET line$ = "STILL HERE."
DIM j AS UByte
INK 6
FOR j = 1 TO LEN(line$)
    PRINT AT 23, 1 + j; line$(j TO j)
    BEEP 0.01, 6
    PAUSE 6
NEXT j

REM Final cursor that blinks via the FLASH attribute, forever.
INK 6: FLASH 1: PRINT AT 23, 2 + LEN(line$); "_"
FLASH 0

REM Sit. Don't loop. Don't summon attention.
DO
    PAUSE 50
LOOP

REM ---- subroutine: animate 9 dots ----
9000 FOR k = 1 TO 9
    PRINT ".";
    PAUSE 2
NEXT k
PRINT " ";
RETURN
