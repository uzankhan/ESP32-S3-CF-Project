# i2c_test.py - COMPLETE FIXED CODE
import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# =============================================
# I2C SCANNER
# =============================================
print("=" * 40)
print("I2C SCANNER")
print("=" * 40)

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# Scan for devices
while not i2c.try_lock():
    pass

try:
    devices = i2c.scan()
    i2c.unlock()
    
    if devices:
        print(f"Found {len(devices)} device(s):")
        for device in devices:
            print(f"  Address: 0x{device:02X} ({device})")
            if device == 0x27:
                print("  >>> LCD found at 0x27!")
            elif device == 0x3F:
                print("  >>> LCD found at 0x3F!")
    else:
        print("No I2C devices found!")
        print("Check:")
        print("  1. Wiring (SDA, SCL, VCC, GND)")
        print("  2. Power supply")
        print("  3. I2C address")
        # Exit if no devices
        while True:
            time.sleep(1)
            
except Exception as e:
    print("Error during scan:", e)
    i2c.unlock()
    while True:
        time.sleep(1)

print("=" * 40)

# =============================================
# LCD TEST (SIRF ADAFRUIT LIBRARY USE KAREIN)
# =============================================
if devices and (0x27 in devices or 0x3F in devices):
    # LCD address decide karein
    lcd_address = 0x27 if 0x27 in devices else 0x3F
    print(f"Using LCD address: 0x{lcd_address:02X}")
    
    try:
        # LCD initialize - SIRF EK TAREEQA
        lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2, address=lcd_address)
        
        # Test messages
        lcd.clear()
        lcd.message = "LCD TEST OK!"
        print("Message 1: 'LCD TEST OK!'")
        time.sleep(2)
        
        lcd.clear()
        lcd.message = f"Addr:\n0x{lcd_address:02X}"
        print(f"Message 2: 'Addr: 0x{lcd_address:02X}'")
        time.sleep(2)
        
        lcd.clear()
        lcd.message = "CircuitPython\nLCD Working!"
        print("Message 3: 'CircuitPython\\nLCD Working!'")
        time.sleep(2)
        
        lcd.clear()
        lcd.message = "TEST\nCOMPLETE!"
        print("Test Complete!")
        time.sleep(2)
        lcd.clear()
        
        print("=" * 40)
        print("✅ LCD TEST PASSED!")
        print("=" * 40)
        
    except Exception as e:
        print("LCD Error:", e)
        print("Check:")
        print("  1. LCD address (0x27 or 0x3F)")
        print("  2. Library files in lib folder")
        print("  3. I2C connections")
else:
    print("❌ LCD NOT FOUND!")
    print("Please check hardware connections")