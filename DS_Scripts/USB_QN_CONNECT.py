import subprocess

def send_adb_tcpip_command(port=5802):
    """
    Send adb tcpip command to enable TCP/IP communication on specified port.
    
    Args:
        port (int): The port number (default: 5802)
    """
    try:
        result = subprocess.run(
            ["adb", "tcpip", str(port)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Success: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
    except FileNotFoundError:
        print("Error: adb command not found. Ensure Android Debug Bridge is installed and in PATH.")

if __name__ == "__main__":
    send_adb_tcpip_command(5802)