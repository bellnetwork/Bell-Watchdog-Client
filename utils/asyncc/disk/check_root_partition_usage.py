import logging, subprocess

async def root_partition_usage(sio):
    try:
        root_partition_output = subprocess.check_output("df -P / | awk '/\\// {print $5}'", shell=True).decode('utf-8')
        root_partition_percent = root_partition_output.strip()  # Remove leading/trailing whitespace
        root_partition_percent = root_partition_percent.rstrip('%')  # Remove trailing '%'
        root_partition_usage = float(root_partition_percent)
        logging.error(f"Root Partition Usage: {root_partition_usage}")
        await sio.emit('live_root_partition_usage_check', root_partition_usage)
    except subprocess.CalledProcessError as e:
        logging.error(f'got error in root_partition_usage: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)
        #await sio.emit('live_root_partition_usage_check', 0)