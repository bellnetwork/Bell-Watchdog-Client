import logging, subprocess

async def network_latency_packet_loss(sio, host='8.8.8.8', count=5):
    try:
        ping_output = subprocess.check_output(f"ping -c {count} {host}", shell=True).decode('utf-8')
        packet_loss = float(ping_output.split(", ")[2].split("%")[0])
        await sio.emit('live_network_latency_packet_loss_check', {'packet_loss': packet_loss})
    except subprocess.CalledProcessError as e:
        logging.error(f'got error in network_latency_packet_loss: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)