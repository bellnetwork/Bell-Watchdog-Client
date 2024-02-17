import logging


"""
NEED TO MODIFY SOON

async def check_server_status(sio):
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