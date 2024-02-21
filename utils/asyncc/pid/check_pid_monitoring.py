# PID Monitoring.py

import psutil
import datetime
from utils.sys.sys_messages.logging import setup_custom_logging

async def pid_monitoring(sio):
    try:
        pid_info_list = []
        for process in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                # Calculate process uptime from its creation time
                uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(process.info['create_time'])
                uptime_str = str(uptime).split('.')[0]  # Convert uptime to string and remove microseconds

                pid_info = {
                    'pid': process.info['pid'],
                    'name': process.info['name'],
                    'uptime': uptime_str
                }
                pid_info_list.append(pid_info)
                
                setup_custom_logging('info', 'PID Status', ' PID: | Name: | Uptime:')
                setup_custom_logging('info', 'PID Status', f" {process.info['pid']} | {process.info['name']} | {uptime_str}")
                await sio.emit('live_pid_monitoring_check', pid_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Handle processes that might have terminated or are not accessible
                continue
    except Exception as e:
        setup_custom_logging('error', 'PID Status', f' There was an error: {e}')
