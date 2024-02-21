import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def network_connections(sio):
    try:
        network_connections = subprocess.check_output("ss -tuln | wc -l", shell=True)
        network_connections = network_connections.strip().decode('utf-8')  # Remove leading/trailing spaces and convert to string
        setup_custom_logging('info', 'Network Connections', f' {network_connections}')
        await sio.emit('live_network_connections_check', {'network_connections': network_connections})
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Network Connections', f' There was an error: {e}')