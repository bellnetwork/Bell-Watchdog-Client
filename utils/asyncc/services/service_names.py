def get_service_name(access_details):
    if "apache2" in access_details:
        return "HTTP"
    elif "sshd" in access_details or "sftp" in access_details:
        return "SSH/SFTP"
    elif "console-getty" in access_details:
        return "Console-Getty"
    elif "cron" in access_details:
        return "Cron"
    elif "dbus" in access_details:
        return "DBus"
    elif "getty@tty2" in access_details:
        return "Getty"
    elif "mariadb" in access_details:
        return "MariaDB"
    elif "networkd-dispatcher" in access_details:
        return "Networkd-Dispatcher"
    elif "rpcbind" in access_details:
        return "RPC Bind"
    elif "rsyslog" in access_details:
        return "RSyslog"
    elif "systemd-journald" in access_details:
        return "Systemd-Journald"
    elif "systemd-logind" in access_details:
        return "Systemd-Logind"
    elif "systemd-udevd" in access_details:
        return "Systemd-Udevd"
    elif "user@0" in access_details:
        return "User"
    elif "xinetd" in access_details:
        try:
            return access_details.split("/")[-1].split()[0]
        except IndexError:
            pass
    return access_details