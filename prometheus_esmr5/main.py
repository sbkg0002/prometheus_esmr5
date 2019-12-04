from prometheus_client import start_http_server, Summary, Gauge
import time
import sys
import serial

'''
Inspired by:
* https://github.com/sanderjo/P1/blob/master/P1-parser.awk
* https://github.com/prometheus/client_python
* https://github.com/gejanssen/slimmemeter-rpi
'''

# Metric configuration
INTERVAL = 10
# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
g = Gauge('my_inprogress_requests', 'Description of gauge')

# Serial configuration
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

# Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s."  % ser.name)      

def get_p1_statistics():
    # Initialize
    p1_counter=0
    p1_state = {}

    # Only iterate over the following data types
    filter_list = {'1-0:1.8.1':'p1_total_electricity_used_rate_1',
                '1-0:1.8.2':'p1_total_electricity_used_rate_2',
                '1-0:2.8.1':'p1_total_electricity_provided_rate_1',
                '1-0:2.8.2':'p1_total_electricity_provided_rate_2',
                '1-0:1.7.0':'p1_total_electricity_used',
                '1-0:2.7.0':'p1_total_electricity_provided',
                '0-1:24.2.1(191204215508W)':'p1_total_gas_used'}

    while p1_counter < 26:
        p1_line=''
        try:
            p1_raw = ser.readline()
        except:
            sys.exit ("Seriele port %s cannot be read. Exiting." % ser.name )    

        # Generate a clean string per line
        p1_str=str(p1_raw, "utf-8").strip()

        # Only lines starting with 0 or 1
        if p1_str[0:1] in ['0','1']:
            # Split the lines on '('
            p1_list = p1_str.split('(')

            # Only use the types in filter_list
            if p1_list[0] in filter_list:
                # Add key:value for metric_name:value
                # Get the friendly name from the filter list and cut off the '*kWh'
                p1_state[filter_list.get(p1_list[0])] = p1_list[1].split('*')[0]

        # if p1_str[0:9] == '0-1:24.2.1':
            # print("YES")

        p1_counter = p1_counter +1

    #Close port and show status
    try:
        ser.close()
    except:
        sys.exit ("Oops %s. Programma afgebroken." % ser.name )      

    return(p1_state)
'''
/1-0:1.8.1/ { print "Electra: Totaal verbruik tarief 1 (nacht) KWh: " getfloat($0) }
/1-0:1.8.2/ { print "Electra: Totaal verbruik tarief 2 (dag) KWh: "   getfloat($0) }
/1-0:2.8.1/ { print "Electra: Totaal geleverd tarief 1 (nacht) KWh: " getfloat($0) }
/1-0:2.8.2/ { print "Electra: Totaal geleverd tarief 2 (dag) KWh: "   getfloat($0) }

/1-0:1.7.0/ { print "Electra: Huidig verbruik [W]: "             1000*getfloat($0) }
/1-0:2.7.0/ { print "Electra: Huidige teruglevering [W]: "       1000*getfloat($0) }

/^\(/       { print "Gas: Totaal verbruik gas in m3: "                getfloat($0) }
'''
    



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
