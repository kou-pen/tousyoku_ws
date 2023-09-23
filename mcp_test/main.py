import mcp3208 as mcp
import time

CE = 0
SPEED = 10000020 # Hz
VREF = 3.3 # V
CH = 0

mcp.Setup(CE,SPEED)

while True:
    data, volt = mcp.ReadData(CE,CH,VREF)
    print("%d, %d"%(data,volt))
    time.sleep(0.01)
    


