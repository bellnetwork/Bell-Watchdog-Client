# bellsysmoni

**Server Monitoring Script Setup Guide**
This guide will walk you through setting up and using the server monitoring script. The script collects various system metrics and sends them to a WebSocket server for analysis. Please follow the steps below to get started.

**Prerequisites**
Before you begin, ensure you have the following prerequisites:

Python 3 installed on your system

The pip package manager

Plugin psutil installed

Plugin requests installed

Internet connectivity

Valid Package on bellbots.eu

New server created on the bellbots.eu portal


**Step 1: Obtain Your API Token**

Log in to your BellBots customer portal at https://bellbots.eu.

Enter your server information and save it to use this script.


**Step 2: Install Required Dependencies**

Open a terminal and run the following commands to install the required dependencies:

# Install Dependencies

For Debian/Ubuntu:

    apt install python3 python3-pip

For Centos:

    yum install python3 python3-pip

    pip3 install psutil requests

**Step 3: Configure the Script**

Download the provided script (sys_check.py) to a directory on your server.

    git clone https://github.com/bellnetwork/bellsysmoni.git

**Step 4: Moving the Service File**

Download the provided service file (sys_check.service) to your server.

Open the service file in a text editor to make necessary changes before moving it.

Make sure to modify the ExecStart and WorkingDirectory lines according to your file structure:

ExecStart: Update the path to the sys_check.py script. The example uses /your/file/location/sys_check.py, but you should replace it with the actual path to your script.

WorkingDirectory: Set this to the directory where the sys_check.py script is located (/your/file/location/services in the example).

Save the changes to the service file.

Now, move the modified service file to the system directory for systemd service files. Run:

Open the script in a text editor.

Make sure to modify the ExecStart and WorkingDirectory lines according to your file structure:

ExecStart: Update the path to the sys_check.py script. The example uses /your/file/location/services/sys_check.py, but you should replace it with the actual path to your script.

WorkingDirectory: Set this to the directory where the sys_check.py script is located (/your/file/location/services in the example).

Save the changes to the service file.

Now, move the modified service file to the system directory for systemd service files.

sudo mv path_to_downloaded_service_file /your/file/location/sys_check.service

**Step 5: Enable and Start the Service**

Enable the service to start on boot:

    systemctl enable sys_check.service

Start the service:

    service sys_check start
    
or:

    systemctl start sys_check

Stop the service:

    service sys_check stop
    
or:

    systemctl start sys_check

Restart the service:

    service sys_check restart
    
or:

    systemctl restart sys_check
    
Step 6: Manual Script Execution

To manually execute the script for debugging purposes, open a terminal and navigate to the directory where the script is located. Run the following command:

    python3 sys_check.py

This will run the script interactively in your terminal, allowing you to observe its behavior and check for any errors.

**Generating a Secret Key for Support (Optional)**

If you encounter any errors or need assistance with the setup, you can generate a secret key that will allow our support team to help you efficiently. Follow these steps:

In the terminal, navigate to the directory where the sys_check.py script is located. For example:

    cd /your/file/location
    python3 sys_check.py

or:

    python3 /your/file/location/sys_check.py

Run the following command to generate a secret key:

    python3 -c "import secrets; print(secrets.token_hex(16))"

A secret key will be generated and displayed in the terminal. Copy this key and keep it secure.

If you need to reach out to our support team, provide them with the secret key. This key will allow them to better understand your setup and assist you more effectively.

Remember, generating and sharing this secret key is optional, but it can greatly aid our support team in helping you troubleshoot any issues you encounter.

**Customization and Advanced Usage**

Please note that the script's core functionality is tightly integrated with the bellbots.eu platform, and unauthorized modifications may cause the script to malfunction or behave unpredictably. We strongly discourage any modifications to the script's existing codebase.

If you have ideas for new features or improvements, we encourage you to share your suggestions with us. You can create a new support ticket on bellbots.eu to propose new features or discuss potential enhancements. Our team will review your suggestions and consider them for future updates to the script.

While you are not allowed to directly modify the script's core code, you can still enhance its capabilities by suggesting new monitoring functions, alert mechanisms, or additional system metrics. Your feedback is valuable to us and can contribute to the ongoing improvement of the Bell macOS Monitoring script.

As for customizing the script's behavior, you can adjust the intervals at which data is collected, alerts are checked, and updates are performed. However, please exercise caution and ensure that any changes align with the intended functionality and usage of the script within the context of the bellbots.eu service.

Thank you for your understanding and cooperation in adhering to the script's usage guidelines. If you have any questions or suggestions, please don't hesitate to reach out to us through the support channels provided on bellbots.eu.
