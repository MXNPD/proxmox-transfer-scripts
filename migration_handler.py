import logging
from storage_handler import list_storage_options, get_dump_directory
from backup_handler import backup_vm, transfer_backup
from restore_handler import restore_vm
from vm_handler import list_vms
from utils import print_colored

def migrate_vm(vmid, source_storage, dest_ip, dest_backup_storage, dest_vm_storage):
    """
    Handles the full migration process for a single VM.
    """
    print_colored(f"Starting migration for VM {vmid}...", "INFO")
    logging.info(f"Starting migration for VM {vmid}")

    # Get source dump directory
    dump_dir = get_dump_directory(source_storage)
    print_colored(f"Backup directory for storage '{source_storage}': {dump_dir}", "DEBUG")

    # Backup the VM
    backup_file = backup_vm(vmid, dump_dir)
    if not backup_file:
        print_colored(f"Backup failed for VM {vmid}. Skipping migration.", "ERROR")
        logging.error(f"Backup failed for VM {vmid}. Skipping migration.")
        return False

    # Transfer the backup to the destination server
    dest_backup_dir = get_dump_directory(dest_backup_storage)
    if not transfer_backup(backup_file, dest_ip, dest_backup_dir):
        print_colored(f"Backup transfer failed for VM {vmid}. Skipping migration.", "ERROR")
        logging.error(f"Backup transfer failed for VM {vmid}. Skipping migration.")
        return False

    # Restore the VM on the destination server
    restore_vm(vmid, dest_ip, dest_backup_dir, dest_vm_storage)

    print_colored(f"Migration for VM {vmid} completed successfully!", "INFO")
    logging.info(f"Migration for VM {vmid} completed successfully")
    return True

def migrate_all_vms(source_storage, dest_ip, dest_backup_storage, dest_vm_storage):
    """
    Handles the migration process for all VMs.
    """
    print_colored("Fetching list of VMs from source server...", "INFO")
    vms = list_vms()
    if not vms:
        print_colored("No VMs found on the source server.", "ERROR")
        logging.error("No VMs found on the source server.")
        return

    for vmid, vm_name in vms:
        print_colored(f"Preparing to migrate VM {vmid} ({vm_name})", "INFO")
        migrate_vm(vmid, source_storage, dest_ip, dest_backup_storage, dest_vm_storage)
