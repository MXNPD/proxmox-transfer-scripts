import logging
from utils import execute_command, print_colored

def restore_vm(vmid, dest_ip, dest_backup_dir, dest_storage):
    """
    Restores a VM from a backup file on the destination server.
    """
    # Find the backup file on the destination server
    backup_file_pattern = f"{dest_backup_dir}/vzdump-qemu-{vmid}-*.vma.zst"
    command_find = f"ssh root@{dest_ip} ls {backup_file_pattern}"
    backup_file = execute_command(command_find).strip()

    if not backup_file:
        print_colored(f"No matching backup file found on destination for VM {vmid}.", "ERROR")
        logging.error(f"No matching backup file found on destination for VM {vmid}.")
        return False

    # Construct and execute the restore command
    command_restore = f"ssh root@{dest_ip} \"qmrestore {backup_file} {vmid} --storage {dest_storage}\""
    print_colored(f"Restoring VM {vmid} on destination server: {dest_ip}", "INFO")
    logging.info(f"Restoring VM {vmid} on destination server: {dest_ip}")
    output = execute_command(command_restore)
    logging.debug(f"qmrestore output for VM {vmid}: {output}")

    if "error" in output.lower():
        print_colored(f"Error restoring VM {vmid}", "ERROR")
        logging.error(f"Error restoring VM {vmid} on destination: {output}")
        return False
    else:
        print_colored(f"VM {vmid} restored successfully on destination.", "INFO")
        logging.info(f"VM {vmid} restored successfully on destination.")
        return True
