import requests
import json

def main():
    URL = 'http://127.0.0.1:8000/'
    res = requests.get(URL)
    print(res.json())
    
if __name__ == '__main__':
    main()
    