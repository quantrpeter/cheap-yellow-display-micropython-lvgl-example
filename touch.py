import lcd_bus
from micropython import const
import machine
import time  # Add time module for clock functionality
import xpt2046
import fs_driver

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
 
_TOUCH_CS = const(33)
_TOUCH_FREQ = const(10_000_000)
 
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
 
import ili9341
import lvgl as lv
 
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
    rgb565_byte_swap=True,
)
 
# display.set_power(True)
display.init(1)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.set_backlight(100)

spi_bus_touch = machine.SPI.Bus(
    host=2,
    mosi=32,
    miso=39,
    sck=25
)

touch_dev = machine.SPI.Device(
   spi_bus=spi_bus_touch,
   freq=_TOUCH_FREQ,
   cs=_TOUCH_CS,
)
 
indev = xpt2046.XPT2046(touch_dev,debug=True,startup_rotation=lv.DISPLAY_ROTATION._90)
# indev.calibrate()

scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)  # White background

# SemiBlock label at the top
semiblock_label = lv.label(scrn)
semiblock_label.set_text("SemiBlock")
semiblock_label.align(lv.ALIGN.TOP_MID, -45, 20)
semiblock_label.set_style_text_color(lv.color_hex(0xFF80C0), 0)  # Pinkly blue color
semiblock_label.set_style_transform_scale(600, 0)  # Scale text to 200% (2x bigger)

# import task_handler
# th = task_handler.TaskHandler()

def event_cb(self,e):
	print("Clicked", e)
	btn = e.get_target_obj()
	label = btn.get_child(0)
	label.set_text(str(self.cnt))
      
btn = lv.button(scrn)
btn.set_size(100, 50)
btn.center()
btn.add_event_cb(event_cb, lv.EVENT.CLICKED | lv.EVENT.PRESSED | lv.EVENT.RELEASED, None)
label = lv.label(btn)
label.set_text("Click me!")
label.center()

while True:
    time.sleep_ms(10)
    lv.tick_inc(10)
    lv.task_handler()
