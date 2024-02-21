import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def cpu_usage(sio):
    try:
        cpu_usage = [float(usage) for usage in subprocess.check_output("mpstat -P ALL 1 1 | awk '/Average:/ {print 100-$NF}'", shell=True).split()]
        setup_custom_logging('info', 'CPU Usage', f' {cpu_usage}')
        if cpu_usage:
            average_cpu_usage = sum(cpu_usage) / len(cpu_usage)
            await sio.emit('live_cpu_usage_check', average_cpu_usage)
        else:
            await sio.emit('live_cpu_usage_check', -1)  # Return a default value if cpu_usage list is empty
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'CPU Usage', f' There was an error: {e}')