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

mcp.Setup(default['CE'],default['SPEED'])
wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(default['LED1'],1)

@app.get("/status")
def index():
    data, _ = mcp.ReadData(default['CE'],default['CH'],default['VREF'])
    print(data)
    return {"status": data > default['TH']}

@app.post("/toggle")
def toggle(data: bool_data):
    wiringpi.digitalWrite(default['LED1'],data.status)
    

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

