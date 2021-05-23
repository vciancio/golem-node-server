from flask import Flask
from golem import GolemStatus
from flask_cors import CORS
import hardware
import sys

app = Flask(__name__)

CORS(app, resources=r'/api/*')

def hardware_stats():
    status = GolemStatus()
    return {
        "cpu": hardware.cpu(),
        "memory": hardware.memory(),
        "isProcessingTask": hardware.isProcessingTask(),
        "shared": {
            "cpu_threads": status.cpu_threads(),
            "mem_gib": status.mem_gib(),
            "storage_gib": status.storage_gib(),
        }
    }

def current_time():
    # return : current time in millis
    import calendar
    import time
    return calendar.timegm(time.gmtime())

def golem():
    status = GolemStatus()
    return {
        "name": status.node_name(),
        "id": status.id(),
        "version": status.version(),
        "wallet": status.account(),
        "network": status.network(),
        "subnet": status.subnet(),
        "processedTotal": status.processed_total(),
        "processedLastHour": status.processed_hour(),
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
