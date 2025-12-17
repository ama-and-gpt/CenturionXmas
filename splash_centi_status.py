# splash_centi_status.py — Centurion STATUS DISPLAY with scrolling + D=LoadStatus

import time

AMBER = 0x03F5
BLACK = 0x0000

MAX_LINES = 16   # fits safely on 320x172
lines_buf = []

STATUS_LINES = [
"STATUS DISPLAY REV 7.13    SYSTEM DATE: 02/23/88",
"",
"MAXIMUM TRANSIENT SIZE     18K",
"TRANSIENT USED            0.380K",
"TRANSIENT USED           14.990K",
"",
"TOTAL SYSTEM RAM         256K",
"OPSYS SIZE                38K",
"PARTITION SIZES            6K",
"TRANSIENT ALLOCATED        2K",
"MEMORY AVAILABLE         210K",
"",
"VOLUME   DISK   PARTITION   JOB",
"# NAME     DATE     TYPE / SIZE / FLAGS ",
"0 SOFTEM    02/23/88 HAWK/PERTEC  STLQ ",
"1 PROGRAMS  09/13/96 HAWK/PERTEC  WP ",
"2 DUMMY                        2 DUMMY",
"3 DUMMY                        3 DUMMY",
"",

"CRT0 READY"

]

def redraw(lcd, cursor=True):
    lcd.fill(BLACK)
    y = 2
    for ln in lines_buf:
        lcd.write_text(ln, 2, y, 1, AMBER)
        y += 9
    if cursor:
        lcd.fill_rect(2, y, 6, 8, AMBER)
    lcd.show()

def term_put(lcd, text, delay=0.03):
    global lines_buf

    lines_buf.append(text)
    if len(lines_buf) > MAX_LINES:
        lines_buf.pop(0)

    redraw(lcd, cursor=True)
    time.sleep(delay)

def blink_cursor(lcd, ms=500):
    start = time.ticks_ms()
    cursor_on = True
    while time.ticks_diff(time.ticks_ms(), start) < ms:
        cursor_on = not cursor_on
        redraw(lcd, cursor=cursor_on)
        time.sleep(0.15)

def type_cmd(lcd, text, delay=0.03):
    # type like terminal: char by char
    y = 2 + len(lines_buf)*9
    x = 2
    for ch in text:
        lcd.write_text(ch, x, y, 1, AMBER)
        x += 6
        lcd.show()
        time.sleep(delay)
    lines_buf.append(text)
    if len(lines_buf) > MAX_LINES:
        lines_buf.pop(0)
    redraw(lcd, cursor=True)

def run_splash_centi_status(lcd):
    global lines_buf
    lines_buf = []

    lcd.fill(BLACK); lcd.show()
    time.sleep(0.15)

    for line in STATUS_LINES:
        term_put(lcd, line, 0.03)

# --- short cursor pause ---
    blink_cursor(lcd, 200)

# --- blank line to subir o comando ---
    term_put(lcd, "", 0.01)

# --- D=LoadStatus + dots animados ---
    type_cmd(lcd, "D=LoadStatus", 0.02)
    for i in range(1, 5):          # ., .., ..., ....
        term_put(lcd, "." * i, 0.045)

# --- pequena pausa e SAIR (não limpar o ecrã à força) ---
    time.sleep(0.25)
    return
    