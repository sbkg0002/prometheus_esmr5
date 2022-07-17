import logging
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from smeterd.meter import SmartMeter

'''
Inspired by:
* https://github.com/sanderjo/P1/blob/master/P1-parser.awk
* https://github.com/prometheus/client_python
* https://github.com/gejanssen/slimmemeter-rpi
* http://domoticx.com/p1-poort-slimme-meter-hardware/

'1-0:1.8.1':'p1_total_electricity_used_rate_1',
'1-0:1.8.2':'p1_total_electricity_used_rate_2',
'1-0:2.8.1':'p1_total_electricity_provided_rate_1',
'1-0:2.8.2':'p1_total_electricity_provided_rate_2',
'1-0:1.7.0':'p1_total_electricity_used',
'1-0:2.7.0':'p1_total_electricity_provided',
'1-0:32.7.0':'p1_l1_voltage',
'1-0:52.7.0':'p1_l2_voltage',
'1-0:72.7.0':'p1_l3_voltage',
'0-0:96.14.0':'p1_current_tarrif' ( 2 is high)
'''


def markup_helper(str_line):
    '''
    Read raw string and return only the value
    '''
    return int(str_line.split('(')[-1].split('*')[0].replace('.', ''))


def markup_helper_float(str_line):
    '''
    Read raw string and return only the value
    '''
    return float(str_line.split('(')[-1].split('*')[0])


def markup_helper_tarrif(str_line):
    '''
    Read raw string and return only the value
    '''
    return int(str_line.split('(')[-1].replace(')', '').replace('0', ''))


class CustomCollector(object):
    def get_p1_metrics(self, p1_lines, metrics):
        # Convert to a list for simple parsing
        p1_list = str(p1_lines).splitlines()

        for p1_line in p1_list:
            # logging.info(p1_line)
            if '1-0:1.8.1' in p1_line:
                logging.info("p1_total_electricity_used_rate_1: {}".format(markup_helper(p1_line)))
                metrics['p1_total_electricity_used_rate_1'].add_metric(["Rozensingel"], markup_helper(p1_line))
            elif '1-0:1.8.2' in p1_line:
                logging.info("p1_total_electricity_used_rate_2: {}".format(markup_helper(p1_line)))
                metrics['p1_total_electricity_used_rate_2'].add_metric(["Rozensingel"], markup_helper(p1_line))
            elif '1-0:2.8.1' in p1_line:
                logging.info("p1_total_electricity_provided_rate_1: {}".format(markup_helper(p1_line)))
                metrics['p1_total_electricity_provided_rate_1'].add_metric(["Rozensingel"], markup_helper(p1_line))
            elif '1-0:2.8.2' in p1_line:
                logging.info("p1_total_electricity_provided_rate_2: {}".format(markup_helper(p1_line)))
                metrics['p1_total_electricity_provided_rate_2'].add_metric(["Rozensingel"], markup_helper(p1_line))
            elif '1-0:1.7.0' in p1_line:
                logging.info("p1_total_electricity_used: {}".format(markup_helper(p1_line)))
                metrics['p1_total_electricity_used'].add_metric(["Rozensingel"], markup_helper(p1_line))
            elif '1-0:2.7.0' in p1_line:
                logging.info("p1_total_electricity_provided: {}".format(markup_helper(p1_line)))
                metrics['p1_total_electricity_provided'].add_metric(["Rozensingel"], markup_helper(p1_line))
            elif '1-0:32.7.0' in p1_line:
                logging.info("p1_l1_voltage: {}".format(markup_helper_float(p1_line)))
                metrics['p1_l1_voltage'].add_metric(["Rozensingel"], markup_helper_float(p1_line))
            elif '1-0:52.7.0' in p1_line:
                logging.info("p1_l2_voltage: {}".format(markup_helper_float(p1_line)))
                metrics['p1_l2_voltage'].add_metric(["Rozensingel"], markup_helper_float(p1_line))
            elif '1-0:72.7.0' in p1_line:
                logging.info("p1_l3_voltage: {}".format(markup_helper_float(p1_line)))
                metrics['p1_l3_voltage'].add_metric(["Rozensingel"], markup_helper_float(p1_line))
            elif '0-0:96.14.0' in p1_line:
                logging.info("p1_current_tarrif: {}".format(markup_helper_tarrif(p1_line)))
                metrics['p1_current_tarrif'].add_metric(["Rozensingel"], markup_helper_tarrif(p1_line))

        return metrics

    def collect(self):
        metrics = {
            'p1_total_electricity_used_rate_1': GaugeMetricFamily('p1_total_electricity_used_rate_1', 'Gebruik elektra dal'),
            'p1_total_electricity_used_rate_2': GaugeMetricFamily('p1_total_electricity_used_rate_2', 'Gebruik elektra piek'),
            'p1_total_electricity_provided_rate_1': GaugeMetricFamily('p1_total_electricity_provided_rate_1', 'Geleverd elektra dal'),
            'p1_total_electricity_provided_rate_2': GaugeMetricFamily('p1_total_electricity_provided_rate_2', 'Geleverd elektra piek'),
            'p1_total_electricity_used': GaugeMetricFamily('p1_total_electricity_used', 'Totaal gebruik elektra'),
            'p1_total_electricity_provided': GaugeMetricFamily('p1_total_electricity_provided', 'Totaal geleverd elektra'),
            'p1_l1_voltage': GaugeMetricFamily('p1_l1_voltage', 'Totaal geleverd elektra'),
            'p1_l2_voltage': GaugeMetricFamily('p1_l2_voltage', 'Totaal geleverd elektra'),
            'p1_l3_voltage': GaugeMetricFamily('p1_l3_voltage', 'Totaal geleverd elektra'),
            'p1_current_tarrif': GaugeMetricFamily('p1_current_tarrif', 'Totaal geleverd elektra')
        }

        meter = SmartMeter('/dev/ttyUSB0', baudrate=115200)
        metrics = self.get_p1_metrics(meter.read_one_packet(), metrics)
        meter.disconnect()

        for metric in metrics.values():
            yield metric


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("Starting ESMR5 metrics exporter")

    REGISTRY.register(CustomCollector())
    start_http_server(8000)

    while True:
        time.sleep(60)
