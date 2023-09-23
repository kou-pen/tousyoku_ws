import mcp3208 as mcp
import wiringpi

import configparser

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

class bool_data(BaseModel):
    status: bool

config = configparser.ConfigParser()
config.read('config.ini')
default = config['RPI']

app = FastAPI()

mcp.Setup(int(default['CE']),int(default['SPEED']))
wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(int(default['LED1']),1)

@app.get("/status")
def index():
    data, _ = mcp.ReadData(int(default['CE']),int(default['CH']),int(default['VREF']))
    print(data)
    return {"status": data > int(default['TH'])}

@app.post("/toggle")
def toggle(data: bool_data):
    wiringpi.digitalWrite(int(default['LED1']),data.status)
    

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

