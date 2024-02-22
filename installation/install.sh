#!/bin/bash

# Define log file path
LOG_FILE="/tmp/bellwatchdog.log"

# Clear the log file at the start of the script
> $LOG_FILE

# Define helper function for logging
print_info() {
    echo -e "\033[34mINFO: $1\033[0m" | tee -a $LOG_FILE
}

print_success() {
    echo -e "\033[32mSUCCESS: $1\033[0m" | tee -a $LOG_FILE
}

print_warning() {
    echo -e "\033[33mWARNING: $1\033[0m" | tee -a $LOG_FILE
}

print_error() {
    echo -e "\033[31mERROR: $1\033[0m" | tee -a $LOG_FILE
}

# Function to print a progress bar
print_progress() {
    local percent_done=$1
    local width=60 # Total width of the progress bar
    local filled_width=$((percent_done * width / 100))
    local unfilled_width=$((width - filled_width))
    printf -v filled_bar "%${filled_width}s" "" # Create a string with spaces equal to filled width
    printf -v unfilled_bar "%${unfilled_width}s" "" # Create a string with spaces equal to unfilled width
    printf "Progress: [%3d%%] [%s%s]\r" "$percent_done" "${filled_bar// /#}" "${unfilled_bar// / }"
    if [[ $percent_done -eq 100 ]]; then echo; fi # Move to a new line at 100%
}

# Determine the package manager and check system compatibility
PKG_MANAGER=""
if command -v apt > /dev/null; then
    PKG_MANAGER="apt-get"
    print_info "Detected APT package manager. Proceeding with Debian/Ubuntu compatible operations."
elif command -v dnf > /dev/null; then
    PKG_MANAGER="dnf"
    print_info "Detected DNF package manager. Proceeding with Fedora compatible operations."
elif command -v yum > /dev/null; then
    PKG_MANAGER="yum"
    print_info "Detected YUM package manager. Proceeding with CentOS/RHEL compatible operations."
else
    print_error "Unsupported package manager or Linux distribution. This script supports APT (Debian/Ubuntu), DNF (Fedora), and YUM (CentOS/RHEL)."
    exit 1
fi

# General function to check if a package is installed
is_package_installed() {
    if [[ "$PKG_MANAGER" == "apt-get" ]]; then
        dpkg -l "$1" &> /dev/null
    else
        rpm -q "$1" &> /dev/null
    fi
}

# Check if packages are installed
check_packages_installed() {
    local system_packages=("python3" "python3-pip" "git" "sysstat")
    local python_packages=("aiohttp" "asyncio" "python-socketio" "dotenv" "psutil" "colorama")
    local pkg_installed=true

    # Check system packages
    for pkg in "${system_packages[@]}"; do
        if dpkg -l 2>/dev/null | grep -qw "$pkg"; then
            print_success "Installed system package: $pkg"
        else
            print_error "Missing system package: $pkg"
            pkg_installed=false
        fi
    done

    # Check Python packages
    for py_pkg in "${python_packages[@]}"; do
        if pip3 list --format=freeze 2>/dev/null | grep -qw "$py_pkg"; then
            print_success "Installed Python package: $py_pkg"
        else
            print_error "Missing Python package: $py_pkg"
            pkg_installed=false
        fi
    done

    if $pkg_installed; then
        return 0
    else
        return 1
    fi
}

# Install missing packages
install_packages() {
    print_info "Updating package lists..."
    if [ "$PKG_MANAGER" = "apt" ]; then
        apt-get update &> /dev/null &
        PID=$!
        for i in {1..50}; do
            sleep 0.1
            print_progress $((i * 2))
        done
        wait $PID
        print_success "Package lists updated."
    fi

    local packages=("python3" "python3-pip" "git" "sysstat" "aiohttp")
    local PIP_OPTIONS=""

    # Detect if running on Debian 12
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [ "$ID" = debian ] && [ "$VERSION_ID" = "12" ]; then
            print_info "Detected Debian 12, using --break-system-packages for pip installations."
            PIP_OPTIONS="--break-system-packages"
        fi
    fi

    for pkg in "${packages[@]}"; do
        print_info "Installing $pkg..."
        $PKG_MANAGER install -y $pkg &> /dev/null &
        PID=$!
        for i in {1..50}; do
            sleep 0.1
            print_progress $((i * 2))
        done
        wait $PID
        print_success "$pkg installed."
    done

    local python_packages=("aiohttp" "asyncio" "python-socketio" "python-dotenv" "python-socketio[client]" "psutil" "colorama")

    for py_pkg in "${python_packages[@]}"; do
        print_info "Installing Python package $py_pkg..."
        pip3 install $PIP_OPTIONS $py_pkg &> /dev/null &
        PID=$!
        for i in {1..50}; do
            sleep 0.1
            print_progress $((i * 2))
        done
        wait $PID
        print_success "Python package $py_pkg installed."
    done

    # Verify installation
    if check_packages_installed; then
        return 0
    else
        return 1
    fi
}

