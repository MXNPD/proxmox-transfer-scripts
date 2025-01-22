from utils import execute_command, print_colored
import logging

def list_storage_options(server_ip=None):
    """
    Lists available storage options on a Proxmox server.
    """
    command = "pvesm status" if not server_ip else f"ssh root@{server_ip} pvesm status"
    output = execute_command(command)
    lines = output.strip().split("\n")
    storage_options = []
    for line in lines[1:]:  # Skip the header line
        parts = line.split()
        if len(parts) > 0:
            storage_options.append(parts[0])  # Storage name is the first column
    logging.info(f"Detected storage options: {storage_options}")
    return storage_options

def get_dump_directory(storage):
    """
    Finds the dump directory path for a given storage name.
    """
    command = f"pvesm status | grep ^{storage}\\s"
    output = execute_command(command)
    lines = output.strip().split("\n")
    for line in lines:
        parts = line.split()
        if len(parts) > 5:  # Ensure enough columns exist
            logging.info(f"Detected backup storage path for {storage}: {parts[5]}")
            return parts[5]  # Path column
    logging.warning(f"Using default dump directory for storage {storage}: /var/lib/vz/dump/")
    return "/var/lib/vz/dump/"  # Default fallback

def get_vm_storage(vmid):
    """
    Determines the storage used by a specific VM.
    """
    command = f"qm config {vmid}"
    output = execute_command(command)
    lines = output.strip().split("\n")
    for line in lines:
        if line.startswith("scsi0") or line.startswith("virtio0") or line.startswith("ide0"):
            if "=" in line:
                parts = line.split(",")
                key_value = parts[0].split("=")
                if len(key_value) > 1:
                    storage = key_value[1]
                    logging.info(f"Detected storage for VM {vmid}: {storage}")
                    return storage
            logging.warning(f"Unexpected format in line for VM {vmid}: {line}")
    logging.warning(f"No specific storage detected for VM {vmid}, using default.")
    return None
