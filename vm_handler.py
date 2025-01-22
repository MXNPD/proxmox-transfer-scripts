import logging
from utils import execute_command

def list_vms():
    """
    Lists all virtual machines on the Proxmox server.
    """
    command = "qm list"
    output = execute_command(command)
    lines = output.strip().split("\n")
    vms = []
    for line in lines[1:]:
        parts = line.split()
        vms.append((parts[0], " ".join(parts[1:])))  # VMID, Name
    logging.info(f"Detected VMs: {vms}")
    return vms

def get_vm_storage(vmid):
    """
    Retrieves the storage location of a VM's disk.
    """
    command = f"qm config {vmid}"
    output = execute_command(command)
    lines = output.strip().split("\n")
    for line in lines:
        if line.startswith(("scsi0", "virtio0", "ide0")):
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
