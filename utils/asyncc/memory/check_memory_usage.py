import logging, subprocess

async def memory_usage(sio):
    try:
        memory_usage = float(subprocess.check_output("free -m | awk '/Mem:/ {print $3/$2 * 100.0}'", shell=True))
        memory_usage = round(memory_usage, 2)
        logging.error(f"Memory Usage: {memory_usage}")
        await sio.emit('live_memory_usage_check', memory_usage)
    except subprocess.CalledProcessError as e:
        logging.error(f'got error in memory_usage: {memory_usage}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)