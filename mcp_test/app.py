import mcp3208 as mcp
import wiringpi

import time

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

class bool_data(BaseModel):
    status: bool

CE = 0
SPEED = 10000020 # Hz
VREF = 3.3 # V
CH = 0
TH = 6000

LED1 = 19


app = FastAPI()

mcp.Setup(CE,SPEED)
wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(LED1,1)

@app.get("/status")
def index():
    data, _ = mcp.ReadData(CE,CH,VREF)
    print(data)
    return {"status": data > TH}

@app.post("/toggle")
def toggle(data: bool_data):
    wiringpi.digitalWrite(LED1,data.status)
    

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

