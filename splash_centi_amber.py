# splash_centi_amber.py — Centurion Boot
import time
import math

AMBER = 0x03F5
BLACK = 0x0000

def type_line(lcd, text, x, y, delay=0.03):
    px = x
    for ch in text:
        lcd.write_text(ch, px, y, 1, AMBER)
        px += 6
        lcd.show()
        time.sleep(delay)

def cursor_block(lcd, x, y, on):
    lcd.fill_rect(x, y, 6, 8, AMBER if on else BLACK)

def run_splash_centi(lcd):
    lcd.fill(BLACK); lcd.show()
    time.sleep(0.2)

    lines = [
        "OS 7.1 - E",
        "",
        "MAX DISK# (H)= 1, SYSTEM DISK (S)= 0",
        "",
        "PREVIOUS SYSTEM DATE: 02/23/88",
        "",
        "ENTER NEW SYSTEM DATE: 022388",
        "ENTER SYSTEM TIME: 120808",
        "",
        "CRT0 READY",
    ]

    y = 5
    for line in lines:
        type_line(lcd, line, 4, y)
        y += 12
        time.sleep(0.03)

    # cursor blink idle
    cx, cy = 4, y
    t0 = time.ticks_ms()
    on = True

    for _ in range(50):  # ~1.5s boot pause
        if time.ticks_diff(time.ticks_ms(), t0) > 300:
            on = not on
            cursor_block(lcd, cx, cy, on)
            lcd.show()
            t0 = time.ticks_ms()
        time.sleep(0.02)

    lcd.fill(BLACK); lcd.show()  # pass to dashboard
