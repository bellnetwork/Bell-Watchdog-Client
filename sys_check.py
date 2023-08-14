from decimal import Decimal
from datetime import datetime
import json
import logging
import os
from sched import scheduler
import secrets
import subprocess
import datetime
import mariadb
import atexit
import time
import sys
import psutil
import requests
import schedule
import shutil

logging.basicConfig(level=logging.INFO)  # Set the root logger's level to INFO

logger = logging.getLogger(__name__)

# Uncomment this line to activate debug logging
logger.setLevel(logging.DEBUG)

result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)

# check if sysstat is installed
def check_sysstat():
    result = subprocess.run(["sar"], shell=True, capture_output=True, text=True)
    if result.stderr == '':
        logging.debug("sysstat is installed")
        return True
    else:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return False
    
# if sysstat is not installed, install it
def install_sysstat():
    result = subprocess.run(["sudo apt install sysstat -y"], shell=True, capture_output=True, text=True)
    if result.stderr == '':
        logging.debug("sysstat installed successfully")
        return True
    else:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return False

# Define a global variable to store the received server ID
received_server_id = None

def get_global_ip():
    global received_server_id  # Declare the global variable
    
    try:
        global_ip = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8')
        server_hostname = subprocess.check_output(['hostname', '-f']).decode('utf-8').strip()
        uptime = int(float(subprocess.check_output("awk '{print $1}' /proc/uptime", shell=True)))
        sys_os = subprocess.check_output("cat /etc/os-release | grep PRETTY_NAME | awk -F '=' '{print $2}' | sed 's/\"//g'", shell=True).decode('utf-8').strip()

        logging.debug(f"Global IP: {global_ip}")
        logging.debug(f"Hostname: {server_hostname}")
        logging.debug(f"Uptime: {uptime}")

        url = '/api/serv/78b32enxx82n/{}/check'.format(global_ip)
        data = {'hostname': server_hostname, 'sys_os': sys_os}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            logging.debug("Server information updated successfully")
            server_id = response.json().get('server_id')  # Store the received server ID
            received_server_id = server_id  # Store the received server ID in the global variable

            return server_id
        else:
            return None
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        time.sleep(5)
        return None

def check_for_update():
    version = 'v2.0.0'
    try:
        server_id = get_global_ip()
        update_url = f'/api/serv/78b32enxx82n/{server_id}/check_update'
        response = requests.get(update_url, params={'version': version})
        if response.status_code == 200:
            update_info = response.json()
            return update_info  # Returns a dictionary with 'available' and 'download_url'
        else:
            return None
    except Exception as e:
        error_message = f"Error checking for updates: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def download_update(download_url):
    try:
        response = requests.get(download_url)
        if response.status_code == 200:
            # Backup the old app.py file
            if os.path.exists('sys_check.py'):
                shutil.copy2('sys_check.py', 'sys_check.py.bak')

            # Save the new script content to a temporary file
            new_script_path = 'update_script.py'
            with open(new_script_path, 'wb') as new_script_file:
                new_script_file.write(response.content)

            # Replace the old app.py with the new received file
            if os.path.exists(new_script_path):
                os.rename(new_script_path, 'sys_check.py')
                os.remove('update_script.py')

            return True
        else:
            return False
    except Exception as e:
        error_message = f"Error downloading update: {str(e)}"
        global_error_message(random_token, error_message)
        return False


def restart_service():
    try:
        # Check if the script was started manually or as a service
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            # The script was started manually, restart the script itself
            print("Restarting the script...")
            python_executable = sys.executable
            script_path = os.path.abspath(__file__)
            subprocess.Popen([python_executable, script_path])
        else:
            # The script was started as a service, restart the service
            print("Restarting the service...")
            print("You can see the updated log on the web interface")
            subprocess.run(["sudo systemctl restart bellsyscheck.service"], shell=True)
    except Exception as e:
        error_message = f"Error restarting service: {str(e)}"
        global_error_message(random_token, error_message)

