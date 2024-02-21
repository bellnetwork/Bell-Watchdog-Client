import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def root_partition_usage(sio):
    try:
        root_partition_output = subprocess.check_output("df -P / | awk '/\\// {print $5}'", shell=True).decode('utf-8')
        root_partition_percent = root_partition_output.strip()  # Remove leading/trailing whitespace
        root_partition_percent = root_partition_percent.rstrip('%')  # Remove trailing '%'
        root_partition_usage = float(root_partition_percent)
        setup_custom_logging('info', 'Root Partition Usage', f' {root_partition_usage}')
        await sio.emit('live_root_partition_usage_check', root_partition_usage)
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Root Partition Usage', f' There was an error: {e}')