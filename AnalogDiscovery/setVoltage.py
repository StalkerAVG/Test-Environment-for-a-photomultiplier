import sys
from time import sleep
import dwfpy as dwf
import AD


def powerOn(device: dwf.Device):
    """Enable power supply outputs"""
    device.analog_io[0][0].value = True
    device.analog_io.master_enable = True

def setVoltage(device: dwf.Device, input_channel: int = 0, output_channel: int = 0, voltage: float = 0.0) -> float:
    """
    Set DC voltage on specified wavegen channel (W1 = channel 0, W2 = channel 1)
    
    Args:
        device: dwfpy Device object
        channel: Output channel (0 for W1, 1 for W2)
        voltage: Desired voltage value in volts
    
    Returns:
        measuered voltage after setting
    """

    powerOn(device)

    sleep(0.5)

    try:
        device.analog_output[input_channel].setup(
            function='dc',
            offset=voltage,
            amplitude=0.0,
            start=True
        )
        
        sleep(0.5)

        return AD.measure(device, channel=output_channel)
        
    except dwf.WaveformsError as e:
        raise Exception(f"Waveforms Error: {e}")
    except Exception as e:
        raise RuntimeError(f"Error setting voltage: {e}")



if __name__ == "__main__":
    args = sys.argv[1:]
    
    if len(args) < 2:
        raise ValueError("Usage: python setVoltage.py <input channel (0 or 1)> <output channel (0 or 1)> <voltage in volts>")
    
    try:
        input_channel = int(args[0])
        output_channel = int(args[1])
        voltage = float(args[2])
        
        if input_channel not in [0, 1]:
            raise ValueError("Channel must be 0 (W1) or 1 (W2)")
        
        if output_channel not in [0, 1]:
            raise ValueError("Channel must be 0 (1+) or 1 (2+)")
        
        with dwf.Device() as device:
            print(f"Found device: {device.name} ({device.serial_number})")
            
            powerOn(device)
            sleep(0.5)
            
            # Set the voltage
            success = setVoltage(device, input_channel, output_channel, voltage)
            
            if success:
                print(f"Voltage set to {success}V on W{input_channel+1} output")
                sys.exit(0)
            else:
                print("Failed to set voltage")
                sys.exit(1)
                
    except ValueError as e:
        print(f"Invalid argument: {e}")
        print("Channel must be an integer (0 or 1) and voltage must be a number")
        sys.exit(1)
    except dwf.WaveformsError as e:
        print(f"Waveforms Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)