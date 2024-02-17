import logging, psutil

async def disk_io_monitoring(sio):
    try:
        disk_io = psutil.disk_io_counters()
        read_bytes = disk_io.read_bytes
        write_bytes = disk_io.write_bytes
        logging.error(f"Disk Read Bytes: {read_bytes}")
        logging.error(f"Disk Write Bytes: {write_bytes}")
        await sio.emit('live_disk_io_monitoring_check', {'read_bytes': read_bytes, 'write_bytes': write_bytes})
    except Exception as e:
        logging.error(f'got error in disk_io_monitoring: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)