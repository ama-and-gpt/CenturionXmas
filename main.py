# main.py – Centurion boot → status → amber dashboard

from lcd import LCD_1inch47
import time

# Init LCD
lcd = LCD_1inch47()

# Force backlight ON early
from machine import Pin, PWM
bl = PWM(Pin(21))
bl.freq(1000)
bl.duty_u16(35000)

time.sleep(0.2)
lcd.fill(0); lcd.show()

# Run Centurion boot stages
try:
    from splash_centi_amber import run_splash_centi
    run_splash_centi(lcd)
except Exception as e:
    print("Centurion boot error:", e)

try:
    from splash_centi_status import run_splash_centi_status
    run_splash_centi_status(lcd)
except Exception as e:
    print("Centurion status error:", e)

# ---- Handoff visível + GC antes do dashboard ----
import gc, time
lcd.fill(0)
lcd.write_text("HANDOFF TO DASHBOARD...", 8, 76, 1, 0x03F5)
lcd.show()
gc.collect()
time.sleep(0.25)
print("FREE RAM:", gc.mem_free())
time.sleep(0.30)

# make LCD available to imported modules
globals()["lcd"] = lcd

# ---- Carregar dashboard com proteção ----
try:
    import main_xmas_amber
    main_xmas_amber.start_dashboard(lcd)

except Exception as e:
    # se algo falhar, mostra no LCD e não parece “preso”
    msg = "DASHBOARD ERROR"
    lcd.fill(0)
    lcd.write_text(msg, 8, 60, 1, 0x03F5)
    lcd.write_text(str(e)[:30], 8, 76, 1, 0x03F5)
    print("FREE RAM:", gc.mem_free())
    lcd.show()
    raise
