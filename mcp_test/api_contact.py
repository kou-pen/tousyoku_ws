import requests
import json

def main():
    GET_URL = 'http://192.168.0.10:8000/status'
    POST_URL = 'http://192.168.0.10:8000/toggle'
    res = requests.get(GET_URL)
    get_json_data = res.json()
    now_status = get_json_data["status"]    
    print(now_status)
    data = {
        'status': not now_status
    }
    
    requests.post(POST_URL, json.dumps(data))
    
if __name__ == '__main__':
    main()
    