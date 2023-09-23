import mcp3208 as mcp
import wiringpi

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

class bool_data(BaseModel):
    status: bool
    
class th_data(BaseModel):
    th: int

CE = 0
SPEED = 1000000 # Hz
VREF = 3.3 # V
CH = 0
TH = 1000

LED1 = 19


app = FastAPI()

mcp.Setup(CE,SPEED)
wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(LED1,1)

@app.post("/status")
def index(data: th_data):
    data, _ = mcp.ReadData(CE,CH,VREF)
    print(data)
    return {"status": data > int(data.th)}

@app.post("/toggle")
def toggle(data: bool_data):
    wiringpi.digitalWrite(LED1,data.status)
    

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

