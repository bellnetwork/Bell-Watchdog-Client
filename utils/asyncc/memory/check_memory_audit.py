import psutil
from utils.sys.sys_messages.logging import setup_custom_logging

async def memory_audit(sio):
    try:
        memory_percent = psutil.virtual_memory().percent
        setup_custom_logging('info', 'Memory Autid', f' {memory_percent}')
        await sio.emit('live_memory_audit_check', memory_percent)
    except Exception as e:
        setup_custom_logging('error', 'Memory Audit', f' There was an error: {e}')