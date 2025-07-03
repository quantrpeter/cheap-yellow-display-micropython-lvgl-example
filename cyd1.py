import lcd_bus
from micropython import const
import machine


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
    rgb565_byte_swap=True
)

import task_handler  # NOQA
import xpt2046  # NOQA

display.set_power(True)
display.init(1)
display.set_color_inversion(False)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.set_backlight(100)

#touch_dev = machine.SPI.Device(
#    spi_bus=spi_bus,
#    freq=_TOUCH_FREQ,
#    cs=_TOUCH_CS
#)

#indev = xpt2046.XPT2046(touch_dev,debug=False,startup_rotation=lv.DISPLAY_ROTATION._0)

#indev.calibrate()

th = task_handler.TaskHandler()

scrn = lv.screen_active()
#scrn.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)

#btnm = lv.buttonmatrix(scrn)
#btnm.add_event_cb(lambda e: btnm_event_handler(e,scrn),lv.EVENT.VALUE_CHANGED, None)
#btnm.set_size(230,120)
#btnm.align(1,5,5)

tabview = lv.tabview(scrn)
tabview.set_tab_bar_size(30)
# tabview.set_style_bg_color(lv.color_hex(0xffffff), 0)  # White background
# tabview.set_style_bg_opa(255, 0)  # Make sure it's fully opaque


tab1 = tabview.add_tab("Tab 1")
tab2 = tabview.add_tab("Tab 2")
tab3 = tabview.add_tab("Tab 3")

# Add content to the tabs
label1 = lv.label(tab1)
label1.set_text("This is the content of Tab 1")

#label2 = lv.label(tab2)
#label2.set_text("This is the content of Tab 2")

label3 = lv.label(tab3)
label3.set_text("This is the content of Tab 3")




btn = lv.button(tab1)
btn.center()
btn.set_size(100,50)
btn.set_style_bg_color(lv.color_make(255, 0, 0), 0)  # RGB: Red=255, Green=0, Blue=0
lbl = lv.label(btn)
lbl.set_text('Start')
lbl.center()

# Add second button
btn2 = lv.button(tab1)
btn2.set_size(100,50)
btn2.align(lv.ALIGN.CENTER, 0, 60)  # Position below the first button
lbl2 = lv.label(btn2)
lbl2.set_text('Stop')
lbl2.center()

# Add toggle button
btn3 = lv.button(tab1)
btn3.set_size(100,50)
btn3.align(lv.ALIGN.CENTER, 0, 120)  # Position below the second button
lbl3 = lv.label(btn3)
lbl3.set_text('Toggle')
btn3.add_event_cb(lambda e: btnm_event_handler(e, tab1), lv.EVENT.VALUE_CHANGED, None)
btn3.set_style_bg_color(lv.color_make(255, 0, 0), 0)  # RGB: Red=0, Green=255, Blue=0
btn3.set_style_bg_opa(255, 0)  # Make sure the background is fully opaque

tab2.set_flex_flow(lv.FLEX_FLOW.COLUMN)
lab21 = lv.label(tab2)
lab21.set_text('Group 1')
chk21 = lv.checkbox(tab2)
chk21.set_text('Option 1')
chk22 = lv.checkbox(tab2)
chk22.set_text('Option 2')
chk23 = lv.checkbox(tab2)
chk23.set_text('Option 3')
chk24 = lv.checkbox(tab2)
chk24.set_text('Option 4')
lab22 = lv.label(tab2)
lab22.set_text('Group 2')
chk25 = lv.checkbox(tab2)
chk25.set_text('Option 5')
chk26 = lv.checkbox(tab2)
chk26.set_text('Option 6')
chk27 = lv.checkbox(tab2)
chk27.set_text('Option 7')
chk28 = lv.checkbox(tab2)
chk28.set_text('Option 8')

o = 1
def btnm_event_handler(e,ta):
    global o
    obj = e.get_target()
    o=obj
    print("Toggled")