def record_start_time():
    server_id = get_global_ip()
    
    if server_id is None:
        error_message = f"Error: no server ID received"
        global_error_message(random_token, error_message)
        return
    
    start_time = subprocess.check_output("awk '{print $1}' /proc/uptime", shell=True).decode('utf-8').strip()
    url = '/api/serv/78b32enxx82nnx8347n9qx4/{}/record_start_time'.format(server_id)
    connect_starttime = requests.post(url, data={'start_time': start_time})
    
    if connect_starttime.status_code == 200:
        print("Successfully recorded start time.")
    else:
        error_message = "Error: failed to record start time"
        global_error_message(random_token, error_message)

# Function to record script stop time
def record_stop_time():
    server_id = get_global_ip()
    
    if server_id is None:
        error_message = "Error: no server ID received"
        global_error_message(random_token, error_message)
        return
    
    system_uptime = subprocess.check_output("awk '{print $1}' /proc/uptime", shell=True).decode('utf-8').strip()
    
    url = '/api/serv/78b32enxx82nnx8347n9qx4/{}/record_stop_time'.format(server_id)
    connect_stoptime = requests.post(url, json=system_uptime)
    if connect_stoptime.status_code == 200:
        print("Successfully recorded stop time.")
    else:
        global_error_message(random_token, error_message)
def system_uptime():
    try:
        uptime = int(float(subprocess.check_output("awk '{print $1}' /proc/uptime", shell=True)))
        return uptime
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def cpu_audit():
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
                    return cpu_percent
        error_message = "Error: failed to get CPU usage"
        global_error_message(random_token, error_message)
        return None
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def memory_audit():
    try:
        memory_percent = psutil.virtual_memory().percent
        logging.debug(f"Memory Usage: {memory_percent}")
        return memory_percent
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None


def cpu_usage():
    try:
        cpu_usage = [float(usage) for usage in subprocess.check_output("mpstat -P ALL 1 1 | awk '/Average:/ {print 100-$NF}'", shell=True).split()]
        logging.debug(f"CPU Usage: {cpu_usage}")
        if cpu_usage:
            average_cpu_usage = sum(cpu_usage) / len(cpu_usage)
            return average_cpu_usage
        else:
            return -1  # Return a default value if cpu_usage list is empty
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

# Function to send cpu usage to the server in real time
def send_cpu_usage():
    server_id = get_global_ip()
    if server_id is None:
        error_message = "Error: no server ID received"
        global_error_message(random_token, error_message)
        return
    cpu_usage_value = cpu_usage()
    url = '/api/serv/7x6b4eh3ecgriey7h/{}/cpu_usage'.format(server_id)
    payload = {'cpu_usage': cpu_usage_value}
    headers = {'Content-Type': 'application/json'}  # Set the Content-Type header
    connect_cpu_usage = requests.post(url, json=payload, headers=headers)
    if connect_cpu_usage.status_code == 200:
        print("Successfully sent cpu usage.")
    else:
        error_message = "Error: failed to send cpu usage"
        global_error_message(random_token, error_message)

def disk_usage():
    try:
        disk_usage_output = subprocess.check_output("df -P / | awk '/\\// {print $5}'", shell=True).decode('utf-8')
        disk_percent = disk_usage_output.strip()  # Remove leading/trailing whitespace
        disk_percent = disk_percent.rstrip('%')  # Remove trailing '%'
        disk_usage = float(disk_percent)
        logging.debug(f"Disk Usage: {disk_usage}")
        return disk_usage
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def network_usage():
    try:
        network_interfaces = psutil.net_io_counters(pernic=True)
        for interface, stats in network_interfaces.items():
            if stats.bytes_recv:
                network_usage_bytes = stats.bytes_recv
                logging.debug(f"Network Usage: {network_usage_bytes}")
                return network_usage_bytes

        print("No network usage data found.")
        return None
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def root_partition_usage():
    try:
        root_partition_output = subprocess.check_output("df -P / | awk '/\\// {print $5}'", shell=True).decode('utf-8')
        root_partition_percent = root_partition_output.strip()  # Remove leading/trailing whitespace
        root_partition_percent = root_partition_percent.rstrip('%')  # Remove trailing '%'
        root_partition_usage = float(root_partition_percent)
        logging.debug(f"Root Partition Usage: {root_partition_usage}")
        return root_partition_usage
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None


