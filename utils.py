import os
import logging

# ANSI color codes
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

# Configure logging
logging.basicConfig(filename='migration.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def print_colored(message, level="INFO"):
    colors = {
        "INFO": Color.GREEN,
        "WARNING": Color.YELLOW,
        "ERROR": Color.RED,
        "DEBUG": Color.BLUE
    }
    color = colors.get(level, Color.RESET)
    print(f"{color}{message}{Color.RESET}")

def execute_command(command):
    ssh_control_options = "-o ControlMaster=auto -o ControlPath=/tmp/ssh_mux_%h_%p_%r -o ControlPersist=10m"
    
    # Check if the command involves 'scp' and replace it with 'rsync'
    if command.startswith("scp"):
        parts = command.split()
        source, destination = parts[1], parts[2]
        command = f"rsync -e 'ssh {ssh_control_options}' -avz {source} {destination}"
    
    if command.startswith("ssh"):
        command = command.replace("ssh", f"ssh {ssh_control_options}")
    
    print_colored(f"Executing command: {command}", "DEBUG")
    logging.debug(f"Executing command: {command}")
    process = os.popen(command)
    output = process.read()
    process.close()
    logging.debug(f"Command output: {output}")
    return output

def main():
    print_colored("Proxmox VM Migration Tool", "INFO")
    
    # Example setup for testing the SSH connection reuse
    print_colored("Testing SSH connection reuse with ControlMaster...", "INFO")
    test_command = "ssh root@destination_ip echo 'SSH connection successful'"
    execute_command(test_command)
    
    print_colored("Test completed. Continue with migration logic.", "INFO")

if __name__ == "__main__":
    main()
