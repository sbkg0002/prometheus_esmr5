from prometheus_client import start_http_server, Gauge
import time
import datetime
import sys
import serial
from smeterd.meter import SmartMeter

'''
Inspired by:
* https://github.com/sanderjo/P1/blob/master/P1-parser.awk
* https://github.com/prometheus/client_python
* https://github.com/gejanssen/slimmemeter-rpi

'1-0:1.8.1':'p1_total_electricity_used_rate_1',
'1-0:1.8.2':'p1_total_electricity_used_rate_2',
'1-0:2.8.1':'p1_total_electricity_provided_rate_1',
'1-0:2.8.2':'p1_total_electricity_provided_rate_2',
'1-0:1.7.0':'p1_total_electricity_used',
'1-0:2.7.0':'p1_total_electricity_provided',
'0-1:24.2.1(191204215508W)':'p1_total_gas_used'
'''

# Define metrics
p1_total_electricity_used_rate_1 = Gauge('p1_total_electricity_used_rate_1', 'Gebruik elektra dal')
p1_total_electricity_used_rate_2 = Gauge('p1_total_electricity_used_rate_2', 'Gebruik elektra piek')
p1_total_electricity_provided_rate_1 = Gauge('p1_total_electricity_provided_rate_1', 'Geleverd elektra dal')
p1_total_electricity_provided_rate_2 = Gauge('p1_total_electricity_provided_rate_2', 'Geleverd elektra piek')
p1_total_electricity_used = Gauge('p1_total_electricity_used', 'Totaal gebruik elektra')
p1_total_electricity_provided = Gauge('p1_total_electricity_provided', 'Totaal geleverd elektra')
p1_total_gas_used = Gauge('p1_total_gas_used', 'Totaal gebruik gas')

# Interval in seconds
interval = 15

def get_p1_metrics(p1_lines):
    # Convert to a list for simple parsing
    p1_list = str(p1_lines).splitlines()

    for p1_line in p1_list:
        # Parse per line
        if '1-0:1.8.1' in p1_line:
            print("[{}] p1_total_electricity_used_rate_1: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_electricity_used_rate_1.set(markup_helper(p1_line))
        elif '1-0:1.8.2' in p1_line:
            print("[{}] p1_total_electricity_used_rate_2: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_electricity_used_rate_2.set(markup_helper(p1_line))
        elif '1-0:2.8.1' in p1_line:
            print("[{}] p1_total_electricity_provided_rate_1: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_electricity_provided_rate_1.set(markup_helper(p1_line))
        elif '1-0:2.8.2' in p1_line:
            print("[{}] p1_total_electricity_provided_rate_2: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_electricity_provided_rate_2.set(markup_helper(p1_line))
        elif '1-0:1.7.0' in p1_line:
            print("[{}] p1_total_electricity_used: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_electricity_used.set(markup_helper(p1_line))
        elif '1-0:2.7.0' in p1_line:
            print("[{}] p1_total_electricity_provided: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_electricity_provided.set(markup_helper(p1_line))
        elif '0-1:24.2.1' in p1_line:
            print("[{}] p1_total_gas_used: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
            p1_total_gas_used.set(markup_helper(p1_line))

def markup_helper(str_line):
    '''
    Read raw string and return only the value
    '''
    return int(str_line.split('(')[-1].split('*')[0].replace('.',''))


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        try:
            # Define device
            meter = SmartMeter('/dev/ttyUSB0', baudrate=115200)
            get_p1_metrics(meter.read_one_packet())
            meter.disconnect()
        except:
            sys.exit ("Serial port cannot be read. Will try again.")
        print("")
        time.sleep(interval)
