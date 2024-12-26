import subprocess
from metrics_handler import *

def read_ht2000_data():
    """
    Retrieves the current metric value from the ht2000 device.

    Return:
        ('1396394602, 02-04-2014 06:23:22, 30.100000, 50.000000, 1542.000000', '')
        with the current timestamp, temperature, humidity, and co2 (PPM).
        (That 2014 years is set in the device)
    """
    command = """./ht2000 /dev/$(sudo dmesg  | grep -i 'SLAB HT2000' | grep -o 'hidraw[0-9]\\+' | head -1)"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        if 'No such file or directory' in result.stderr.strip():
            print("Cannot find ht2000 device.")
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        print("Command Error:")
        print(str(e))
        return None, None
    
if __name__ == "__main__":
    # print(generate_metrics(read_ht2000_data()))
    
    server_address = ("", 8008) 
    httpd = HTTPServer(server_address, MetricsHandler)
    print(f"Serving metrics on http://localhost:8008/metrics")
    httpd.serve_forever()
