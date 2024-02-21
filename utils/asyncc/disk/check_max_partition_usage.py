import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def max_partition_usage(sio):
    try:
        max_partition_usage = subprocess.check_output("df -P | grep /dev/ | sort -k 5 -n -r | head -1 | awk '{print $5}'", shell=True)
        max_partition_usage = max_partition_usage.strip().decode('utf-8')  # Remove leading/trailing spaces and convert to string
        max_partition_usage = max_partition_usage.rstrip('%')  # Remove trailing '%'
        setup_custom_logging('info', 'Max Partition Usage', f' {max_partition_usage}')
        await sio.emit('live_max_partition_usage_check', {'max_partition_usage': max_partition_usage})
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Max Partition Usage', f' There was an error: {e}')