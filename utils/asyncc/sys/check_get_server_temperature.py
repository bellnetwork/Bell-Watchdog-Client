import logging, psutil

async def get_server_temperature(sio):
    try:
        # psutil.sensors_temperatures() returns a dictionary of temperature data
        temperature_data = psutil.sensors_temperatures()
        
        # Check if the 'coretemp' key is present in the dictionary
        if 'coretemp' in temperature_data:
            core_temperatures = temperature_data['coretemp']
            
            # Assuming you want to get the average temperature of all cores
            total_temperature = sum(sensor.current for sensor in core_temperatures) / len(core_temperatures)
            logging.error(f"Total temperature: {total_temperature}")
            await sio.emit('live_get_server_temperature_check', {'total_temperature': total_temperature})
    except Exception as e:
        logging.error(f'got error in get_server_temperature: {e}')
        #error_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)        