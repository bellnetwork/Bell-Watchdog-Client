import logging, psutil
import datetime

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

                logging.error(f"PID: {process.info['pid']}, Name: {process.info['name']}, Uptime: {uptime_str}")
                await sio.emit('live_pid_monitoring_check', pid_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Handle processes that might have terminated or are not accessible
                continue
    except Exception as e:
        logging.error(f'got error in pid_monitoring: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)