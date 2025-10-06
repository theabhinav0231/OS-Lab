import os
import sys
import time

# --- Task 1: Process Creation Utility ---
def task_1_process_creation(num_children=3):
    """
    Creates a specified number of child processes using os.fork().
    The parent process waits for all children to complete.
    [cite_start][cite: 35, 36]
    """
    print(f"\n--- Task 1: Creating {num_children} Child Processes using os.fork() ---")
    child_pids = []

    for i in range(num_children):
        pid = os.fork()

        if pid == 0:
            # --- Child Process Logic ---
            child_pid = os.getpid()
            parent_pid = os.getppid()
            print(f"  Child-{i+1}: PID={child_pid}, Parent PID={parent_pid}")
            time.sleep(1) # Simulate doing some work
            os._exit(0) # Child must exit to prevent it from continuing the loop

        else:
            # --- Parent Process Logic ---
            print(f"Parent (PID:{os.getpid()}): Forked child with PID {pid}")
            child_pids.append(pid)

    # Parent waits for all children to finish
    for pid in child_pids:
        os.waitpid(pid, 0)

    print("Parent: All child processes have finished.")
    print("-" * 50)


# --- Task 2: Command Execution Using exec() ---
def task_2_command_execution():
    """
    Forks child processes to execute different Linux commands using os.execvp().
    [cite_start][cite: 38]
    """
    print("\n--- Task 2: Executing Commands in Child Processes ---")
    commands = {
        "List Files": ('ls', '-l'),
        "Current Date": ('date',),
        "Running Processes": ('ps', 'aux')
    }

    for desc, cmd in commands.items():
        pid = os.fork()

        if pid == 0:
            # --- Child Process Logic ---
            print(f"\n  Child (PID:{os.getpid()}) executing: '{' '.join(cmd)}'")
            try:
                os.execvp(cmd[0], cmd)
            except FileNotFoundError:
                print(f"Error: Command not found: {cmd[0]}")
                os._exit(1)
            # execvp replaces the child process, so this line is never reached on success

        else:
            # --- Parent Process Logic ---
            # Wait for the child to finish before creating the next one
            os.waitpid(pid, 0)
            print(f"Parent: Child for '{desc}' has finished.")

    print("\nParent: All command-executing children have finished.")
    print("-" * 50)


# --- Task 3: Zombie & Orphan Processes ---
def task_3_zombie_and_orphan():
    """
    Demonstrates the creation of zombie and orphan processes.
    [cite_start][cite: 40, 41]
    """
    print("\n--- Task 3: Simulating Zombie & Orphan Processes ---")

    # 1. Zombie Process Simulation
    print("\n-- Part A: Zombie Process --")
    pid = os.fork()
    if pid == 0:
        # Child process exits immediately
        print(f"  Zombie Child (PID:{os.getpid()}): Exiting now.")
        os._exit(0)
    else:
        # Parent does not wait, allowing the child to become a zombie
        print(f"  Parent (PID:{os.getpid()}): Created child {pid}, not waiting.")
        print("  >> The child is now a zombie. Check with 'ps -el | grep defunct' in another terminal.")
        time.sleep(5)
        # Now, the parent cleans up the zombie
        os.waitpid(pid, 0)
        print("  Parent: Cleaned up the zombie process.")

    # 2. Orphan Process Simulation
    print("\n-- Part B: Orphan Process --")
    pid = os.fork()
    if pid == 0:
        # Child process lives on after parent dies
        original_ppid = os.getppid()
        print(f"  Orphan Child (PID:{os.getpid()}): My parent is {original_ppid}.")
        time.sleep(2) # Give parent time to exit
        new_ppid = os.getppid()
        print(f"  Orphan Child: My original parent died. My new parent is {new_ppid} (init/systemd).")
        os._exit(0)
    else:
        # Parent exits immediately
        print(f"  Parent (PID:{os.getpid()}): Exiting before my child.")
        time.sleep(0.1) # A small delay to ensure the child's first print happens
        # We can't use os._exit() here as it would terminate the whole script.

    # Wait for the orphan child to finish its demonstration before moving on
    time.sleep(3)
    print("\nParent: Orphan simulation complete.")
    print("-" * 50)


