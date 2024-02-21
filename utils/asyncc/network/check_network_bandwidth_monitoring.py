import psutil
from utils.sys.sys_messages.logging import setup_custom_logging

async def network_bandwidth_monitoring(sio):
    try:
        network_io = psutil.net_io_counters()
        bytes_sent = network_io.bytes_sent
        bytes_recv = network_io.bytes_recv
        setup_custom_logging('info', 'Network Bytes Sent', f' {bytes_sent}')
        setup_custom_logging('info', 'Network Bytes Received', f' {bytes_recv}')
        await sio.emit('live_network_bandwidth_monitoring_check', {'bytes_sent': bytes_sent, 'bytes_recv': bytes_recv})
    except Exception as e:
        setup_custom_logging('error', 'Network Bandwidth Monitor', f' There was an error: {e}')