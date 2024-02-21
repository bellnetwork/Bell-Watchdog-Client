import psutil
from utils.sys.sys_messages.logging import setup_custom_logging

async def network_usage(sio):
    try:
        network_interfaces = psutil.net_io_counters(pernic=True)
        for interface, stats in network_interfaces.items():
            if stats.bytes_recv:
                network_usage_bytes = stats.bytes_recv
                # Convert network usage from bytes to megabytes
                network_usage_megabytes = network_usage_bytes / (1024 * 1024)
                setup_custom_logging('info', 'Network Usaget', f' {network_usage_bytes}')
                await sio.emit('live_network_usage_check', {'network_usage_megabytes': network_usage_megabytes})
    except Exception as e:
        setup_custom_logging('error', 'Network Usage', f' There was an error: {e}')