# --- Task 4: Inspecting Process Info from /proc ---
def task_4_inspect_proc(pid_to_inspect):
    """
    Reads and prints information about a process from the /proc filesystem.
    [cite_start][cite: 43]
    """
    print(f"\n--- Task 4: Inspecting Process PID {pid_to_inspect} from /proc ---")
    proc_dir = f"/proc/{pid_to_inspect}"
    
    if not os.path.exists(proc_dir):
        print(f"  Error: Process with PID {pid_to_inspect} not found.")
        return

    try:
        # Read from /proc/[pid]/status
        with open(os.path.join(proc_dir, 'status'), 'r') as f:
            for line in f:
                if line.startswith(('Name:', 'State:', 'VmSize:')):
                    print(f"  {line.strip()}")
                    
        # Read executable path from /proc/[pid]/exe
        exe_path = os.readlink(os.path.join(proc_dir, 'exe'))
        print(f"  Executable Path: {exe_path}")

        # List open file descriptors from /proc/[pid]/fd
        fd_dir = os.path.join(proc_dir, 'fd')
        open_files = os.listdir(fd_dir)
        print(f"  Open File Descriptors: {len(open_files)}")

    except (PermissionError, FileNotFoundError) as e:
        print(f"  Could not read full info for PID {pid_to_inspect}: {e}")
    finally:
        print("-" * 50)


# --- Task 5: Process Prioritization ---
def cpu_intensive_work(label):
    """A simple task that consumes CPU time."""
    start_time = time.time()
    print(f"  {label} (PID:{os.getpid()}, Nice:{os.nice(0)}): Starting CPU work.")
    # A simple, inefficient loop to burn CPU cycles
    count = 0
    for _ in range(250_000_000):
        count += 1
    end_time = time.time()
    print(f"  {label}: Finished in {end_time - start_time:.2f} seconds.")


def task_5_process_prioritization():
    """
    Demonstrates process priority by overloading the CPU with more
    processes than available cores.
    """
    print("\n--- Task 5: Demonstrating Process Prioritization (CPU Overload) ---")
    
    try:
        num_cores = os.cpu_count()
        print(f"  Detected {num_cores} CPU cores. Creating {num_cores * 2} processes to ensure competition.")
    except NotImplementedError:
        num_cores = 4 # Fallback for some systems
        print(f"  Could not detect CPU cores. Defaulting to creating {num_cores * 2} processes.")

    num_processes = num_cores * 2
    child_pids = []

    print("  Starting a mix of default-priority and low-priority children...")

    for i in range(num_processes):
        pid = os.fork()
        if pid == 0:
            # Child Process Logic
            if i % 2 == 0:
                # Even-numbered children get default priority
                os.nice(0)
                cpu_intensive_work(f"Default Priority-{i//2}")
            else:
                # Odd-numbered children get low priority
                os.nice(15) # Using 15 for a more pronounced effect
                cpu_intensive_work(f"Low Priority-{i//2}")
            os._exit(0)
        else:
            # Parent Process Logic
            child_pids.append(pid)

    # Parent waits for all children to finish
    for pid in child_pids:
        os.waitpid(pid, 0)

    print("\nParent: All CPU-intensive children have finished.")
    print("Observe the finish times: the 'Default Priority' processes should have generally finished earlier than the 'Low Priority' ones.")
    print("-" * 50)
    

# --- Main Execution ---
def main():
    """Main function to run all the OS lab tasks."""
    print("====== Operating System Lab Assignment 1 ======")
    task_1_process_creation()
    task_2_command_execution()
    task_3_zombie_and_orphan()
    
    # For Task 4, we inspect the main script's own process ID
    task_4_inspect_proc(os.getpid())
    
    task_5_process_prioritization()
    print("\n======== All Tasks Completed ========")


if __name__ == "__main__":
    main()