from utils.sys.sys_messages.logging import setup_custom_logging

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
                    setup_custom_logging('info', 'CPU Audit', f' {cpu_percent}')
                    await sio.emit('live_cpu_audit_check', cpu_percent)
    except Exception as e:
        setup_custom_logging('error', 'CPU Audit', f' There was an error: {e}')