#!/usr/bin/env python3

import platform
import psutil
import time
import os
from flask import Flask, jsonify, request, abort
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SECRET_TOKEN = os.getenv("SECRET_TOKEN", "default-token")
PORT = int(os.getenv("PORT", 8080))

def get_system_info():
    info = {
        "host_info_is_available": True,
        "boot_time": int(psutil.boot_time()),
        "hostname": platform.node(),
        "platform": platform.system(),
        "cpu": {
            "load_is_available": True,
            "load1_percent": int(psutil.getloadavg()[0] * 100),
            "load15_percent": int(psutil.getloadavg()[2] * 100),
            "temperature_is_available": True,
            "temperature_c": get_cpu_temperature()
        },
        "memory": {
            "memory_is_available": True,
            "total_mb": psutil.virtual_memory().total // (1024 * 1024),
            "used_mb": psutil.virtual_memory().used // (1024 * 1024),
            "used_percent": int(psutil.virtual_memory().percent),
            "swap_is_available": True,
            "swap_total_mb": psutil.swap_memory().total // (1024 * 1024),
            "swap_used_mb": psutil.swap_memory().used // (1024 * 1024),
            "swap_used_percent": int(psutil.swap_memory().percent)
        },
        "mountpoints": [
            {
                "path": partition.mountpoint,
                "name": partition.mountpoint,
                "total_mb": psutil.disk_usage(partition.mountpoint).total // (1024 * 1024),
                "used_mb": psutil.disk_usage(partition.mountpoint).used // (1024 * 1024),
                "used_percent": int(psutil.disk_usage(partition.mountpoint).percent)
            }
            for partition in psutil.disk_partitions()
            if not partition.mountpoint.startswith(("/snap", "/boot/efi"))
        ]
    }
    return info

def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000.0
        return int(temp)
    except FileNotFoundError:
        return 0

@app.route('/api/sysinfo/all', methods=['GET'])
def sysinfo():
    token = request.headers.get('Authorization')
    if token != f"Bearer {SECRET_TOKEN}":
        abort(401, description="Unauthorized: Invalid token")

    info = get_system_info()
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)