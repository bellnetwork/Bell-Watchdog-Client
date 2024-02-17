import logging, subprocess

async def disk_usage(sio):
    try:
        disk_usage_output = subprocess.check_output("df -P / | awk '/\\// {print $5}'", shell=True).decode('utf-8')
        disk_percent = disk_usage_output.strip()  # Remove leading/trailing whitespace
        disk_percent = disk_percent.rstrip('%')  # Remove trailing '%'
        disk_usage = float(disk_percent)
        logging.error(f"Disk Usage: {disk_usage}")
        await sio.emit('live_disk_usage_check', disk_usage)
    except subprocess.CalledProcessError as e:
        logging.error(f"got error in disk_usage: {disk_usage}")
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)
