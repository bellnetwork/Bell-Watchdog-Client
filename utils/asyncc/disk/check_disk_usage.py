import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def disk_usage(sio):
    try:
        disk_usage_output = subprocess.check_output("df -P / | awk '/\\// {print $5}'", shell=True).decode('utf-8')
        disk_percent = disk_usage_output.strip()  # Remove leading/trailing whitespace
        disk_percent = disk_percent.rstrip('%')  # Remove trailing '%'
        disk_usage = float(disk_percent)
        setup_custom_logging('info', 'Disk Usage', f' {disk_usage}')
        await sio.emit('live_disk_usage_check', disk_usage)
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Disk Usage', f' There was an error: {e}')
