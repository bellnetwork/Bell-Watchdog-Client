import platform, logging

def server_information(sio):

    sio.emit('server_information_check', {
        'server_machine': platform.machine(),
        'server_node': platform.node(),
        'server_platform': platform.platform(),
        'server_processor': platform.processor(),
        'python_version': platform.python_version(), 
        'server_release': platform.release(),
        'server_uname': platform.uname()
        })