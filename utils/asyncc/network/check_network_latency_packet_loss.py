import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def network_latency_packet_loss(sio, host='8.8.8.8', count=5):
    try:
        ping_output = subprocess.check_output(f"ping -c {count} {host}", shell=True).decode('utf-8')
        packet_loss = float(ping_output.split(", ")[2].split("%")[0])
        setup_custom_logging('info', 'Network Latency Lost', f' {packet_loss}')
        await sio.emit('live_network_latency_packet_loss_check', {'packet_loss': packet_loss})
    except subprocess.CalledProcessError as e:
        setup_custom_logging('error', 'Network Latency Lost', f' There was an error: {e}')