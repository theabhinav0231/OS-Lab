import os
import sys
import platform
import uuid
import shutil
import time
import subprocess

# ==========================================
# UTILITY FUNCTIONS
# ==========================================
def print_header(title):
    print("\n" + "=" * 50)
    print(f"   {title}")
    print("=" * 50)

def log_activity(message):
    """Simulates writing to system_log.txt as seen in the repo"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    try:
        with open("system_log.txt", "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing to log: {e}")

# ==========================================
# TASK 1: PROCESS & SYSTEM CALLS
# ==========================================
def task1_process_info():
    """
    Simulates fetching Process Control Block (PCB) information using system calls.
    """
    print_header("Task 1: Process Information (System Calls)")
    
    # 1. Get current Process ID
    pid = os.getpid()
    log_activity(f"System Call: os.getpid() -> {pid}")
    
    # 2. Get Parent Process ID (Cross-platform safe)
    if hasattr(os, 'getppid'):
        ppid = os.getppid()
    else:
        ppid = "N/A (Windows requires specific API)"
    log_activity(f"System Call: os.getppid() -> {ppid}")
    
    # 3. Get Current Directory
    cwd = os.getcwd()
    log_activity(f"System Call: os.getcwd() -> {cwd}")

    # 4. Simulate a child process (using subprocess to be OS agnostic)
    print("\n[Simulating Child Process Creation...]")
    try:
        # Pinging localhost is a safe, standard way to spawn a child process
        cmd = ['ping', '-c', '1', '127.0.0.1'] if platform.system() != 'Windows' else ['ping', '-n', '1', '127.0.0.1']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child_pid = process.pid
        log_activity(f"Child Process Spawned (PID: {child_pid})")
        process.wait()
        log_activity(f"Child Process (PID: {child_pid}) Terminated")
    except Exception as e:
        print(f"Child process simulation failed: {e}")

# ==========================================
# TASK 2: SYSTEM INFORMATION
# ==========================================
def task2_system_stats():
    """
    Simulates fetching Kernel and OS statistics.
    """
    print_header("Task 2: System Information Detection")
    
    uname = platform.uname()
    
    info = {
        "System": uname.system,
        "Node Name": uname.node,
        "Release": uname.release,
        "Version": uname.version,
        "Machine": uname.machine,
        "Processor": uname.processor
    }
    
    for key, value in info.items():
        print(f"{key:<15}: {value}")
        log_activity(f"Detected {key}: {value}")

# ==========================================
# TASK 3: VIRTUAL MACHINE DETECTION
# ==========================================
def task3_vm_detection():
    """
    Task 3: Checks MAC address and specific files to detect if running in a VM.
    Common VM MAC Vendors:
    00:05:69 (VMware), 00:0C:29 (VMware), 00:50:56 (VMware)
    00:1C:42 (Parallels)
    08:00:27 (VirtualBox)
    """
    print_header("Task 3: Virtual Machine (VM) Detection")
    
    # 1. MAC Address Analysis
    mac_num = uuid.getnode()
    mac_hex = ':'.join(['{:02x}'.format((mac_num >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    print(f"Current MAC Address: {mac_hex}")
    
    # Standard OUI prefixes for VMs
    vm_ouis = {
        "00:05:69": "VMware", "00:0c:29": "VMware", "00:50:56": "VMware",
        "08:00:27": "VirtualBox",
        "00:1c:42": "Parallels",
        "00:15:5d": "Hyper-V"
    }
    
    detected_vm = "Unknown / Physical Machine"
    mac_prefix = mac_hex[:8].lower() # First 3 bytes
    
    for oui, vendor in vm_ouis.items():
        if mac_hex.startswith(oui):
            detected_vm = f"Virtual Machine ({vendor})"
            break
            
    log_activity(f"MAC Analysis Result: {detected_vm}")

    # 2. Check for common VM files (Linux specific simulation)
    if platform.system() == "Linux":
        vm_files = [
            "/sys/class/dmi/id/product_uuid",
            "/sys/class/dmi/id/sys_vendor"
        ]
        print("\nChecking Hypervisor signatures in /sys/class/dmi/...")
        for file in vm_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        content = f.read().strip()
                        print(f"  Found {file}: {content}")
                        if "VMware" in content or "VirtualBox" in content:
                            log_activity("Hypervisor Signature Found in System Files")
                except PermissionError:
                    print(f"  {file} exists (Permission Denied to read)")
    else:
        print("\n(Skipping Linux-specific file checks on non-Linux OS)")

# ==========================================
# TASK 4: FILE SYSTEM OPERATIONS
# ==========================================
def task4_file_operations():
    """
    Task 4: Programmatic creation, writing, renaming, and deletion of files.
    """
    print_header("Task 4: Automated File System Operations")
    
    dir_name = "lab4_test_dir"
    file_name = "os_lab_test.txt"
    renamed_file = "os_lab_final.txt"
    
    # 1. Create Directory
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        log_activity(f"Created directory: {dir_name}")
    else:
        log_activity(f"Directory {dir_name} already exists")
        
    file_path = os.path.join(dir_name, file_name)
    
    # 2. Write File
    with open(file_path, "w") as f:
        f.write("Operating System Lab Assignment 4\nTask: File Systems")
    log_activity(f"Created and wrote to file: {file_path}")
    
    # 3. Read File
    with open(file_path, "r") as f:
        content = f.read()
    print(f"  [File Content]: {content}")
    
    # 4. Rename File
    new_path = os.path.join(dir_name, renamed_file)
    if os.path.exists(new_path):
        os.remove(new_path) # Clean up if exists
    os.rename(file_path, new_path)
    log_activity(f"Renamed {file_name} to {renamed_file}")
    
    # 5. Clean up (Optional, kept for demonstration)
    print("\nCleaning up created files (Simulation Reset)...")
    try:
        shutil.rmtree(dir_name)
        log_activity(f"Deleted directory: {dir_name}")
    except Exception as e:
        print(f"Cleanup failed: {e}")

# ==========================================
# TASK 5: RECURSIVE DIRECTORY TRAVERSAL
# ==========================================
def task5_directory_traversal():
    """
    Task 5: Walk through a directory tree (simulating 'ls -R' or 'tree').
    """
    print_header("Task 5: Directory Traversal (os.walk)")
    
    # Create a dummy structure for demonstration
    base = "lab4_tree_demo"
    os.makedirs(os.path.join(base, "subdir1"), exist_ok=True)
    os.makedirs(os.path.join(base, "subdir2"), exist_ok=True)
    with open(os.path.join(base, "root_file.txt"), "w") as f: f.write("x")
    with open(os.path.join(base, "subdir1", "nested.txt"), "w") as f: f.write("x")
    
    print(f"Scanning directory structure for: {base}\n")
    
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(base):
        level = root.replace(base, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}|-- {os.path.basename(root)}/")
        total_dirs += 1
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}|-- {f}")
            total_files += 1

    log_activity(f"Traversal Complete: Found {total_files} files in {total_dirs} directories.")
    
    # Cleanup
    shutil.rmtree(base)

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    while True:
        print("\n" + "="*40)
        print("   OS LAB 4: SYSTEM CALLS & VM DETECTION")
        print("="*40)
        print("1. Process Info (Task 1)")
        print("2. System Stats (Task 2)")
        print("3. VM Detection (Task 3)")
        print("4. File Ops Simulation (Task 4)")
        print("5. Directory Walk (Task 5)")
        print("6. Run All Tasks")
        print("0. Exit")
        
        choice = input("\nEnter Choice: ")
        
        if choice == '1':
            task1_process_info()
        elif choice == '2':
            task2_system_stats()
        elif choice == '3':
            task3_vm_detection()
        elif choice == '4':
            task4_file_operations()
        elif choice == '5':
            task5_directory_traversal()
        elif choice == '6':
            task1_process_info()
            task2_system_stats()
            task3_vm_detection()
            task4_file_operations()
            task5_directory_traversal()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()