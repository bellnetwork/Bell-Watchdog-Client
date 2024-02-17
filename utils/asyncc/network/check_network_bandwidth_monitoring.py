import logging, psutil

async def network_bandwidth_monitoring(sio):
    try:
        network_io = psutil.net_io_counters()
        bytes_sent = network_io.bytes_sent
        bytes_recv = network_io.bytes_recv
        logging.debug(f"Network Bytes Sent: {bytes_sent}")
        logging.debug(f"Network Bytes Received: {bytes_recv}")
        await sio.emit('live_network_bandwidth_monitoring_check', {'bytes_sent': bytes_sent, 'bytes_recv': bytes_recv})
    except Exception as e:
        logging.error(f'got error in network_bandwidth_monitoring: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)