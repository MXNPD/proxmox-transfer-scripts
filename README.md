Here’s a clean, structured **README.md** you can drop straight into your repo:

````markdown
# Proxmox Transfer Scripts

A modular Python toolkit for handling **VM and container transfers** in Proxmox VE.  
This project provides simple CLI commands to **backup, migrate, restore, and manage storage/VMs** across Proxmox nodes.

---

## 📂 Project Structure

- **`main.py`** – CLI entry point for all commands.  
- **`backup_handler.py`** – Handles VM/CT backups (`vzdump`).  
- **`restore_handler.py`** – Restores backups to a target node/storage.  
- **`migration_handler.py`** – Orchestrates full migrations (backup → transfer → restore).  
- **`storage_handler.py`** – Handles storage validation, checks, and space availability.  
- **`vm_handler.py`** – VM/CT lifecycle helpers (start, stop, status).  
- **`utils.py`** – Shared utilities (logging, SSH/rsync wrappers, etc.).

---

## ⚡ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/MXNPD/proxmox-transfer-scripts.git
   cd proxmox-transfer-scripts
````

2. Ensure Python 3 is installed.

3. Install any required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   *(if no `requirements.txt` exists, dependencies are minimal and rely on `subprocess` + system tools like `ssh`, `rsync`, `vzdump`.)*

---

## 🚀 Usage

Run everything from `main.py`.

### **Migrate a VM/CT**

Moves a VM/CT from one node to another (backup → transfer → restore).

```bash
python3 main.py migrate \
  --vmid 101 \
  --source node1 \
  --target node2 \
  --storage local-lvm
```

### **Backup a VM/CT**

Creates a vzdump backup on a specific node/storage.

```bash
python3 main.py backup \
  --vmid 101 \
  --node node1 \
  --storage local-lvm
```

### **Restore a VM/CT**

Restores a backup file onto a target node/storage.

```bash
python3 main.py restore \
  --file /var/lib/vz/dump/vzdump-qemu-101.vma.zst \
  --target node2 \
  --storage local-lvm
```

### **Check Available Storage**

```bash
python3 main.py storage --node node1
```

### **Start/Stop a VM/CT**

```bash
python3 main.py vm --vmid 101 --action start
python3 main.py vm --vmid 101 --action stop
```

---

## 🔧 How It Works

* **Migration**:

  1. Stops the VM/CT (if running).
  2. Creates a backup (`vzdump`).
  3. Transfers the backup to the target node (`rsync`/`scp`).
  4. Restores on target node/storage.
  5. Starts VM/CT again.

* **Backup & Restore** can also be run standalone.

---

## ✅ Requirements

* Proxmox VE nodes with SSH access between them.
* `vzdump`, `rsync`, `scp`, and `qemu-img` installed on nodes.
* Python 3.8+ on the machine running these scripts.

---

## ⚠️ Notes

* Ensure passwordless SSH is set up between nodes for seamless operation.
* Recommended to test backups/restores on non-production VMs before using on critical workloads.
* Currently built for **Linux CLI environments**.

---
