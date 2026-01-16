import dwfpy as dwf
import time

def connect():
    try:
        device = dwf.Device()
        device.open()
        device.reset()
        return device
    except Exception:
        return None

def disconnect(device) -> None:
    if device:
        try:
            device.close()
            print("Disconnected successfully.")
        except Exception as e:
            print(f"Error disconnecting: {e}")

if __name__ == "__main__":
    try:
        dev = connect()
        print(f"Connected to: {dev.name}")
        disconnect(dev)
    except Exception as e:
        print(e)