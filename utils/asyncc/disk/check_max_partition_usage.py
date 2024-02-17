import logging, subprocess

async def max_partition_usage(sio):
    try:
        max_partition_usage = subprocess.check_output("df -P | grep /dev/ | sort -k 5 -n -r | head -1 | awk '{print $5}'", shell=True)
        max_partition_usage = max_partition_usage.strip().decode('utf-8')  # Remove leading/trailing spaces and convert to string
        max_partition_usage = max_partition_usage.rstrip('%')  # Remove trailing '%'
        logging.error(f"Max Partition Usage: {max_partition_usage}")
        await sio.emit('live_max_partition_usage_check', {'max_partition_usage': max_partition_usage})
    except subprocess.CalledProcessError as e:
        logging.error(f'got error in max_partition_usage: {max_partition_usage}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)