import logging, psutil

async def memory_audit(sio):
    try:
        memory_percent = psutil.virtual_memory().percent
        logging.error(f"Memory Usage: {memory_percent}")
        await sio.emit('live_memory_audit_check', memory_percent)
    except Exception as e:
        logging.error(f'got error in memory_audit: {memory_audit}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)
        