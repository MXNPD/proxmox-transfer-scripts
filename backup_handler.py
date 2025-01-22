import os
import logging
from utils import execute_command, print_colored

def find_backup_file(vmid, dump_dir):
    """
    Locates the backup file for a specific VM in the dump directory.
    """
    pattern = os.path.join(dump_dir, f"vzdump-qemu-{vmid}-*.vma.zst")
    command = f"ls {pattern}"
    backup_file = execute_command(command).strip()
    if backup_file:
        logging.info(f"Found backup file for VM {vmid}: {backup_file}")
        return backup_file
    logging.error(f"No backup file found for VM {vmid} in directory {dump_dir}")
    return None

def backup_vm(vmid, dump_dir):
    """
    Creates a backup for a specific VM in the given dump directory.
    """
    command = f"vzdump {vmid} --compress zstd --dumpdir {dump_dir}"
    print_colored(f"Running backup command: {command}", "INFO")
    logging.info(f"Running backup command: {command}")
    output = execute_command(command)
    logging.debug(f"vzdump output for VM {vmid}: {output}")

    backup_file = find_backup_file(vmid, dump_dir)
    if backup_file:
        print_colored(f"Backup created for VM {vmid}: {backup_file}", "INFO")
        logging.info(f"Backup created for VM {vmid}: {backup_file}")
        return backup_file
    else:
        print_colored(f"Error: Backup file for VM {vmid} was not created.", "ERROR")
        logging.error(f"Error: Backup file for VM {vmid} was not created. Check vzdump output.")
        return None

def transfer_backup(backup_file, dest_ip, dest_backup_dir):
    """
    Transfers a backup file to the destination server.
    """
    command = f"scp {backup_file} root@{dest_ip}:{dest_backup_dir}/{os.path.basename(backup_file)}"
    print_colored(f"Transferring backup file: {backup_file} to {dest_backup_dir}", "INFO")
    logging.info(f"Transferring backup file: {backup_file} to {dest_backup_dir}")
    output = execute_command(command)
    if "error" in output.lower():
        print_colored(f"Error transferring backup {backup_file}", "ERROR")
        logging.error(f"Error transferring backup {backup_file}: {output}")
        return False
    else:
        print_colored(f"Backup {backup_file} transferred successfully.", "INFO")
        logging.info(f"Backup {backup_file} transferred successfully.")
        return True
