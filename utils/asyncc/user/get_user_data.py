import subprocess
from utils.sys.sys_messages.logging import setup_custom_logging

async def get_user_name(ip_address):
    try:
        output = subprocess.check_output(["who"], universal_newlines=True)
        lines = output.strip().split("\n")
        for line in lines:
            if ip_address in line:
                return line.split()[0]
    except Exception as e:
        setup_custom_logging('error', 'Get User Data', f' There was an error: {e}')  
    return "Unknown"