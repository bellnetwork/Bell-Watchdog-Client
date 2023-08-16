# Bell Linux Monitoring Script

The Bell macOS Monitoring script is a Python-based monitoring tool designed to collect and report various system metrics from macOS-based servers. It provides functionalities for monitoring system performance, tracking resource usage, checking for updates, and sending alerts. The script is intended to be run as a background service and can be customized to suit specific monitoring needs.

## Overview

The script utilizes various Python libraries and system commands to gather information about the system's performance, resource utilization, network activity, and more. It communicates with a remote server to report the collected data, allowing users to monitor their macOS server's health and status remotely.

## Features

- **System Information:** Collects and reports essential system information, including the global IP address, hostname, uptime, and operating system version.

- **Update Check:** Periodically checks for updates and downloads and installs them if available, ensuring that the monitoring tool is up-to-date.

- **Resource Monitoring:** Monitors CPU usage, memory usage, disk usage, network bandwidth, and other system resources.

- **Temperature Monitoring:** Gathers temperature data from system sensors, providing insights into the server's thermal state.

- **Process Monitoring:** Tracks running processes and their CPU usage, allowing users to monitor the performance of individual processes.

- **Alerting Mechanisms:** Can be configured to send alerts based on predefined thresholds for disk usage, swap usage, and network latency.

- **Service Status Monitoring:** Checks the status of a specific service and can trigger server reboot or shutdown actions based on the server's status.

## Usage

**Dependencies:** The script relies on various Python libraries, including psutil, requests, and others. Make sure these dependencies are installed.

**Configuration:** Configure the script by modifying the settings at the beginning of the script. Customize alert thresholds, URLs, and other parameters to match your requirements.

**Execution:** Run the script as a background service. It will continuously gather data and send it to a remote server for monitoring.

**Alerts:** Configure alerting mechanisms by setting threshold values for resource usage. The script will send alerts if resource usage exceeds the specified thresholds.

## Disclaimer

This script is provided as a starting point for creating a monitoring tool and may require additional adjustments to work seamlessly with your system and network environment. It's important to review and test the script in a controlled environment before deploying it to production systems.

**Important Note:** This script is intended to be used exclusively with a booked service on the bellbots.eu platform. The provided IP address is crucial for verification, and unauthorized use is strictly prohibited. Ensure that you have a legitimate booking on bellbots.eu and have entered the correct IP address for verification. Unauthorized use may result in account suspension or legal action.

## Installation and Usage Guide

### Prerequisites

    macOS-based server
    Python 3.x installed
    Internet connectivity

### Installation Steps

1. Clone the Repository:

        git clone gh repo clone bellnetwork/bellsys_moni_macos
        cd bellsys_moni_macos

### Install Dependencies:

For Debian/Ubuntu:

    apt install python3 python3-pip

For Centos:

    yum install python3 python3-pip

    pip3 install psutil requests


### Run the Script:
 
    python3 sys_check.py &

### Usage Guide

Monitoring Data: The script will continuously monitor various metrics, such as CPU usage, memory usage, network activity, and more.

Alerts: If configured, the script will send alerts when predefined thresholds are exceeded.

Update Check: The script will periodically check for updates and install them if available. This ensures the monitoring tool is up-to-date.

Remote Monitoring: The collected data is sent to a remote server for monitoring. Configure the URLs in the script to match your remote server's endpoints.

### Stopping the Script
To stop the script, find its process ID (PID) and use the kill command.

### Setup launchctl
Edit and move the .plist file. Ensure the correct path is entered.

    vi com.bellsyscheck.plist
    mv com.bellsyscheck.plist /Library/LaunchDaemons/com.bellsyscheck.plist

Load and start the service:

    sudo launchctl load /Library/LaunchDaemons/com.bellsyscheck.plist
    sudo launchctl start com.bellsyscheck

Verify the Service:

    sudo launchctl list | grep com.bellsyscheck

## Logs and Unloading
Logs are written to /var/log/bellsyscheck.log and /var/log/bellsyscheck_error.log.
To stop and unload the service:

    sudo launchctl stop com.bellsyscheck
    sudo launchctl unload /Library/LaunchDaemons/com.bellsyscheck.plist

### Customization and Advanced Usage
The script's core functionality is tightly integrated with the bellbots.eu platform. Unauthorized modifications may cause malfunctions. While you can't modify the core code, you can suggest new features through bellbots.eu support.

For customization, adjust intervals for data collection, alerts, and updates. Always ensure changes align with intended usage and bellbots.eu service context. Your feedback is valuable for ongoing improvements.

Thank you for understanding and adhering to usage guidelines. For questions or suggestions, reach out via bellbots.eu support channels.
