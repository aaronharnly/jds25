REM === JDS - BIRTHDAY EDITION ===

REM ============================================================
REM  STAGE 1: QUINE INTRO
REM   Boot to a white Spectrum BASIC editor, "type" the program's
REM   own source one chunk at a time. The first thing the recipient
REM   sees is the program describing itself.
REM ============================================================

BORDER 7: PAPER 7: INK 0: BRIGHT 0
CLS

REM Iconic Spectrum boot prompt
PRINT "(C) 1982 Sinclair Research Ltd"
PAUSE 60
PRINT
PAUSE 20

typeSrc("REM === JDS - BIRTHDAY ===")
typeSrc("")
typeSrc("BORDER 0")
typeSrc("PAPER 0")
typeSrc("INK 7")
typeSrc("CLS")
typeSrc("")
typeSrc("REM LOAD SCREEN$")
typeSrc("ASM")
typeSrc("    ld hl, scr_data")
typeSrc("    ld de, 16384")
typeSrc("    ld bc, 6912")
typeSrc("    ldir")
typeSrc("    jp scr_after")
typeSrc("scr_data:")
typeSrc("    INCBIN ""card.scr""")
typeSrc("scr_after:")
typeSrc("END ASM")
typeSrc("")
typeSrc("PAUSE 200")
typeSrc("")
typeSrc("runBirthdayCheck")
typeSrc("")
typeSrc("incrementAge")
typeSrc("END")

PAUSE 40

REM ============================================================
REM  STAGE 2: SIMULATED TAPE LOADER
REM   Border flashes red/cyan with a pseudo-random screech.
REM   Authentic Spectrum tape-load aesthetic for ~2 seconds.
REM ============================================================

DIM f AS UInteger
FOR f = 1 TO 180
    BORDER 2: BEEP 0.003, INT(RND * 50) - 10
    BORDER 5: BEEP 0.003, INT(RND * 50) - 10
NEXT f
BORDER 0

REM ============================================================
REM  STAGE 3: SPLASH + BOOT SEQUENCE
REM ============================================================

BORDER 0: PAPER 0: INK 7: BRIGHT 1
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

PAPER 0: BRIGHT 1

REM ---- Header ----
INK 6: PRINT AT 16, 0; "> SELFCHECK...";
PAUSE 50

REM ---- Stat lines: each label appears, dot leader animates,
REM      value area scrambles random chars, then settles. ----

REM YOUTHFULNESS OF MIND --> counts up to a perfect score
labelDots(17, "YOUTHFULNESS OF MIND")
noiseValue(17, 8)
showVal(17, "10", 3): PAUSE 5
showVal(17, "30", 3): PAUSE 4
showVal(17, "55", 3): PAUSE 4
showVal(17, "75", 3): PAUSE 3
showVal(17, "90", 3): PAUSE 3
showVal(17, "97", 3): PAUSE 3
showVal(17, "100", 4)
BEEP 0.04, 12
PAUSE 20

REM POMP TOLERANCE --> 0
labelDots(18, "POMP TOLERANCE")
noiseValue(18, 6)
showVal(18, "0", 7)
BEEP 0.03, -3
PAUSE 20

REM CAKE TOLERANCE --> 0, no appeal
labelDots(19, "CAKE TOLERANCE")
noiseValue(19, 8)
showVal(19, "0", 7)
BEEP 0.03, -5
PAUSE 20

REM LISP AFFINITY --> 95
labelDots(20, "LISP AFFINITY")
noiseValue(20, 8)
showVal(20, "95", 6)
BEEP 0.04, 8
PAUSE 20

REM PROLOG AFFINITY --> 99
labelDots(21, "PROLOG AFFINITY")
noiseValue(21, 8)
showVal(21, "99", 6)
BEEP 0.04, 10
PAUSE 20

REM CANDLE COUNT --> counts up, hits UByte ceiling, overflows
labelDots(22, "CANDLE COUNT")
noiseValue(22, 8)
showVal(22, "100", 3): PAUSE 5
showVal(22, "150", 3): PAUSE 4
showVal(22, "200", 3): PAUSE 4
showVal(22, "240", 3): PAUSE 3
showVal(22, "250", 3): PAUSE 3
showVal(22, "254", 3): PAUSE 3
showVal(22, "255", 3): PAUSE 10
INK 2: FLASH 1: PRINT AT 22, 28; " OVF";
FLASH 0
BEEP 0.06, -14
PAUSE 20

