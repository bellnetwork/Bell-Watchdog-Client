import logging, psutil

async def network_usage(sio):
    try:
        network_interfaces = psutil.net_io_counters(pernic=True)
        for interface, stats in network_interfaces.items():
            if stats.bytes_recv:
                network_usage_bytes = stats.bytes_recv
                # Convert network usage from bytes to megabytes
                network_usage_megabytes = network_usage_bytes / (1024 * 1024)
                logging.error(f"Network Usage: {network_usage_bytes}")
                await sio.emit('live_network_usage_check', {'network_usage_megabytes': network_usage_megabytes})
    except Exception as e:
        logging.error(f'got error in network_usage: {network_usage}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)        