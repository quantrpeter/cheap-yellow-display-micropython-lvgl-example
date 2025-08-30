import lcd_bus
from micropython import const
import machine
import time  # Add time module for clock functionality
from fs_driver import fs_register

# Try to import ntptime for NTP sync
try:
    import ntptime
    NTP_AVAILABLE = True
except ImportError:
    NTP_AVAILABLE = False
    print("ntptime not available")

# Try to import network for WiFi
try:
    import network
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False
    print("network not available")

# WiFi Configuration - CHANGE THESE TO YOUR WIFI CREDENTIALS
#WIFI_SSID = "Quantr 2.4G"
#WIFI_PASSWORD = "quantrwi"
WIFI_SSID = "peter 2.4G"
WIFI_PASSWORD = "peter1234"

# Timezone Configuration
TIMEZONE_OFFSET = 8  # Hong Kong is UTC+8 hours
TIMEZONE_NAME = "Hong Kong"
 
 
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

import ili9341  # NOQA
import lvgl as lv  # NOQA

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
 
import task_handler  # NOQA
import xpt2046  # NOQA
 
display.set_power(True)
display.init(1)
# display.set_color_inversion(True)
display.set_rotation(lv.DISPLAY_ROTATION._270)
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
 
indev = xpt2046.XPT2046(touch_dev,debug=False,startup_rotation=lv.DISPLAY_ROTATION._0)
# indev.calibrate()
 
th = task_handler.TaskHandler()

# WiFi connection functions
def connect_wifi():
    """Connect to WiFi network"""
    if not NETWORK_AVAILABLE:
        print("Network module not available")
        return False
    
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        if wlan.isconnected():
            print("WiFi already connected")
            print(f"IP address: {wlan.ifconfig()[0]}")
            return True
        
        print(f"Connecting to WiFi: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection with timeout
        timeout = 10  # 10 seconds timeout
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")
        
        if wlan.isconnected():
            print(f"\nWiFi connected successfully!")
            print(f"IP address: {wlan.ifconfig()[0]}")
            return True
        else:
            print(f"\nWiFi connection failed!")
            return False
            
    except Exception as e:
        print(f"WiFi connection error: {e}")
        return False

def disconnect_wifi():
    """Disconnect from WiFi"""
    if not NETWORK_AVAILABLE:
        return
    
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)
        print("WiFi disconnected")
    except Exception as e:
        print(f"WiFi disconnect error: {e}")

# Time setting functions
def get_local_time():
    """Get time adjusted for Hong Kong timezone (UTC+8)"""
    # Get UTC time
    utc_time = time.time()
    # Add timezone offset (8 hours = 8 * 3600 seconds)
    local_timestamp = utc_time + (TIMEZONE_OFFSET * 3600)
    # Convert to local time structure
    return time.localtime(local_timestamp)

def sync_time_ntp():
    """Try to sync time with NTP server (requires WiFi)"""
    if not NTP_AVAILABLE:
        print("NTP not available")
        return False
    
    if not NETWORK_AVAILABLE:
        print("Network not available")
        return False
    
    try:
        # Check if WiFi is connected
        wlan = network.WLAN(network.STA_IF)
        if wlan.isconnected():
            print("Syncing time with NTP server...")
            ntptime.settime()
            print(f"Time synced successfully! (UTC time will be converted to {TIMEZONE_NAME})")
            return True
        else:
            print("WiFi not connected, cannot sync NTP time")
            return False
    except Exception as e:
        print(f"NTP sync failed: {e}")
        return False

def set_manual_time():
    """Set time manually - modify the values as needed"""
    # Format: (year, month, day, weekday, hour, minute, second, microsecond)
    rtc = machine.RTC()
    # Set to July 4, 2025, 14:30:00 Hong Kong time
    # Note: This sets the RTC to UTC time, but we'll display Hong Kong time
    # So if we want to display 14:30 HK time, we set RTC to 06:30 UTC
    utc_hour = 14 - TIMEZONE_OFFSET  # Convert HK time to UTC
    if utc_hour < 0:
        utc_hour += 24
    rtc.datetime((2025, 7, 4, 5, utc_hour, 30, 0, 0))
    print(f"Manual time set to: 2025-07-04 14:30:00 {TIMEZONE_NAME} time")

