import requests
import time
# URL do servidor ESP8266
url = "http://192.168.4.1"
def send_command(command):
    try:
        r = requests.get(url+command)
        if r.status_code == 200:
            print("Command sent successfully")
        else:
            print("Failed to send command")
    except:
        print("Failed to connect to server")




send_command("/?command=/backward")
time.sleep(2)
send_command("/?command=/forward")


 




