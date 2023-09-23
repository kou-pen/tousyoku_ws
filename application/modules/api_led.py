import requests
import json

class ApiLed():
    def __init__(self,th,GET,POST,TOKEN=None):
        self.GET_URL = GET
        self.POST_URL = POST
        self.TOKEN = TOKEN
        self.th = th
        
    
    def get_now_status(self,th):
        data = {
            'th': th
        }
        res = requests.post(self.GET_URL,json.dumps(data))
        json_data = res.json()
        return json_data["status"]
    
    def post_led_status(self,status):
        data = {
            'status': not status
        }
        requests.post(self.POST_URL,json.dumps(data))
        
    def line_notify(self,msg=None):
        headers = {
            'Authorization': 'Bearer '+self.TOKEN,
        }
        files = {
            'message': (None,msg)
        }
        requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files)
        
    def toggle_led(self):
        self.post_led_status(self.get_now_status(self.th))

def main():
    GET_URL = 'http://192.168.0.10:8000/status'
    POST_URL = 'http://192.168.0.10:8000/toggle'
    LINE_TOKEN = 'Yi1UAVve4DbuaADyUld2W1cGuwMEBqLRqoRoDjD075q'
    use_api = ApiLed(GET_URL,POST_URL,LINE_TOKEN)
    use_api.line_notify()
    # use_api.toggle_led()

    
if __name__ == '__main__':
    main()
    
