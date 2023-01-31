# Data File to Import Data

# ========================================================================================
# Libraries
# ========================================================================================
import serial

ser = serial.Serial('COM6', 38400, timeout=0, parity=serial.PARITY_EVEN, rtscts = 1)

while True:
    s = ser.read(100)

    try:
        s = ord(s)
    except:
        s = 0
        
    print(s)