def max_partition_usage():
    try:
        max_partition_usage = subprocess.check_output("df -P | grep /dev/ | sort -k 5 -n -r | head -1 | awk '{print $5}'", shell=True)
        max_partition_usage = max_partition_usage.strip().decode('utf-8')  # Remove leading/trailing spaces and convert to string
        max_partition_usage = max_partition_usage.rstrip('%')  # Remove trailing '%'
        logging.debug(f"Max Partition Usage: {max_partition_usage}")
        return max_partition_usage
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None


def network_connections():
    try:
        network_connections = subprocess.check_output("ss -tuln | wc -l", shell=True)
        network_connections = network_connections.strip().decode('utf-8')  # Remove leading/trailing spaces and convert to string
        logging.debug(f"Network Connections: {network_connections}")
        return network_connections
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None


def memory_usage():
    try:
        memory_usage = float(subprocess.check_output("free -m | awk '/Mem:/ {print $3/$2 * 100.0}'", shell=True))
        memory_usage = round(memory_usage, 2)
        logging.debug(f"Memory Usage: {memory_usage}")
        return memory_usage
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None
    
def disk_io_monitoring():
    try:
        disk_io = psutil.disk_io_counters()
        read_bytes = disk_io.read_bytes
        write_bytes = disk_io.write_bytes
        logging.debug(f"Disk Read Bytes: {read_bytes}")
        logging.debug(f"Disk Write Bytes: {write_bytes}")
        return read_bytes, write_bytes
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def network_bandwidth_monitoring():
    try:
        network_io = psutil.net_io_counters()
        bytes_sent = network_io.bytes_sent
        bytes_recv = network_io.bytes_recv
        logging.debug(f"Network Bytes Sent: {bytes_sent}")
        logging.debug(f"Network Bytes Received: {bytes_recv}")
        return bytes_sent, bytes_recv
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def get_server_temperature():
    try:
        # psutil.sensors_temperatures() returns a dictionary of temperature data
        temperature_data = psutil.sensors_temperatures()
        
        # Check if the 'coretemp' key is present in the dictionary
        if 'coretemp' in temperature_data:
            core_temperatures = temperature_data['coretemp']
            
            # Assuming you want to get the average temperature of all cores
            total_temperature = sum(sensor.current for sensor in core_temperatures) / len(core_temperatures)
            logging.debug(f"Total temperature: {total_temperature}")
            return total_temperature
        
        logging.debug("No temperature data found.")
        return None
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def pid_monitoring():
    try:
        pid_list = []
        for process in psutil.process_iter():
            pid_list.append(process.pid)
        
        print("Running PIDs:")
        for pid in pid_list:
            logging.debug(f"PID: {pid}")
        
        return pid_list
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

# Disk Space Monitoring
def disk_space_monitoring(partition='/'):
    try:
        disk_usage_output = subprocess.check_output(f"df -P {partition} | awk '/\\// {{print $5}}'", shell=True).decode('utf-8')
        disk_percent = disk_usage_output.strip().rstrip('%')
        return float(disk_percent)
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

# Swap Space Monitoring
def swap_space_monitoring():
    try:
        swap = psutil.swap_memory()
        swap_percent = swap.percent
        return swap_percent
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

# Network Latency and Packet Loss
def network_latency_packet_loss(host='8.8.8.8', count=5):
    try:
        ping_output = subprocess.check_output(f"ping -c {count} {host}", shell=True).decode('utf-8')
        packet_loss = float(ping_output.split(", ")[2].split("%")[0])
        return packet_loss
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None


# Alerting Mechanisms (Assuming use of email for alerts)
def send_alert(subject, message):
    try:
        # Use your email sending mechanism here
        pass
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return None

