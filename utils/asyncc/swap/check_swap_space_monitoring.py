import psutil
from utils.sys.sys_messages.logging import setup_custom_logging

async def swap_space_monitoring(sio):
    try:
        swap = psutil.swap_memory()
        swap_percent = swap.percent
        setup_custom_logging('info', 'Swap Space', f' {swap_percent}')
        await sio.emit('live_swap_space_monitoring_check', {'swap_percent': swap_percent})
    except Exception as e:
        setup_custom_logging('error', 'Swap Space', f' There was an error: {e}')