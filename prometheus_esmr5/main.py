from prometheus_client import start_http_server, Summary, Gauge
import time
import sys
import serial

INTERVAL = 10
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
g = Gauge('my_inprogress_requests', 'Description of gauge')

# Serial configuration
#Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"


#Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Aaaaarch."  % ser.name)      

p1_teller=0

while p1_teller < 26:
    p1_line=''
    # Read 1 line van de seriele poort
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )      
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()
    #  als je alles wil zien moet je de volgende line uncommenten
    print (p1_line)
    p1_teller = p1_teller +1

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    g.inc()      # Increment by 1
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(INTERVAL)
