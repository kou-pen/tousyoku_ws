import requests
import json

class api_led():
    def __init__(self,GET,POST):
        self.GET_URL = GET
        self.POST_URL = POST
    
    def get_now_status(self):
        res = requests.get(self.GET_URL)
        json_data = res.json()
        return json_data["status"]
    
    def post_led_status(self,status):
        data = {
            'status': not status
        }
        requests.post(self.POST_URL,json.dumps(data))
        
    def toggle_led(self):
        self.post_led_status(self.get_now_status)

def main():
    GET_URL = 'http://192.168.0.10:8000/status'
    POST_URL = 'http://192.168.0.10:8000/toggle'
    use_api = api_led(GET_URL,POST_URL)
    use_api.toggle_led()

    
if __name__ == '__main__':
    main()
    
