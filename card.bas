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

REM ---- Stats panel (rows 16..22) ----
PAPER 0: BRIGHT 1

INK 5: PRINT AT 16, 1; "CLASS"; : INK 7: PRINT "   : "; : INK 6: PRINT "ERUDITE CURMUDGEON"
INK 5: PRINT AT 17, 1; "TONGUES"; : INK 7: PRINT " : "; : INK 6: PRINT "LISP, FORTH, NOT JVM"
INK 5: PRINT AT 18, 1; "TROPHIES"; : INK 7: PRINT ": "; : INK 4: PRINT "LONGEST-LIVED SCHEMA"
INK 4: PRINT AT 19, 12; "INVENTOR OF ODDITIES"
INK 4: PRINT AT 20, 12; "DEEPEST THINKER"
INK 3: PRINT AT 21, 4; CHR$(34); "I SEEK NOT ATTENTION"; CHR$(34)

REM ---- A short ascending tune. Thoughtful, not triumphant. ----
BEEP 0.07, -5
BEEP 0.07,  0
BEEP 0.07,  4
BEEP 0.07,  7
BEEP 0.30, 12

REM ---- Marquee on row 23 ----
DIM m AS STRING
LET m = "   *   TWENTY-FIVE YEARS   *   FROM THE MESOZOIC   *   THINGS WORK ON THE FIRST TRY, WITH STRANGELY HIGH FREQUENCY   *   NO POMP. NO FANFARE. JUST OBJECTS THAT OUTLIVE THE SCHEMA.   "
DIM mm AS STRING
LET mm = m + m

DIM i AS UInteger
DIM L AS UInteger
LET L = LEN(m)

INK 7: BRIGHT 0
DO
    FOR i = 1 TO L
        PRINT AT 23, 0; mm(i TO i + 31)
        PAUSE 3
        IF INKEY$ <> "" THEN EXIT DO
    NEXT i
LOOP

PAUSE 0