def setup_time():
    """Setup the system time"""
    print("Setting up time...")
    
    # First try to connect to WiFi
    # if connect_wifi():
    #     # If WiFi connected, try NTP sync
    #     if sync_time_ntp():
    #         print(f"Time setup complete via NTP (displaying {TIMEZONE_NAME} time)")
    #         return
    
    # If WiFi or NTP failed, use manual time
    print("Using manual time setting")
    set_manual_time()
    
    # Print current time to verify (Hong Kong time)
    current = get_local_time()
    print(f"Current {TIMEZONE_NAME} time: {current[0]}-{current[1]:02d}-{current[2]:02d} {current[3]:02d}:{current[4]:02d}:{current[5]:02d}")

# Initialize time
setup_time()

scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)  # White background

# Set background image
try:
    fs_drv = lv.fs_drv_t()
    fs_register(fs_drv, "S")
    bg_img = lv.image(scrn)
    # bg_img.set_src("S:colorful20.png")
    bg_img.set_src("S:clock1.png")
    # bg_img.set_size(140, 140)
    bg_img.set_pos(10, 10)
    # bg_img.align(lv.ALIGN.CENTER, 0, 0)
    # bg_img.set_zoom(256)  # 256 = 1x zoom
    # bg_img.set_style_opa(lv.OPA.COVER, 0)
except Exception as e:
    print("Failed to load background image:", e)

def btnm_event_handler(e, scrn):
    """Handle button matrix events"""
    obj = e.get_target()
    txt = obj.get_button_text(obj.get_selected_button())
    print(f"Button pressed: {txt}")

# Comment out button matrix to remove btn1-btn5 display
# btnm = lv.buttonmatrix(scrn)
# btnm.add_event_cb(lambda e: btnm_event_handler(e,scrn),lv.EVENT.VALUE_CHANGED, None)
# btnm.set_size(230,120)
# btnm.align(1,5,5)

# SemiBlock label at the top
semiblock_label = lv.label(scrn)
semiblock_label.set_text("SemiBlock")
semiblock_label.align(lv.ALIGN.TOP_MID, -45, 20)
semiblock_label.set_style_text_color(lv.color_hex(0xFF80C0), 0)  # Pinkly blue color
semiblock_label.set_style_transform_scale(600, 0)  # Scale text to 200% (2x bigger)

# Digital clock display - large font
clock_label = lv.label(scrn)
clock_label.set_text("00:00:00")
clock_label.align(lv.ALIGN.LEFT_MID, 50, -15)
clock_label.set_style_transform_scale(500, 0)  # Scale text to 300% (3x bigger)
clock_label.set_style_text_color(lv.color_hex(0x000000), 0)  # Black color

# Date display
date_label = lv.label(scrn)
date_label.set_text("2025-01-01")
date_label.align(lv.ALIGN.LEFT_MID, 50, 30)
date_label.set_style_transform_scale(500, 0)
date_label.set_style_text_color(lv.color_hex(0x0000FF), 0)  # Blue color

# Day of week display
day_label = lv.label(scrn)
day_label.set_text("Monday")
day_label.align(lv.ALIGN.LEFT_MID, 50, 75)
day_label.set_style_transform_scale(500, 0)
day_label.set_style_text_color(lv.color_hex(0x0000FF), 0)  # Blue color

# Clock frame/border
clock_frame = lv.obj(scrn)
clock_frame.set_size(280, 140)
clock_frame.align(lv.ALIGN.CENTER, 0, 40)
clock_frame.set_style_border_width(2, 0)
clock_frame.set_style_border_color(lv.color_hex(0xFF80C0), 0)  # Gray border
clock_frame.set_style_bg_opa(lv.OPA.TRANSP, 0)  # Transparent background
clock_frame.set_style_radius(10, 0)  # Rounded corners

# Don't move labels to frame - keep them on main screen for proper updates

def update_clock():
    """Update the clock display with current time in Hong Kong timezone"""
    # Use Hong Kong local time instead of system time
    current_time = get_local_time()
    
    # Format time as HH:MM:SS
    time_str = "{:02d}:{:02d}:{:02d}".format(
        current_time[3],  # hour
        current_time[4],  # minute
        current_time[5]   # second
    )
    
    # Format date as YYYY-MM-DD
    date_str = "{:04d}-{:02d}-{:02d}".format(
        current_time[0],  # year
        current_time[1],  # month
        current_time[2]   # day
    )
    
    # Get day of week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_str = days[current_time[6]]
    
    clock_label.set_text(time_str)
    date_label.set_text(date_str)
    day_label.set_text(day_str)
    
    # Debug print to verify time is being read correctly
    print(f"{TIMEZONE_NAME} Time: {time_str}, Date: {date_str}, Day: {day_str}")

# Create a timer to update the clock every second
clock_timer = lv.timer_create(lambda timer: update_clock(), 1000, None)

# Initial clock update
update_clock()
