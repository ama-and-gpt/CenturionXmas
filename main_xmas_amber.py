# main_modular_amber.py
# Centurion — Christmas Mode (neve + trenó ASCII + mensagem)

import time
import gc
import urandom

AMBER = 0x03F5
BLACK = 0x0000
WHITE = 0xFFFF
MSG_Y = 90
MSG_H = 50   # cobre as duas linhas em size=2

# --------------------------------------------------
# ASCII do trenó — dois frames (pernas da rena)
# --------------------------------------------------
SLED_FRAMES = [
    [   # frame 0
        " \\o##o/        Y",
        " |####|--- *OOo=",
        "_|_____/   /  \\"
    ],
    [   # frame 1 (pernas alternadas)
        " \\#oo#/       Y",
        " |####|--- *OOo",
        "_|_____/   \\ /"
    ]
]

SLED = SLED_FRAMES[0]

SLED_W = max(len(l) for l in SLED_FRAMES[0]) * 6
SLED_H = len(SLED_FRAMES[0]) * 9

SLED_Y = 38
CENTER_X = (320 - SLED_W) // 2

# --------------------------------------------------
# Neve
# --------------------------------------------------
FLAKE_COUNT = 18

def init_snow():
    flakes = []
    for _ in range(FLAKE_COUNT):
        flakes.append({
            "x": urandom.getrandbits(9) % 320,
            "y": urandom.getrandbits(8) % 172,
            "s": 1 + (urandom.getrandbits(2) & 1)
        })
    return flakes

def update_snow(lcd, flakes):
    for f in flakes:
        lcd.pixel(f["x"], f["y"], BLACK)

        f["y"] += f["s"]
        if f["y"] >= 172:
            f["y"] = 0
            f["x"] = urandom.getrandbits(9) % 320

        lcd.pixel(f["x"], f["y"], AMBER)



# --------------------------------------------------
# Trenó
# --------------------------------------------------
def set_sled_frame(i):
    global SLED
    SLED = SLED_FRAMES[i & 1]

def draw_sled(lcd, x):
    # fora do ecrã à direita → NÃO desenhar
    if x >= 320:
        return

    y = SLED_Y
    char_w = 6

    for line in SLED:
        draw_x = x
        start = 0

        # clipping à esquerda
        if draw_x < 0:
            start = (-draw_x) // char_w
            draw_x = 0

        # se depois do clipping ainda estiver fora → ignora
        if draw_x >= 320:
            y += 9
            continue

        # clipping à direita (seguro)
        max_chars = (320 - draw_x) // char_w
        if max_chars <= 0:
            y += 9
            continue

        visible = line[start:start + max_chars]
        if visible:
            lcd.write_text(visible, draw_x, y, 1, AMBER)

        y += 9

def clear_sled(lcd):
    lcd.fill_rect(
        0,
        SLED_Y - 1,
        320,
        SLED_H + 2,
        BLACK
    )

# --------------------------------------------------
# Mensagem
# --------------------------------------------------
def show_message(lcd):
    lcd.write_text("FELIZ NATAL", 85, 95, 2, AMBER)
    lcd.write_text("MERRY CHRISTMAS", 50, 120, 2, AMBER)
    lcd.show()

def clear_message(lcd):
    lcd.fill_rect(
        0,
        MSG_Y - 2,
        320,
        MSG_H,
        BLACK
    )

# --------------------------------------------------
# Sequência completa do trenó
# --------------------------------------------------
def run_sled_sequence(lcd, flakes):
    # ----------------------------
    # 1) Entrada pela esquerda
    # ----------------------------
    x = -SLED_W
    step = 0
    while x < CENTER_X:
        clear_sled(lcd)
        x += 4

        set_sled_frame(step)
        step += 1
        draw_sled(lcd, x)

        update_snow(lcd, flakes)
        lcd.show()
        time.sleep(0.04)

    # alinhar exatamente no centro
    x = CENTER_X
    clear_sled(lcd)
    set_sled_frame(0)
    draw_sled(lcd, x)
    clear_message(lcd)
    show_message(lcd)
    lcd.show()

    # ----------------------------
    # 2) Parado + mensagem (10 s)
    # ----------------------------
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < 10_000:
        update_snow(lcd, flakes)
        lcd.show()
        time.sleep(0.06)

    # ----------------------------
    # 3) Saída pela direita
    # ----------------------------
    step = 0
    clear_sled(lcd)
    clear_message(lcd)
    while x < 320:
        clear_sled(lcd)
        x += 4

        set_sled_frame(step)
        step += 1
        draw_sled(lcd, x)

        update_snow(lcd, flakes)
        lcd.show()
        time.sleep(0.04)

    # ----------------------------
    # 4) Pausa pós-saída (5 s)
    # ----------------------------
    clear_sled(lcd)
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < 5_000:
        update_snow(lcd, flakes)
        lcd.show()
        time.sleep(0.06)

# --------------------------------------------------
# Entry point chamado pelo main.py
# --------------------------------------------------
def start_dashboard(lcd):
    lcd.fill(BLACK)
    lcd.show()
    gc.collect()

    flakes = init_snow()

    while True:
        run_sled_sequence(lcd, flakes)

# --------------------------------------------------
# Execução autónoma / REPL
# --------------------------------------------------
def run():
    from lcd import LCD_1inch47
    from machine import Pin, PWM

    # inicializar LCD
    lcd = LCD_1inch47()

    # backlight ON
    bl = PWM(Pin(21))
    bl.freq(1000)
    bl.duty_u16(35000)

    # pequeno delay para estabilizar
    time.sleep(0.2)

    # arrancar animação
    start_dashboard(lcd)


# auto-run se for main.py
if __name__ == "__main__":
    run()
