from prometheus_client import start_http_server, Summary, Gauge
import time
import datetime
import sys
import serial

'''
Inspired by:
* https://github.com/sanderjo/P1/blob/master/P1-parser.awk
* https://github.com/prometheus/client_python
* https://github.com/gejanssen/slimmemeter-rpi

filter_list = {'1-0:1.8.1':'p1_total_electricity_used_rate_1',
            '1-0:1.8.2':'p1_total_electricity_used_rate_2',
            '1-0:2.8.1':'p1_total_electricity_provided_rate_1',
            '1-0:2.8.2':'p1_total_electricity_provided_rate_2',
            '1-0:1.7.0':'p1_total_electricity_used',
            '1-0:2.7.0':'p1_total_electricity_provided',
            '0-1:24.2.1(191204215508W)':'p1_total_gas_used'}
'''

# Define metrics
p1_total_electricity_used_rate_1 = Gauge('p1_total_electricity_used_rate_1', 'Gebruik elektra dal')
p1_total_electricity_used_rate_2 = Gauge('p1_total_electricity_used_rate_2', 'Gebruik elektra piek')
p1_total_electricity_provided_rate_1 = Gauge('p1_total_electricity_provided_rate_1', 'Geleverd elektra dal')
p1_total_electricity_provided_rate_2 = Gauge('p1_total_electricity_provided_rate_2', 'Geleverd elektra piek')
p1_total_electricity_used = Gauge('p1_total_electricity_used', 'Totaal gebruik elektra')
p1_total_electricity_provided = Gauge('p1_total_electricity_provided', 'Totaal geleverd elektra')
p1_total_gas_used = Gauge('p1_total_gas_used', 'Totaal gebruik gas')

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

# Interval in seconds
interval = 30


def get_p1_metrics():
    ser_open()

    p1_counter=0
    while p1_counter < 26:
        p1_counter = p1_counter +1
        p1_line=''
        try:
            p1_raw = ser.readline()
        except:
            sys.exit ("Seriele port %s cannot be read. Exiting." % ser.name )

        # Generate a clean string per line
        p1_line=str(p1_raw, "utf-8").strip()

        if '1-0:1.8.1' in p1_line:
            print("p1_total_electricity_used_rate_1: {}" .format(markup_helper(p1_line)))
            p1_total_electricity_used_rate_1.set(markup_helper(p1_line))
        elif '1-0:1.8.2' in p1_line:
            print("p1_total_electricity_used_rate_2: {}" .format(markup_helper(p1_line)))
            p1_total_electricity_used_rate_2.set(markup_helper(p1_line))
        elif '1-0:2.8.1' in p1_line:
            print("p1_total_electricity_provided_rate_1: {}" .format(markup_helper(p1_line)))
            p1_total_electricity_provided_rate_1.set(markup_helper(p1_line))
        elif '1-0:1.7.0' in p1_line:
            print("p1_total_electricity_used: {}" .format(markup_helper(p1_line)))
            p1_total_electricity_used.set(markup_helper(p1_line))
        elif '1-0:2.7.0' in p1_line:
            print("p1_total_electricity_provided: {}" .format(markup_helper(p1_line)))
            p1_total_electricity_provided.set(markup_helper(p1_line))
        elif '0-1:24.2.1' in p1_line:
            print("p1_total_gas_used: {}" .format(markup_helper(p1_line)))
            p1_total_gas_used.set(markup_helper(p1_line))
    ser.close()



def ser_open():
    # Open COM port
    try:
        ser.open()
    except:
        sys.exit ("Error opening %s."  % ser.name)      

def ser_close():
    #Close port and show status
    try:
        ser.close()
    except:
        sys.exit ("Oops %s. Programme aborted." % ser.name )      

def markup_helper(str_line):
    '''
    Read raw string and return only the value
    '''
    return float(str_line.split('(')[-1].split('*')[0])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        get_p1_metrics()
        print("[{}] Got new metrics from device." .format(datetime.datetime.now()))
        time.sleep(interval)
