# Bell-Watchdog-Client

## Introduction
- Bell Watchdog is a part of the Bell System Monitoring tool, designed to monitor and report various system metrics in real-time. This document focuses on the client-side application, which collects and sends metrics to a central server via WebSocket.

## Prerequisites
- For a more specific guide tailored to Linux distributions where the Bell Watchdog can be effectively used and noting the requirement of root privileges for setup and installation, please see the modified section below:

## System Requirements
- **Operating System:** The client script is compatible with Debian, Ubuntu, CentOS, and other Linux-based operating systems.
- **Python Version:** Python 3.6 or later.
- **Network Access:** Ensure access to the internet or a local network where the WebSocket server is hosted.

<details>

<summary>Manual Installation</summary>

## Installation
- This installation guide assumes you are operating as the root user. If you're not logged in as root, you can switch to the root user by executing su and entering the root password, or you can prefix commands with sudo where applicable.

## System Utilities
- The script relies on certain utilities to gather system metrics. Install the sysstat package to enable the collection of CPU, memory, I/O, and other important system statistics.

## On Debian/Ubuntu systems, use the following command:
````
apt-get update && apt-get install sysstat
````

## For CentOS/RHEL systems, execute:

````
yum install sysstat
````

## Python Environment Setup
- It's recommended to use a virtual environment for Python projects to manage dependencies effectively.

## Install virtualenv if you haven't already:
````
apt-get install python3-virtualenv
````

## Create a virtual environment in your project directory:
````
virtualenv venv
````

## Activate the virtual environment:
````
source venv/bin/activate
````

## Install Python Packages
- With the virtual environment activated, install the necessary Python packages using pip:
pip install socketio-client asyncio psutil watchdog

## On Debian 12:
````
pip install socketio-client asyncio psutil watchdog --break-system-packages
````

## Configuration
- Before running the Bell Watchdog, ensure you have configured the WebSocket server's URL in your project. This typically involves setting a variable or a configuration file within the project to specify the WebSocket server address.

## Running the Client
- To start the client application and begin monitoring, run the following command from your project directory:

````
cd /path/to/your/project && python3 -m app debug
````

Replace directory with the name of your main Python project location if it's different.

For the client version setup and management as a systemd service, follow these guidelines. This guide will help you to set up the Bell Watchdog as a service that can start automatically at boot and can be controlled manually through systemd commands. This setup requires root or sudo privileges on your Linux system.

Creating a Systemd Service File for the Watchdog
Locate the Example Service File:
An example service file is provided at /install/service/bell_watchdog.service. Review this file for an understanding of how the service is configured.

## Create Your Service File:
Copy the example service file to the /etc/systemd/system/ directory and name it according to your preference, for instance, bell_watchdog.service.
````
cp /path/to/your/project/install/service/bell_watchdog.service /etc/systemd/system/bell_watchdog.service
````

## Edit the Service File:
You might need to edit the service file to match your project's specific paths and settings. Use your preferred text editor to open the file:
````
nano /etc/systemd/system/bell_watchdog.service
````
````
vi /etc/systemd/system/bell_watchdog.service
````

Make necessary adjustments to paths and user/group settings as per your setup.

## Setting up as Root
Given the nature of system monitoring, running the script with root privileges ensures comprehensive access to system metrics. This guide is written with the assumption that operations are performed as root. If you're using a non-root account, ensure you have sufficient permissions by being a part of the sudoers group or by acquiring necessary permissions through other means.

## Managing the Watchdog Service
**Start the service:**
````
systemctl start bell_watchdog
````

**Stop the service:**
````
systemctl stop bell_watchdog
````

**Restart the service:** 
- This is useful after making changes to the service configuration or your client application.
````
systemctl restart bell_watchdog
````

**Enable auto-start at boot:**
````
systemctl enable bell_watchdog
````

**Disable auto-start at boot:**
````
systemctl disable bell_watchdog
````

**Check service status:**
````
systemctl status bell_watchdog
````

## Viewing Logs
- To view the logs for your Watchdog, use:
````
journalctl -u bell_watchdog.service
````

This command displays the log messages generated by your client application. Use the -f flag with journalctl to follow the log output in real-time.

## Note
This README serves as a guide for deploying the Bell Watchdog as a systemd service. Depending on your specific project requirements, including dependencies, environment setup, and execution paths, you may need to adjust the service file and systemd commands accordingly. Ensure the client script is set up to run properly as the main entry point for your monitoring tasks.
</details>

<details>

<summary>Automatic Installation</summary>

</details>
