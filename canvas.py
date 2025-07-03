import lcd_bus
from micropython import const
import machine
import ili9341
import lvgl as lv
from time import sleep

# display settings
_WIDTH = const(240)
_HEIGHT = const(320)
_BL = const(21)
_RST = const(17)
_DC = const(2)

_MOSI = const(13)
#_MISO = const(12)
_SCK = const(14)
_HOST = const(1)  # SPI2

_LCD_CS = const(15)
_LCD_FREQ = const(40000000)

#_TOUCH_CS = const(9)
#_TOUCH_FREQ = const(1000000)

spi_bus = machine.SPI.Bus(
    host=_HOST,
    mosi=_MOSI,
    #miso=_MISO,
    sck=_SCK
)

display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    freq=_LCD_FREQ,
    dc=_DC,
    cs=_LCD_CS,
)

display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=_WIDTH,
    display_height=_HEIGHT,
    reset_pin=_RST,
    reset_state=ili9341.STATE_LOW,
    backlight_pin=_BL,
    backlight_on_state=ili9341.STATE_HIGH,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=ili9341.BYTE_ORDER_BGR,
    rgb565_byte_swap=True
)

import task_handler
th = task_handler.TaskHandler()

display.set_power(True)
display.init(1)
display.set_color_inversion(False)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.set_backlight(100)


scrn = lv.screen_active()

# Create a canvas to draw colorful pattern
canvas = lv.canvas(scrn)
canvas.set_size(120, 120)
canvas.align(lv.ALIGN.CENTER, 0, 0)

# Create buffer for canvas (RGB565 format, 2 bytes per pixel)
canvas_buffer = bytearray(120 * 120 * 2)
canvas.set_buffer(canvas_buffer, 120, 120, lv.COLOR_FORMAT.RGB565)

# Fill canvas with colorful pattern
canvas.fill_bg(lv.color_hex(0x000000), lv.OPA.COVER)

# Draw colorful rectangles
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
for i, color in enumerate(colors):
    x = (i % 3) * 40
    y = (i // 3) * 40
    canvas.set_style_bg_color(lv.color_hex(color), 0)
    # Draw filled rectangle
    for dy in range(35):
        for dx in range(35):
            canvas.set_px(x + dx, y + dy, lv.color_hex(color), lv.OPA.COVER)

# Add a label to show status
label1 = lv.label(scrn)
label1.set_text("Colorful Canvas Pattern")
label1.align(lv.ALIGN.TOP_MID, 0, 10)

print("Canvas pattern created!")

sleep(2)
