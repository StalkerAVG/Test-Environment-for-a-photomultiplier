'''
Use when the Analog Discovery was locked by a different device
'''

import ctypes
import sys

def force_reset():
    print("Loading DWF driver...")
    try:
        # Load the Digilent WaveForms Library (dwf.dll on Windows)
        if sys.platform.startswith("win"):
            dwf = ctypes.cdll.dwf
        elif sys.platform.startswith("darwin"):
             # MacOS path (standard install)
            dwf = ctypes.cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
             # Linux path
            dwf = ctypes.cdll.LoadLibrary("libdwf.so")
            
        print("Attempting FDwfDeviceCloseAll()...")
        # Call the C function directly
        dwf.FDwfDeviceCloseAll()
        print("Success: Command sent to driver.")
        
    except Exception as e:
        print(f"Failed to load driver or close handles: {e}")
        print("Ensure WaveForms Runtime is installed.")

if __name__ == "__main__":
    force_reset()