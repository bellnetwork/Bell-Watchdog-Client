import os, subprocess

from utils.asyncc.services.service_names import get_service_name
from utils.sys.sys_messages.logging import setup_custom_logging

server_name = subprocess.check_output("hostname", shell=True).decode().strip()
async def check_attempts_logs(sio):
    """Checks the system logs for hacking attempts and successful SSH logins."""
    log_file = '/var/log/auth.log' # Update the path to the system log file
    cmd = f"grep 'authentication failure' {log_file}"
    output = os.popen(cmd).read()
    if output:
        data_one = f'Hacking attempt detected on {server_name}:\n{output}'
        setup_custom_logging('info', 'Attempt Logs', data_one)
        await sio.emit('check_attempts_logs', data_one)
    
    cmd = f"grep 'sshd.*Accepted' {log_file}" # Search for successful SSH logins
    output = os.popen(cmd).read()
    if output:
        for line in output.split('\n'):
            if line:
                words = line.split()
                user = words[8] # Extract the username from the log entry
                ip = words[10].split(':')[0] # Extract the IP address from the log entry
                data_two = f'Successful SSH login by user {user} ({ip})'
                setup_custom_logging('info', 'Attempt Logs', data_two)
                await sio.emit('check_attempts_logs', data_two)
