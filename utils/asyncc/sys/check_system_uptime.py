import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def system_uptime(sio):
    try:
        server_uptime = int(float(subprocess.check_output("awk '{print $1}' /proc/uptime", shell=True)))
        setup_custom_logging('info', 'Server Uptime', f' {server_uptime}')
        await sio.emit('live_system_uptime_check', {'server_uptime': server_uptime})
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Server Uptime', f' There was an error: {e}')     