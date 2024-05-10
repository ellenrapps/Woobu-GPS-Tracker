'''
Developed by Ellen Red

'''

import network
from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
import ujson
import gps_data


ssid = "" 
password = ""
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while ap.active == False:
    pass

print('Connection successful')
print(ap.ifconfig())


app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/')
async def index(request):
    return render_template('index.html')


@app.route('/update')
def update(request):
    values_gps = gps_data.la_lo_time_sat()
    new_latitude = values_gps[0]
    new_longitude = values_gps[1]
    new_gps_time = values_gps[2]
    new_satelites = values_gps[3]
    
    data = {
    "new_latitude" : new_latitude,
    "new_longitude" : new_longitude,
    "new_gps_time" : new_gps_time,
    "new_satelites" : new_satelites
    }
    response = ujson.dumps(data)
    return response
   

@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)
    

def start_server():
    print('Starting microdot app')
    try:
        app.run(port=80)
    except:
        app.shutdown()    

start_server()

