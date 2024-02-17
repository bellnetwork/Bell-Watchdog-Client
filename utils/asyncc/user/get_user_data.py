import subprocess

async def get_user_name(ip_address):
    try:
        output = subprocess.check_output(["who"], universal_newlines=True)
        lines = output.strip().split("\n")
        for line in lines:
            if ip_address in line:
                return line.split()[0]
    except Exception as e:
        print(f"Error getting user name: {e}")
    return "Unknown"