# Function to check and optionally delete a directory
check_and_prepare_directory() {
    local directory_path="$1"
    local directory_name="$2" # For logging purposes

    if [ -d "$directory_path" ]; then
        print_error "The directory '$directory_path' ($directory_name) already exists."
        print_info "Do you want to delete the existing directory and proceed? (yes/no)"
        read -r user_choice
        case "$user_choice" in
            yes|y)
                rm -rf "$directory_path"
                print_success "Existing directory '$directory_path' removed."
                ;;
            no|n)
                print_error "Installation aborted by the user."
                return 1
                ;;
            *)
                print_error "Invalid input. Please answer yes/y or no/n."
                return 1
                ;;
        esac
    fi
    return 0
}

# Main function to download and prepare the Bell Watchdog
get_script() {
    local repo_url="https://github.com/bellnetwork/Bell-Sys-Monitor-Client-Linux.git"
    local target_dir="bellwatchdog"
    local final_path="/etc/bell/$target_dir"

    # Check and prepare local target directory
    if ! check_and_prepare_directory "$target_dir" "local target"; then
        return 1
    fi

    # Check and prepare final path
    if ! check_and_prepare_directory "$final_path" "final path"; then
        return 1
    fi

    print_info "Downloading Bell Watchdog Client..."
    if git clone "$repo_url" "$target_dir"; then
        print_success "Repository cloned successfully."
    else
        print_error "Failed to clone repository."
        return 1
    fi

    # Ensure the /etc/bell/ directory exists before moving
    mkdir -p "/etc/bell"

    # Move the cloned directory to the final path
    mv "$target_dir" "$final_path" | tee -a $LOG_FILE

    if [ $? -eq 0 ]; then
        print_success "Successfully moved the directory to '$final_path'."
        move_service
    else
        print_error "Failed to move the directory to '$final_path'."
        return 1
    fi
    return 0
}

# Move the service file
move_service() {
    local service_file="bellwatchdog.service"
    local source_service_file="/etc/bell/$target_dir/installation/service/$service_file"
    local target_service_path="/etc/systemd/system/$service_file"

    # Check if the service file already exists in the target location
    if [ -f "$target_service_path" ]; then
        print_error "The service file '$service_file' already exists in '/etc/systemd/system'."
        print_info "Do you want to overwrite the existing service file? (yes/no)"
        read -r overwrite_choice
        case "$overwrite_choice" in
            yes|y)
                # Overwrite the existing service file
                ;;
            no|n)
                print_error "Skipping service file move. The existing service file will be used."
                return 0
                ;;
            *)
                print_error "Invalid input. Please answer yes/y or no/n."
                return 1
                ;;
        esac
    fi

    # Move the service file to the systemd system directory
    if mv "$source_service_file" "$target_service_path"; then
        print_success "Successfully moved the service file to '$target_service_path'."
        systemctl daemon-reload
        print_success "Systemd daemon reloaded to recognize the new service."
    else
        print_error "Failed to move the service file to '$target_service_path'."
        return 1
    fi
    return 0
}

# Create a connection
create_connection() {
    local new_hostname=""
    local default_hostname=""

    while true; do
        print_info "Enter the WebSocket hostname or IP address (e.g., socket.mydomain.com or 12.34.56.78)${default_hostname:+ (default $default_hostname)}:"
        read -r new_hostname

        # If no new hostname entered and default is available, use the default
        if [ -z "$new_hostname" ] && [ ! -z "$default_hostname" ]; then
            new_hostname=$default_hostname
        fi

        # If new_hostname is still empty, prompt again
        if [ -z "$new_hostname" ]; then
            print_error "You must enter a valid hostname or IP address."
            continue # Skip the rest of the loop and prompt again
        fi

        # Attempt to connect with the provided or default hostname
        if test_connection "$new_hostname"; then
            print_success "Connection successful."
            break # Exit loop if connection is successful
        else
            print_error "Failed to connect to $new_hostname. Please ensure the WebSocket server is online and accessible."
            # Set the entered hostname as the new default for the next prompt iteration
            default_hostname=$new_hostname
        fi
    done
}

