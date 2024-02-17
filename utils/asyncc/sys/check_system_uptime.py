import logging, subprocess

async def system_uptime(sio):
    try:
        server_uptime = int(float(subprocess.check_output("awk '{print $1}' /proc/uptime", shell=True)))
        await sio.emit('live_system_uptime_check', {'server_uptime': server_uptime})
    except subprocess.CalledProcessError as e:
        logging.error(f'got error in system_uptime: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)        