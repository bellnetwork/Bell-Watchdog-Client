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


Step 1: Obtain Your API Token

Log in to your BellBots customer portal at https://bellbots.eu.

Navigate to your account settings or API settings to find your unique API token.

Copy the API token, as you'll need it for script configuration.

Step 2: Install Required Dependencies

Open a terminal and run the following commands to install the required dependencies:

# Install Dependencies

For Debian/Ubuntu:

apt install python3 python3-pip

For Centos:

yum install python3 python3-pip

pip3 install psutil requests

**Step 3: Configure the Script**

Download the provided script (sys_check.py) to a directory on your server.

Open the script in a text editor. Do not modify the script content, as it may break functionality.

Find the following lines in the script:

**Replace 'YOUR_API_TOKEN_HERE' with your actual API token**

api_token = 'YOUR_API_TOKEN_HERE'

Replace 'YOUR_API_TOKEN_HERE' with the API token you obtained in Step 1.

**Step 4: Moving the Service File**

Download the provided service file (sys_check.service) to your server.

Open the service file in a text editor to make necessary changes before moving it.

Make sure to modify the ExecStart and WorkingDirectory lines according to your file structure:

ExecStart: Update the path to the sys_check.py script. The example uses /etc/bellsocket/services/sys_check.py, but you should replace it with the actual path to your script.

WorkingDirectory: Set this to the directory where the sys_check.py script is located (/etc/bellsocket/services in the example).

Save the changes to the service file.

Now, move the modified service file to the system directory for systemd service files. Run:

Open the script in a text editor.

Make sure to modify the ExecStart and WorkingDirectory lines according to your file structure:

ExecStart: Update the path to the sys_check.py script. The example uses /etc/bellsocket/services/sys_check.py, but you should replace it with the actual path to your script.

WorkingDirectory: Set this to the directory where the sys_check.py script is located (/etc/bellsocket/services in the example).

Save the changes to the service file.

Now, move the modified service file to the system directory for systemd service files.

sudo mv path_to_downloaded_service_file /etc/systemd/system/sys_check.service

**Step 5: Enable and Start the Service**

Enable the service to start on boot:

sudo systemctl enable sys_check.service

Start the service:

sudo systemctl start sys_check.service
    
Step 6: Manual Script Execution

To manually execute the script for debugging purposes, open a terminal and navigate to the directory where the script is located. Run the following command:

python3 sys_check.py

This will run the script interactively in your terminal, allowing you to observe its behavior and check for any errors.

**Generating a Secret Key for Support (Optional)**

If you encounter any errors or need assistance with the setup, you can generate a secret key that will allow our support team to help you efficiently. Follow these steps:

In the terminal, navigate to the directory where the sys_check.py script is located. For example:

cd /etc/bellsocket/services

Run the following command to generate a secret key:

python3 -c "import secrets; print(secrets.token_hex(16))"

A secret key will be generated and displayed in the terminal. Copy this key and keep it secure.

If you need to reach out to our support team, provide them with the secret key. This key will allow them to better understand your setup and assist you more effectively.

Remember, generating and sharing this secret key is optional, but it can greatly aid our support team in helping you troubleshoot any issues you encounter.

**Important Notes**

Do not modify the script content: Modifying the script may cause it to malfunction. If you need to make changes, consult the script's author or refer to its documentation.

Service Management: You can manage the script service using systemctl commands. For example, to stop the service, run sudo systemctl stop sys_check.service.