# Test the connection to the websocket
test_connection() {
    local hostname=$1
    print_info "Attempting to create a connection to $hostname..."
    if curl -s --head --request GET "$hostname" | grep "200 OK" > /dev/null | tee -a $LOG_FILE; then
        print_success "Successfully connected to $hostname"
        
        # Now, call save_hostname and use its return value
        save_hostname "$hostname"
        local save_status=$?
        if [ $save_status -eq 0 ]; then
            print_success "Hostname has been successfully saved after successful connection."
            return 0
        else
            print_error "Failed to save the hostname after successful connection."
            return 1
        fi
    else
        print_error "Failed to connect to $hostname. Please ensure the websocket is online and accessible."
        return 1
    fi
}

# Save the entered hostname to .env
save_hostname() {
    local hostname=$1
    local target_dir="/etc/bell/bellwatchdog"
    local env_file_path="$target_dir/.env"

    if [ -f "$env_file_path" ]; then
        # The .env file exists, attempt to update SERVER_HOSTNAME
        sed -i "s|SERVER_HOSTNAME='.*'|SERVER_HOSTNAME='wss://$hostname'|g" "$env_file_path"
        
        if [ $? -eq 0 ]; then
            print_success "Hostname successfully updated in .env config file."
        else
            print_error "Failed to update hostname in .env config file."
        fi
    else
        # The .env file doesn't exist, create it and add SERVER_HOSTNAME
        echo "Creating a new .env file at $env_file_path"
        echo "SERVER_HOSTNAME='$hostname'" > "$env_file_path"
        
        if [ $? -eq 0 ]; then
            print_success "The .env file was successfully created and the hostname was saved."
        else
            print_error "Failed to create .env file and save hostname."
        fi
    fi
}

# Try the new app
try_the_app() {
    local script_path="/etc/bell/bellwatchdog"
    local app_entry_point="app"
    print_success "Would you like to test your new script now? (yes/no)"
    read -r want_try_app
    if [[ $want_try_app =~ ^(yes|y)$ ]]; then

        print_info "Attempting to start the script for testing..."
        # Start the script in the background and wait for up to 20 seconds
        (cd $script_path && timeout 20 python3 -m $app_entry_point) &>> $LOG_FILE &
        local script_pid=$!

        local progress=0
        while [[ $progress -lt 100 && -d "/proc/$script_pid" ]]; do
            sleep 2 # Wait for 2 seconds before updating the progress
            ((progress+=10)) # Increment progress
            print_progress "$progress"
        done

        wait $script_pid
        local exit_status=$?

        if [[ $exit_status -eq 0 ]] || [[ $exit_status -eq 124 ]]; then
            print_info "The script was tested successfully for 20 seconds."
            head -n 10 /tmp/bellwatchdog.log
            print_success "For more details, see /tmp/bellwatchdog.log"
            print_success "The script was automatically stopped after 20 seconds as planned."
            print_success "Installation is now complete."
            start_service
        else
            print_error "There was an issue starting the script. Please review the output in /tmp/bellwatchdog.log for more details."
        fi
    else
        setup_completed
    fi
}

# Start and enable the service
start_service() {
    local service_name="bellwatchdog.service"

    print_success "Do you want to start Bell Watchdog as a service? (yes/y or no/n):"
    read -r service_choice
    if [[ $service_choice =~ ^(yes|y)$ ]]; then
        # Enable the service to start on boot
        if systemctl enable "$service_name"; then
            print_success "The service '$service_name' has been enabled to start on boot."
        else
            print_error "Failed to enable the service '$service_name'."
            return 1
        fi
        
        # Start the service immediately
        if systemctl start "$service_name"; then
            print_success "The service '$service_name' has been started successfully."
            cleanup_system
        else
            print_error "Failed to start the service '$service_name'."
            return 1
        fi
    elif [[ $service_choice =~ ^(no|n)$ ]]; then
        print_warning "Service startup skipped by the user."
        cleanup_system
    else
        print_error "Invalid input. Please answer yes/y or no/n."
        start_service
    fi
}

