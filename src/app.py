from flask import Flask, render_template, jsonify
import socket
import psutil
import platform
import datetime
import os
from functools import wraps
import time
import json

app = Flask(__name__)

def get_system_metrics():
    cpu_times_percent = psutil.cpu_times_percent(interval=1)
    return {
        'cpu': {
            'total_usage': psutil.cpu_percent(interval=1),
            'per_cpu': psutil.cpu_percent(interval=1, percpu=True),
            'user': cpu_times_percent.user,
            'system': cpu_times_percent.system,
            'idle': cpu_times_percent.idle
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent,
            'used': psutil.virtual_memory().used
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent
        },
        'network': {
            'bytes_sent': psutil.net_io_counters().bytes_sent,
            'bytes_recv': psutil.net_io_counters().bytes_recv,
            'packets_sent': psutil.net_io_counters().packets_sent,
            'packets_recv': psutil.net_io_counters().packets_recv
        }
    }

def get_system_info():
    return {
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname()),
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
        'python_version': platform.python_version()
    }

@app.route('/')
def index():
    try:
        metrics = get_system_metrics()
        system_info = get_system_info()
        return render_template('dashboard.html',
                             metrics=metrics,
                             system_info=system_info,
                             timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/metrics')
def api_metrics():
    return jsonify(get_system_metrics())

@app.route('/api/sysinfo')
def api_sysinfo():
    return jsonify(get_system_info())

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
