import logging
from storage_handler import list_storage_options
from migration_handler import migrate_vm, migrate_all_vms
from utils import print_colored
from vm_handler import list_vms


def main():
    # Set up logging
    logging.basicConfig(
        filename="migration.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    print_colored("Proxmox VM Migration Tool", "INFO")

    # Fetch storage options from the source server
    print_colored("Fetching storage options from source server...", "INFO")
    source_storage_options = list_storage_options()
    if not source_storage_options:
        print_colored("No storage options found on the source server.", "ERROR")
        logging.error("No storage options found on the source server.")
        return

    print("Available storage options on source server:")
    for i, storage in enumerate(source_storage_options, start=1):
        print(f"{i}: {storage}")

    source_storage_choice = int(input("Select the source storage for backups (default is 'local', e.g., 1, 2...): ") or 1)
    source_storage = source_storage_options[source_storage_choice - 1]

    # Prompt for destination server
    dest_ip = input("Enter the destination Proxmox IP: ")

    # Fetch storage options from the destination server
    print_colored("Fetching storage options from destination server...", "INFO")
    dest_storage_options = list_storage_options(server_ip=dest_ip)
    if not dest_storage_options:
        print_colored("No storage options found on the destination server.", "ERROR")
        logging.error("No storage options found on the destination server.")
        return

    print("Available storage options on destination server:")
    for i, storage in enumerate(dest_storage_options, start=1):
        print(f"{i}: {storage}")

    dest_backup_choice = int(input("Select the destination storage for backups (e.g., 1, 2...): "))
    dest_backup_storage = dest_storage_options[dest_backup_choice - 1]

    dest_vm_choice = int(input("Select the destination storage for VMs (e.g., 1, 2...): "))
    dest_vm_storage = dest_storage_options[dest_vm_choice - 1]

    # Fetch and display VM list
    print_colored("Fetching list of VMs from source server...", "INFO")
    vms = list_vms()
    if not vms:
        print_colored("No VMs found on the source server.", "ERROR")
        logging.error("No VMs found on the source server.")
        return

    print("Select VMs to transfer (you can select multiple by entering numbers separated by commas):")
    print("0: Transfer all VMs")
    for i, (vmid, vm_name) in enumerate(vms, start=1):
        print(f"{i}: {vmid} - {vm_name}")

    choices = input("Enter your choice(s) (e.g., '0' for all VMs or '1, 2, 3' to select specific VMs): ")
    if "0" in choices.split(","):
        migrate_all_vms(source_storage, dest_ip, dest_backup_storage, dest_vm_storage)
    else:
        selected_vms = [vms[int(choice.strip()) - 1][0] for choice in choices.split(",") if choice.strip().isdigit()]
        for vmid in selected_vms:
            migrate_vm(vmid, source_storage, dest_ip, dest_backup_storage, dest_vm_storage)


if __name__ == "__main__":
    main()