REM ODDITY LEVEL --> long scramble of symbols, eventually INF.
REM Note: row 23 is the bottom row. EVERY PRINT here MUST end with `;`
REM to suppress the implicit newline, otherwise the screen scrolls.
labelDots(23, "ODDITY LEVEL")
DIM s AS UByte
INK 3: PAPER 0: BRIGHT 1
FOR s = 1 TO 32
    PRINT AT 23, 29; CHR$(33 + INT(RND * 90)); CHR$(33 + INT(RND * 90)); CHR$(33 + INT(RND * 90));
    PAUSE 1
NEXT s
PRINT AT 23, 28; "    ";
INK 3: FLASH 1: PRINT AT 23, 29; "INF";
FLASH 0
BEEP 0.10, 18

REM Hold the settled grid briefly
PAUSE 200

REM ---- Stage transition: clear bottom 8 rows ----
PAPER 0: INK 0: BRIGHT 1
DIM rr AS UByte
FOR rr = 16 TO 23
    PRINT AT rr, 0; "                                ";
NEXT rr
PAUSE 50

REM ---- Final message: typed character by character.
REM      He is a Common Lisp loyalist; the card speaks his tongue.
REM      Age stays undisclosed -- he seeks not attention.

typeLine(17, 0, "> (incf age)", 4, 4)
PAUSE 35
typeLine(19, 0, "> ; RESULT: STILL MESOZOIC", 6, 6)
PAUSE 35
typeLine(21, 0, "> HAPPY BIRTHDAY ANYWAY.", 3, 9)

REM Final cursor that blinks via the FLASH attribute, forever.
INK 3: FLASH 1: PRINT AT 21, 24; "_";
FLASH 0

REM Sit. Don't loop. Don't summon attention.
DO
    PAUSE 50
LOOP


REM ============= subroutines =============

REM Type one line of "source code" onto the listing screen.
REM Char-by-char with a small pause every 4 chars so it reads as
REM typing rather than instant LIST output. Empty string = blank line.
REM NB: zxbasic strings are 0-indexed (unlike Sinclair BASIC), so the
REM loop runs 0..LEN-1; a 1-based loop silently eats the first char.
SUB typeSrc(line$ AS STRING)
    DIM j AS UByte
    IF LEN(line$) > 0 THEN
        FOR j = 0 TO LEN(line$) - 1
            PRINT line$(j TO j);
            IF ((j + 1) BAND 3) = 0 THEN PAUSE 1
        NEXT j
    END IF
    PRINT
END SUB

REM Print the label at col 0, then animate a dot leader from
REM (label end + 1) to col 27, leaving cols 28..31 free for the value.
REM Every PRINT ends with `;` so on row 23 we don't trigger a hardware scroll.
SUB labelDots(row AS UByte, label$ AS STRING)
    INK 5: PAPER 0: BRIGHT 1
    PRINT AT row, 0; label$;
    PAUSE 4
    INK 7
    DIM k AS UByte
    FOR k = LEN(label$) + 1 TO 27
        PRINT AT row, k; ".";
        PAUSE 2
    NEXT k
END SUB

REM Show pure noise in cols 29..31 for `frames` ticks.
SUB noiseValue(row AS UByte, frames AS UByte)
    INK 3: PAPER 0: BRIGHT 1
    DIM t AS UByte
    FOR t = 1 TO frames
        PRINT AT row, 29; CHR$(33 + INT(RND * 90)); CHR$(33 + INT(RND * 90)); CHR$(33 + INT(RND * 90));
        PAUSE 1
    NEXT t
END SUB

REM Right-align `val$` at col 31, blanking cols 28..31 first.
REM Trailing `;` on both PRINTs so the cursor doesn't auto-newline off row 23.
SUB showVal(row AS UByte, val$ AS STRING, color AS UByte)
    INK color: PAPER 0: BRIGHT 1
    PRINT AT row, 28; "    ";
    PRINT AT row, 32 - LEN(val$); val$;
END SUB

REM Type a string char-by-char with a faint per-key click.
REM 0-based string indexing (zxbasic default) — see typeSrc note.
SUB typeLine(row AS UByte, col AS UByte, line$ AS STRING, color AS UByte, pitch AS Byte)
    INK color: PAPER 0: BRIGHT 1
    DIM j AS UByte
    FOR j = 0 TO LEN(line$) - 1
        PRINT AT row, col + j; line$(j TO j);
        BEEP 0.008, pitch
        PAUSE 4
    NEXT j
END SUB