def check_alert_conditions():
    disk_threshold = 90  # Example: Disk usage above 90%
    swap_threshold = 50  # Example: Swap usage above 50%
    packet_loss_threshold = 10  # Example: Packet loss above 10%

    disk_usage = disk_space_monitoring()
    swap_usage = swap_space_monitoring()
    packet_loss = network_latency_packet_loss()

    if disk_usage is not None and disk_usage > disk_threshold:
        send_alert("High Disk Usage", f"Disk usage is {disk_usage}%")

    if swap_usage is not None and swap_usage > swap_threshold:
        send_alert("High Swap Usage", f"Swap usage is {swap_usage}%")

    if packet_loss is not None and packet_loss > packet_loss_threshold:
        send_alert("High Packet Loss", f"Packet loss is {packet_loss}%")

# Service Status Monitoring
def check_service_status(service_name):
    try:
        status_output = subprocess.check_output(f"systemctl is-active {service_name}", shell=True).decode('utf-8').strip()
        return status_output == "active"
    except subprocess.CalledProcessError as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)
        return False
    
def check_server_status():
    try:
        server_id = get_global_ip()
        
        reboot_url = f'https://dhoz1tk2qru8ro6ntgx.bellsocket.com/api/serv/78b32enxx82nnx8347n9qx4/{server_id}/reboot_serv'
        shutdown_url = f'https://dhoz1tk2qru8ro6ntgx.bellsocket.com/api/serv/78b32enxx82ncguyvgjbtr7n9qxuny38/{server_id}/stop_serv'
        
        connect_status = requests.post(f'https://dhoz1tk2qru8ro6ntgx.bellsocket.com/api/serv/78b32enxx82nnx8347n9qx4/{server_id}/check_server_status')
        
        try:
            status_data = connect_status.json()
            server_status = status_data.get("status", "")
        except json.JSONDecodeError:
            error_message = "Error decoding JSON response. This means that our server is down."
            global_error_message(random_token, error_message)
            return
        
        print(f"Server status: {server_status}")
        
        if server_status == 'running':
            print("Status is running")
            logging.debug("Server is running")
        elif server_status == 'stopping':
            try:
                connect_stopping = requests.post(shutdown_url)
                if connect_stopping.text == 'stopping':
                    error_message = "Error: Server not stopping"
                    global_error_message(random_token, error_message)
                else:
                    logging.debug("Shutdown server...")
                    os.system("shutdown -h now")
            except Exception as e:
                logging.debug(f"Error: {e}")
                error_message = f"Error: {str(e)}"
                global_error_message(random_token, error_message)
        elif server_status == 'rebooting':
            try:
                connect_reboot = requests.post(reboot_url)
                if connect_reboot.text == 'rebooting':
                    logging.debug(f"Error: Server not rebooting {e}")
                    error_message = f"Error: {str(e)}"
                    global_error_message(random_token, error_message)
                else:
                    logging.debug("Restarting server...")
                    os.system("shutdown -r now")
            except Exception as e:
                error_message = f"Error: {str(e)}"
                global_error_message(random_token, error_message)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)


