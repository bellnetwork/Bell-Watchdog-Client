import psutil
from utils.sys.sys_messages.logging import setup_custom_logging

async def get_server_temperature(sio):
    try:
        # psutil.sensors_temperatures() returns a dictionary of temperature data
        temperature_data = psutil.sensors_temperatures()
        
        # Check if the 'coretemp' key is present in the dictionary
        if 'coretemp' in temperature_data:
            core_temperatures = temperature_data['coretemp']
            
            # Assuming you want to get the average temperature of all cores
            total_temperature = sum(sensor.current for sensor in core_temperatures) / len(core_temperatures)
            setup_custom_logging('info', 'Total temperature', f' {total_temperature}')
            await sio.emit('live_get_server_temperature_check', {'total_temperature': total_temperature})
    except Exception as e:
        setup_custom_logging('error', 'Total temperature', f' There was an error: {e}')      