# Clean up the installation
cleanup_system() {
    local installation_dir="/etc/bell/bellwatchdog/installation"
    print_info "Initiating cleanup process..."

    # Check if the installation directory exists and remove it
    if [ -d "$installation_dir" ]; then
        print_info "Removing installation directory: $installation_dir"
        rm -rf "$installation_dir"
        if [ $? -eq 0 ]; then
            print_success "Installation directory removed successfully."
        else
            print_error "Failed to remove the installation directory. Manual removal may be required."
        fi
    else
        print_warning "Installation directory does not exist or has already been removed."
    fi

    # Corrected part for the debug log file
    if [ -f "$LOG_FILE" ]; then
        print_info "Removing log file: $LOG_FILE"
        rm -f "$LOG_FILE"
        if [ $? -eq 0 ]; then
            print_success "Debug log file removed successfully."
        else
            print_error "Failed to remove the log file. Manual removal may be required."
        fi
    else
        print_warning "Debug log file does not exist or has already been removed."
    fi

    print_success "System cleanup completed."
    setup_completed
}


# Function to simulate typing effect in terminal
print_typing() {
    local message=$1
    local delay=${2:-0.02} # Default delay between characters

    # Loop through all characters in the message
    for (( i=0; i<${#message}; i++ )); do
        echo -n "${message:$i:1}"
        sleep $delay # Wait a bit before printing the next character
    done
    echo # Move to the new line at the end of the message
}

# The setup was completed success
setup_completed() {
    echo -e "\033[32m" # Change text color to green for success messages
    print_typing "Congratulations! Bell Watchdog is now ready to safeguard your digital environment."
    print_typing "For immediate debugging, launch the script using the command below:"
    print_typing "cd /etc/bell/bellwatchdog && python3 -m app"
    
    print_typing "Manage the Bell Watchdog service with the following commands:"
    print_typing "- Start Service: systemctl start bellwatchdog"
    print_typing "- Restart Service: systemctl restart bellwatchdog"
    print_typing "- Stop Service: systemctl stop bellwatchdog"
    print_typing "- Service Status: systemctl status bellwatchdog"
    
    print_typing "We're committed to providing you with the best experience. For assistance or to share feedback:"
    print_typing "- Report Issues: https://github.com/bellnetwork/Bell-Watchdog-Linux/issues"
    print_typing "- Contribute: https://github.com/bellnetwork/Bell-Watchdog-Linux/pulls"
    print_typing "- Support Ticket: https://bellwatchdog.cloud/github/help"
    
    print_typing "Thank you for choosing Bell Watchdog. Your journey towards a more secure and efficient IT environment begins now."
    echo -e "\033[0m" # Reset text color to default
}

# Function to detect and validate the operating system
detect_and_validate_os() {
    local supported_os=("debian" "ubuntu" "centos" "fedora" "rhel")
    # Extract the OS name and convert it to lowercase
    local os_name=$(awk -F= '/^NAME/{print tolower($2)}' /etc/os-release | tr -d '"' | tr '[:upper:]' '[:lower:]')

    print_info "Detected OS: $os_name"

    # Check if the current OS is in the list of supported OSes, ignoring case
    for os in "${supported_os[@]}"; do
        if [[ "$os_name" == *$os* ]]; then
            print_success "This operating system ($os_name) is supported."
            return 0
        fi
    done

    print_error "This script can only be installed on the following operating systems: ${supported_os[*]}."
    print_error "Exiting installation."
    exit 1
}

# Start setup
start_setup() {
    print_info "Welcome to the Bell Monitor Client setup."
    print_info "Detecting operating system..."
    
    detect_and_validate_os

    print_info "We are now preparing the installation. This may take a short time."

    if check_packages_installed; then
        print_success "Great. It seems you already installed all packages."
    else
        print_error "It looks like some packages are missing. Do you want to install them? (yes/no)"
        read -r install_choice
        until [[ $install_choice =~ ^(yes|y|no|n)$ ]]; do
            print_error "Invalid input. Please answer yes/y or no/n."
            read -r install_choice
        done

        if [[ $install_choice =~ ^(yes|y)$ ]]; then
            print_info "Alright. We are now updating your system and will install all necessary packages. This may take a while."
            if ! install_packages; then
                print_error "Failed to install packages."
                exit 1 # Exiting due to failure
            fi
        elif [[ $install_choice =~ ^(no|n)$ ]]; then
            print_error "Installation aborted by the user."
            exit 1 # Exiting due to user choice
        fi
    fi

    print_info "Proceeding with script download and setup..."
    if ! get_script; then
        print_error "Failed to download and prepare the Bell Watchdog."
        exit 1
    fi

    if ! create_connection; then
        print_error "Failed to establish a connection. Please ensure the WebSocket server is online and accessible."
        exit 1
    fi

    try_the_app
}

# Execute the setup function
start_setup
