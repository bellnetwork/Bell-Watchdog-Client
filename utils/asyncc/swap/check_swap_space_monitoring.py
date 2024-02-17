import logging, psutil

async def swap_space_monitoring(sio):
    try:
        swap = psutil.swap_memory()
        swap_percent = swap.percent
        await sio.emit('live_swap_space_monitoring_check', {'swap_percent': swap_percent})
    except Exception as e:
        logging.error(f'got error in swap_space_monitoring: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)