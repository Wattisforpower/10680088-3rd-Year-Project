# Data File to Import Data

# ========================================================================================
# Libraries
# ========================================================================================
import serial

class GetData:
    def __init__(self, COM, BaudRate) -> None:
        self.COMPort = COM
        self.BaudRate = BaudRate
    
    def StartConnection(self) -> None:
        self.COMMS = serial.Serial(self.COMPort, self.BaudRate)
        try:
            self.COMMS.open()
        except IOError:
            self.COMMS.close()
            self.COMMS.open()
    
    def readConnection(self) -> str:
        self.result = self.COMMS.readline()
        return self.result
    
    

'''
ser = serial.Serial('COM6', 38400, timeout=0, parity=serial.PARITY_EVEN, rtscts = 1)

while True:
    s = ser.read(100)

    try:
        s = ord(s)
    except:
        s = 0
        
    print(s)
'''
