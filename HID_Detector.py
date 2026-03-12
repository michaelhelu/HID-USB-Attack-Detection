import time
import threading
import wmi
import pythoncom
import os  # for shutdown command

# USB HID device you want to trigger shutdown
TARGET_VID_PID = "VID_05AC&PID_020B"

def monitor_usb():
    pythoncom.CoInitialize()  # COM must be initialized in thread
    c = wmi.WMI()
    watcher = c.watch_for(notification_type="Creation", wmi_class="Win32_Keyboard")

    while True:
        device = watcher()
        name = device.Name
        pnp_id = device.PNPDeviceID

        print(f"[ALERT] New keyboard detected: {name} (PNPDeviceID: {pnp_id})")

        # Check if this is the specific HID device
        if TARGET_VID_PID in pnp_id:
            print("⚠️ HID device detected! Shutting down the computer...")
            # Shutdown immediately
            os.system("shutdown /s /t 0")
# Run monitoring in a thread
usb_thread = threading.Thread(target=monitor_usb, daemon=True)
usb_thread.start()

print("[INFO] Monitoring for new keyboards (HID devices). Press Ctrl+C to exit.")
while True:
    time.sleep(1)