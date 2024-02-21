import psutil
from utils.sys.sys_messages.logging import setup_custom_logging

async def disk_io_monitoring(sio):
    try:
        disk_io = psutil.disk_io_counters()
        read_bytes = disk_io.read_bytes
        write_bytes = disk_io.write_bytes
        setup_custom_logging('info', 'Disk Read Bytes', f' {read_bytes}')
        setup_custom_logging('info', 'Disk Read Bytes', f' {write_bytes}')
        await sio.emit('live_disk_io_monitoring_check', {'read_bytes': read_bytes, 'write_bytes': write_bytes})
    except Exception as e:
        setup_custom_logging('error', 'Disk IO Monitoring', f' There was an error: {e}')