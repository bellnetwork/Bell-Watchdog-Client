# Utils Network Status Check

import socket, asyncio, subprocess

from utils.asyncc.services.service_names import get_service_name
from utils.asyncc.user.get_user_data import get_user_name
from utils.sys.sys_messages.logging import setup_custom_logging

server_name = subprocess.check_output("hostname", shell=True).decode().strip()
# Define the services you are interested in
SERVICES = ["HTTP", "SSH/SFTP", "Console-Getty", "Cron", "DBus", "Getty", "MariaDB", "Networkd-Dispatcher", "RPC Bind", "RSyslog", "Systemd-Journald", "Systemd-Logind", "Systemd-Udevd", "User", "Xinetd"]

connections = set()
connected_users = {}  # type: Dict[str, str]

async def check_network_status(sio):
    global connections, connected_users

    # Get the server IP
    server_ip = socket.gethostbyname(server_name)
    server_ip_printed = False

    # Get the list of network connections
    output = subprocess.check_output(["ss", "-tun"], universal_newlines=True)
    lines = output.strip().split("\n")[1:]

    # Extract the service name from each line and send a message if an unknown service is detected
    for line in lines:
        fields = line.strip().split()
        if len(fields) >= 5:
            access_details = fields[-1]
            if access_details.startswith("(") and access_details.endswith(")"):
                access_details = access_details[1:-1]
            user_ip = fields[4].split(":")[0]
            service_name = get_service_name(access_details)

            if service_name not in SERVICES and fields[4] not in connections:
                connections.add(fields[4])

                # Print user IP instead of server IP
                if not server_ip_printed:
                    server_ip_printed = True

                # Check if user is logged in
                username = await get_user_name(user_ip)
                if username != 'Unknown':
                    # User is logged in
                    data_one = f'User {username} ({user_ip}) reconnected to {service_name}'
                    setup_custom_logging('info', 'User Reconnected', data_one)
                    sio.emit('network_status_update', data_one)
                else:
                    # New user connected
                    connected_users[user_ip] = None
                    data_two = f'New user ({user_ip}) connected to {service_name}'
                    setup_custom_logging('error', 'New Connection', data_two)
                    sio.emit('network_status_update', data_two)

                # Check if user is trying to access via SSH and whether the attempt failed or succeeded
                if 'sshd' in access_details:
                    if 'Failed password' in access_details:
                        username = access_details.split()[-3]
                        data_three = f'Failed SSH login attempt by user {username} ({user_ip})'
                        setup_custom_logging('error', 'Connection Attempt', data_three)
                        sio.emit('network_status_update', data_three)
                    elif 'Accepted' in access_details:
                        username = access_details.split()[-1]
                        data_four = f'Successful SSH login by user {username} ({user_ip})'
                        setup_custom_logging('error', 'New Connection', data_four)
                        sio.emit('network_status_update', data_four)