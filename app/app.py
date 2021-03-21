from flask import Flask
from golem import GolemStatus, get_status
from flask_cors import CORS
import hardware
import sys

app = Flask(__name__)

CORS(app, resources=r'/api/*')

def hardware_stats():
    return {
        "cpu": hardware.cpu(),
        "memory": hardware.memory(),
    }

def current_time():
    # return : current time in millis
    import calendar
    import time
    return calendar.timegm(time.gmtime())

def golem():
    o = get_status()
    # print(o, file=sys.stderr)
    if o is None:
        return None
    status = GolemStatus(o)
    return {
        "name": status.node_name(),
        "version": status.version(),
        "wallet": status.wallet(),
        "network": status.network(),
        "subnet": status.subnet(),
        "processedTotal": status.processed_total(),
        "processedLastHour": status.processed_hour(),
        "processingLastHour": status.processing_hour(),
    }

@app.route('/api/status', methods=['GET'])
def stats_all():
    return {
        "timestamp" : current_time(),
        "hardware" : hardware_stats(),
        "info": golem(),
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0')
