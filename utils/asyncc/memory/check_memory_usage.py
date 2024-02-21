import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def memory_usage(sio):
    try:
        memory_usage = float(subprocess.check_output("free -m | awk '/Mem:/ {print $3/$2 * 100.0}'", shell=True))
        memory_usage = round(memory_usage, 2)
        setup_custom_logging('info', 'Memory Usage', f' {memory_usage}')
        await sio.emit('live_memory_usage_check', memory_usage)
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Memory Usage', f' There was an error: {e}')