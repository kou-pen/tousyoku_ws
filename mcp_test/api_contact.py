import requests
import json

def main():
    URL = 'http://192.168.0.10:8000/status'
    res = requests.get(URL)
    print(res.json())
    
if __name__ == '__main__':
    main()
    