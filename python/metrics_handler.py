from http.server import BaseHTTPRequestHandler, HTTPServer
from run import read_ht2000_data

def generate_metrics(data_tuple):
    if data_tuple[0]:
        fields = data_tuple[0].split(',')
        temperature = fields[2].strip()
        rh_data = fields[3].strip()
        co2 = fields[4].strip()

        metrics = f"""
# This device's sensor is only run once for 4 secdonds, so don't scrape too fast
        
# HELP temperature Measured temperature in Celsius
# TYPE temperature gauge
temperature {temperature}
# HELP rh_data Relative humidity data as a percentage
# TYPE rh_data gauge
rh_data {rh_data}
# HELP co2 Carbon dioxide concentration in ppm
# TYPE co2 gauge
co2 {co2}
"""
        return metrics
    return "# No data available"

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            metrics = generate_metrics(read_ht2000_data())
            self.wfile.write(metrics.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

