import mcp3208 as mcp
import time
from fastapi import FastAPI
import uvicorn

CE = 0
SPEED = 10000020 # Hz
VREF = 3.3 # V
CH = 0

app = FastAPI()

mcp.Setup(CE,SPEED)

@app.get("/status")
def index():
    data, volt = mcp.ReadData(CE,CH,VREF)
    return {"status": data > 1000}

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)

