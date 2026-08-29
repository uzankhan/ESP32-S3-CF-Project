# boot.py - USB settings for ESP32-S3
import usb_cdc
import usb_hid
import storage

# Sirf console enable karein (data disable)
usb_cdc.enable(console=True, data=False)

# HID (keyboard/mouse) disable karein
usb_hid.disable()

# Storage enable (CIRCUITPY drive visible)
storage.enable_usb_drive()

print("boot.py executed - USB endpoints saved!")