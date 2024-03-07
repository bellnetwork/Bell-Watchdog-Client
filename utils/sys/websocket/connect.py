# Create connection py

import asyncio, socketio

from utils.imports import function_handler_imports as ehi
from utils.sys.sys_messages.logging import setup_custom_logging

async def main(sio):
    ehi.accept_connect(sio)
    ehi.accept_disconnect(sio)
    await ehi.create_connection(sio)
    try:
        while True:
            #await ehi.check_attempts_logs(sio)
            await ehi.cpu_audit(sio)
            await ehi.cpu_usage(sio)
            await ehi.disk_io_monitoring(sio)
            await ehi.disk_usage(sio)
            await ehi.max_partition_usage(sio)
            await ehi.root_partition_usage(sio)
            await ehi.memory_audit(sio)
            await ehi.memory_usage(sio)
            #await ehi.check_network_status(sio)
            await ehi.network_bandwidth_monitoring(sio)
            await ehi.network_connections(sio)
            await ehi.network_latency_packet_loss(sio)
            await ehi.network_usage(sio)
            await ehi.swap_space_monitoring(sio)
            #await ehi.check_server_status(sio)
            await ehi.get_server_temperature(sio)   
            await ehi.system_uptime(sio)
            #await ehi.pid_monitoring(sio)     
            await asyncio.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        setup_custom_logging('error', 'Connection Status', ' Disconnecting due to keyboard interrupt.')  
        await sio.disconnect()
