import logging

async def cpu_audit(sio):
    try:
        with open('/proc/stat') as stat_file:
            lines = stat_file.readlines()
            for line in lines:
                if line.startswith('cpu '):
                    fields = line.split()
                    idle_ticks = float(fields[4])
                    total_ticks = sum(float(x) for x in fields[1:])
                    cpu_percent = (1.0 - idle_ticks / total_ticks) * 100.0
                    logging.debug(f"CPU Usage: {cpu_percent}")
                    await sio.emit('live_cpu_audit_check', cpu_percent)
                    
        #error_message = "Error: failed to get CPU usage"
        #global_error_message(random_token, error_message)
        #sio.emit('live_cpu_audit_check_error', '0')
    except Exception as e:
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)
        #sio.emit('live_cpu_audit_check_error', '0') 
        logging.error(f'got error in cpu_audit: {e}')