def global_error_message(random_token, error_message):
    # get server ip
    server_ip = get_global_ip()
    print("Please check your internet connection and try again. If the problem persists, please follow these steps:")
    print("1. Go to https://bellbots.eu and login with your account.")
    print("2. Go to the 'Service Status' page and check for the status. Also make sure that you have saved your IP address in the control panel.")
    print("3. If the status is 'Running', please wait for a few minutes and try again later or contact us.")
    print("4. If the status is 'Stopping', please wait for a few minutes and try again later.")
    print("5. Check for if a new update is available. You can check for updates in your control panel.")
    print("6. If the problem persists, please contact us. Please include also the token below and the error message.")
    print(f"Token: {random_token}")
    print("Error: " + error_message)
    try:
        error_url = f'/api/serv/78b32enxx82nnx8347n9qx4/{server_ip}/error'
        payload = {
            'errors': [
                {
                    'secret_token': random_token,
                    'error_message': error_message
                }
            ]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(error_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Error sent to WebSocket server")
        else:
            print("Failed to send error to WebSocket server. It seems that our service is down. Please wait for a few minutes and try again later.")
            print("Script will try again in 5 seconds...")
            time.sleep(5)
            get_global_ip()
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(f"Error sending error to WebSocket server: {e}. It seems that our service is down. Please wait for a few minutes and try again later.")
        print("Script will try again in 5 seconds...")
        time.sleep(5)
        get_global_ip()

random_token = secrets.token_hex(16)
error_message = ""
global_error_message(random_token, error_message) 
        
def save_system_status():
    server_id = get_global_ip()

    if server_id is None:
        error_message = "Error: Server ID not found"
        global_error_message(random_token, error_message)
        
        return

    status_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status_uptime = format_uptime(system_uptime())
    status_cpu = cpu_audit()
    status_memory = memory_audit()
    status_disk = disk_usage()
    status_root_partition = root_partition_usage()
    status_max_partition = max_partition_usage()
    status_network = network_usage()
    status_network_connections = network_connections()
    status_cpu_usage = cpu_usage()
    status_memory_usage = memory_usage()
    server_temperature = get_server_temperature()
    disk_percent = disk_usage()
    swap_percent = swap_space_monitoring()
    packet_loss = network_latency_packet_loss()

    # Convert network usage from bytes to megabytes
    network_usage_bytes = network_usage()
    network_usage_megabytes = network_usage_bytes / (1024 * 1024)

    if server_temperature is None:
        server_temperature = float('0.0')  # Set default value to 0.0 if no data is available

    pid_list = [
    {
        'pid_id': pid,
        'process_name': psutil.Process(pid).name(),
        'start_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu_usage': psutil.Process(pid).cpu_percent()
    }
    for pid in pid_monitoring()
]

    try:
        data = {
            'get_status_time': status_time,
            'format_uptime': status_uptime,
            'cpu_audit': status_cpu,
            'memory_audit': status_memory,
            'disk_usage': status_disk,
            'root_partition_usage': status_root_partition,
            'max_partition_usage': status_max_partition,
            'network_usage': status_network,
            'network_connections': status_network_connections,
            'cpu_usage': status_cpu_usage,
            'memory_usage': status_memory_usage,
            'get_server_temperature': server_temperature,
            'disk_usage': disk_percent,
            'swap_space_monitoring': swap_percent,
            'network_latency_packet_loss': packet_loss,
            'network_usage_send': network_usage_bytes,
            'network_usage_recv': network_usage_megabytes,
            'disk_read_bytes': status_disk,
            'disk_write_bytes': status_disk,
            'pid_monitoring': pid_list,  # Include pid monitoring data
        }
        print(f"Found pid data: {pid_list}")

        connect_status = requests.post(
            f'https://dhoz1tk2qru8ro6ntgx.bellsocket.com/api/serv/78b32enxx82n/{server_id}/system_status',
            json=data
        )

        if connect_status.status_code == 200:
            print("Data sent successfully")
        else:
            error_message = "Error: Failed to send data to WebSocket server"
            global_error_message(random_token, error_message)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        global_error_message(random_token, error_message)

    logging.debug(f"Network usage (megabytes): {network_usage_megabytes}")

def format_uptime(uptime_seconds):
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"


# Register the function to be called when the script exits
atexit.register(record_stop_time)

# Record script start time
record_start_time()

try:
    while True:
        update_info = check_for_update()
        if update_info and update_info.get('available'):
            download_url = update_info.get('download_url')
            if download_update(download_url):
                restart_service()
                
        # Call the functions to collect data
        uptime = system_uptime()
        memory_percent = memory_audit()
        cpu_percent = cpu_audit()
        cpu_usage_percent = cpu_usage()
        disk_percent = disk_usage()
        network_bytes = network_usage()
        root_partition_percent = root_partition_usage()
        max_partition_percent = max_partition_usage()
        status_network = network_usage()
        network_connections_count = network_connections()
        memory_usage_percent = memory_usage()
        read_bytes, write_bytes = disk_io_monitoring()
        sent_bytes, recv_bytes = network_bandwidth_monitoring()
        server_temperature = get_server_temperature()
        server_status = check_server_status()
        disk_percent = disk_usage()
        swap_percent = swap_space_monitoring()
        packet_loss = network_latency_packet_loss()
        cpu_usage_live = send_cpu_usage()
        
        # Save the collected data
        save_system_status()


        time.sleep(30)  # Sleep for 30 seconds
except KeyboardInterrupt:
    pass


record_stop_time()
