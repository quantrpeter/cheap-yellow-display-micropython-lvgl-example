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

display.set_power(True)
display.init(1)
display.set_color_inversion(False)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.set_backlight(100)

scrn = lv.screen_active()

label1 = lv.label(scrn)
label1.set_text("Colorful Canvas Pattern")
label1.align(lv.ALIGN.TOP_MID, 0, 10)

# Use LVGL's file system image support to avoid loading the whole file into RAM
img = lv.image(scrn)
img.set_src("colorful.bin")
img.set_size(200, 200)
img.center()

import task_handler
task_handler.TaskHandler()

sleep(2)
