import random
import time

# ==========================================
# PART 1: CPU SCHEDULING ALGORITHMS
# ==========================================

def priority_scheduling():
    """
    Simulates Non-Preemptive Priority Scheduling.
    Lower number implies higher priority (standard convention).
    """
    print("\n--- Priority Scheduling (Non-Preemptive) ---")
    try:
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            print(f"\nProcess {i+1}:")
            arrival = int(input("  Arrival Time: "))
            burst = int(input("  Burst Time: "))
            priority = int(input("  Priority (1 is highest): "))
            # Store as [ID, Arrival, Burst, Priority, Waiting, Turnaround, Completion]
            processes.append({'id': i+1, 'at': arrival, 'bt': burst, 'p': priority, 'wt': 0, 'tat': 0, 'ct': 0})
        
        # Sort by Arrival Time, then Priority
        # Note: In a real simulation, we'd manage a ready queue based on time. 
        # For this lab simulation, we'll sort primarily by priority for simplicity 
        # assuming all arrive at 0 or handling a simple queue.
        # Let's do a proper time-step simulation.
        
        processes.sort(key=lambda x: x['at']) # Initial sort by arrival
        
        completed = 0
        current_time = 0
        avg_wt = 0
        avg_tat = 0
        is_completed = [False] * n
        result_sequence = []

        while completed < n:
            # Find processes that have arrived and are not completed
            available_processes = []
            for i in range(n):
                if processes[i]['at'] <= current_time and not is_completed[i]:
                    available_processes.append((processes[i]['p'], i)) # (Priority, Index)
            
            if available_processes:
                # Select process with highest priority (lowest number)
                available_processes.sort() 
                _, idx = available_processes[0]
                
                # Execute process
                p = processes[idx]
                current_time += p['bt']
                p['ct'] = current_time
                p['tat'] = p['ct'] - p['at']
                p['wt'] = p['tat'] - p['bt']
                
                avg_wt += p['wt']
                avg_tat += p['tat']
                is_completed[idx] = True
                completed += 1
                result_sequence.append(p['id'])
            else:
                current_time += 1

        print("\nProcess Execution Order:", " -> ".join(map(str, result_sequence)))
        print(f"\n{'ID':<5}{'Priority':<10}{'Arrival':<10}{'Burst':<10}{'Wait':<10}{'Turnaround':<10}")
        for p in processes:
            print(f"{p['id']:<5}{p['p']:<10}{p['at']:<10}{p['bt']:<10}{p['wt']:<10}{p['tat']:<10}")
            
        print(f"\nAverage Waiting Time: {avg_wt/n:.2f}")
        print(f"Average Turnaround Time: {avg_tat/n:.2f}")

    except ValueError:
        print("Invalid input. Please enter integers.")

def round_robin_scheduling():
    """
    Simulates Round Robin Scheduling with a Time Quantum.
    """
    print("\n--- Round Robin Scheduling ---")
    try:
        n = int(input("Enter number of processes: "))
        time_quantum = int(input("Enter Time Quantum: "))
        processes = []
        for i in range(n):
            print(f"Process {i+1}:")
            burst = int(input("  Burst Time: "))
            # For simplicity in this lab version, assuming all arrive at t=0
            processes.append({'id': i+1, 'bt': burst, 'rem_bt': burst, 'wt': 0, 'tat': 0})
        
        current_time = 0
        queue = processes[:] # All processes in queue initially (Arrival Time = 0)
        completed_list = []
        
        while any(p['rem_bt'] > 0 for p in processes):
            done_something = False
            for p in processes:
                if p['rem_bt'] > 0:
                    done_something = True
                    if p['rem_bt'] > time_quantum:
                        current_time += time_quantum
                        p['rem_bt'] -= time_quantum
                    else:
                        current_time += p['rem_bt']
                        p['wt'] = current_time - p['bt']
                        p['rem_bt'] = 0
                        p['tat'] = current_time
            if not done_something:
                break

        print(f"\n{'ID':<5}{'Burst':<10}{'Wait':<10}{'Turnaround':<10}")
        avg_wt = 0
        avg_tat = 0
        for p in processes:
            print(f"{p['id']:<5}{p['bt']:<10}{p['wt']:<10}{p['tat']:<10}")
            avg_wt += p['wt']
            avg_tat += p['tat']
        
        print(f"\nAverage Waiting Time: {avg_wt/n:.2f}")
        print(f"Average Turnaround Time: {avg_tat/n:.2f}")

    except ValueError:
        print("Invalid input.")

# ==========================================
# PART 2: FILE ALLOCATION STRATEGIES
# ==========================================

def sequential_allocation():
    """
    Simulates Sequential File Allocation.
    """
    print("\n--- Sequential File Allocation ---")
    total_blocks = 50
    disk = [0] * total_blocks # 0 = free, 1 = allocated
    files = {}

    while True:
        print(f"\nDisk Status (Total: {total_blocks} blocks): {disk.count(0)} free")
        choice = input("1. Allocate File\n2. Show Files\n3. Exit to Main Menu\nChoice: ")
        
        if choice == '1':
            name = input("Enter file name: ")
            try:
                start = int(input(f"Enter starting block (0-{total_blocks-1}): "))
                length = int(input("Enter length of file: "))
                
                if start + length > total_blocks:
                    print("Error: File exceeds disk bounds.")
                    continue
                
                # Check if blocks are free
                is_free = True
                for i in range(start, start + length):
                    if disk[i] == 1:
                        is_free = False
                        break
                
                if is_free:
                    for i in range(start, start + length):
                        disk[i] = 1
                    files[name] = (start, length)
                    print(f"File '{name}' allocated successfully at blocks {start} to {start+length-1}.")
                else:
                    print("Error: Blocks already allocated.")
            except ValueError:
                print("Invalid input.")

        elif choice == '2':
            print("\nAllocated Files:")
            for name, (start, length) in files.items():
                print(f"File: {name} | Start: {start} | Length: {length}")
        
        elif choice == '3':
            break

def indexed_allocation():
    """
    Simulates Indexed File Allocation.
    """
    print("\n--- Indexed File Allocation ---")
    total_blocks = 50
    disk = [0] * total_blocks
    # Randomly occupy some blocks to make it realistic
    for i in range(10):
        disk[random.randint(0, 49)] = 1
        
    print(f"Disk initialized with {disk.count(1)} used blocks (random).")
    
    while True:
        choice = input("\n1. Create File\n2. Exit to Main Menu\nChoice: ")
        if choice == '1':
            name = input("Enter file name: ")
            try:
                size = int(input("Enter file size (in blocks): "))
                free_blocks = [i for i, x in enumerate(disk) if x == 0]
                
                # We need size + 1 blocks (1 for index block)
                if len(free_blocks) < size + 1:
                    print("Error: Not enough memory.")
                    continue
                
                index_block = free_blocks[0]
                disk[index_block] = 1
                allocated_blocks = []
                
                # Allocate data blocks randomly from remaining free blocks
                for i in range(size):
                    block = free_blocks[i+1] # Skip the one we used for index
                    disk[block] = 1
                    allocated_blocks.append(block)
                
                print(f"\nFile '{name}' Allocated.")
                print(f"Index Block: {index_block}")
                print(f"Data Blocks pointers in Index Block: {allocated_blocks}")
                
            except ValueError:
                print("Invalid input.")
        elif choice == '2':
            break

# ==========================================
# PART 3: MEMORY MANAGEMENT (CONTIGUOUS)
# ==========================================

def memory_allocation_simulation():
    """
    Simulates First-Fit, Best-Fit, and Worst-Fit.
    """
    print("\n--- Contiguous Memory Allocation ---")
    try:
        # Initial Memory State
        block_sizes = [100, 500, 200, 300, 600]
        print(f"Available Memory Blocks: {block_sizes}")
        
        n_proc = int(input("Enter number of processes: "))
        process_sizes = []
        for i in range(n_proc):
            process_sizes.append(int(input(f"Enter memory for Process {i+1}: ")))

        print("\nSelect Strategy:")
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")
        strat = input("Choice: ")
        
        allocation = [-1] * n_proc # Stores block index for each process
        
        # We work on a copy of blocks for the simulation
        blocks = block_sizes.copy()

        for i in range(n_proc):
            p_size = process_sizes[i]
            best_idx = -1
            
            if strat == '1': # First Fit
                for j in range(len(blocks)):
                    if blocks[j] >= p_size:
                        best_idx = j
                        break
                        
            elif strat == '2': # Best Fit
                for j in range(len(blocks)):
                    if blocks[j] >= p_size:
                        if best_idx == -1 or blocks[j] < blocks[best_idx]:
                            best_idx = j
                            
            elif strat == '3': # Worst Fit
                for j in range(len(blocks)):
                    if blocks[j] >= p_size:
                        if best_idx == -1 or blocks[j] > blocks[best_idx]:
                            best_idx = j
            
            if best_idx != -1:
                allocation[i] = best_idx
                blocks[best_idx] -= p_size # Reduce available memory in block
            
        print(f"\n{'Process No.':<15}{'Process Size':<15}{'Block No.':<15}{'Block Initial Size'}")
        for i in range(n_proc):
            blk_no = allocation[i] + 1 if allocation[i] != -1 else "Not Allocated"
            orig_size = block_sizes[allocation[i]] if allocation[i] != -1 else "-"
            print(f"{i+1:<15}{process_sizes[i]:<15}{blk_no:<15}{orig_size}")

    except ValueError:
        print("Invalid input.")

# ==========================================
# PART 4: MFT & MVT
# ==========================================

def mft_mvt_simulation():
    """
    Simulates MFT (Fixed Partition) and MVT (Variable Partition).
    """
    print("\n--- MFT / MVT Simulation ---")
    print("1. MFT (Multiprogramming with Fixed Tasks)")
    print("2. MVT (Multiprogramming with Variable Tasks)")
    choice = input("Choice: ")
    
    try:
        total_memory = int(input("Enter Total Memory Size (e.g. 1000): "))
        
        if choice == '1': # MFT
            block_size = int(input("Enter Block Size (Fixed): "))
            num_blocks = total_memory // block_size
            external_frag_initial = total_memory - (num_blocks * block_size)
            
            print(f"\nTotal Blocks Created: {num_blocks}")
            print(f"Initial External Fragmentation (Unusable): {external_frag_initial}")
            
            n_proc = int(input("Enter number of processes: "))
            internal_frag_total = 0
            processes_alloc = 0
            
            print(f"\n{'Process':<10}{'Memory Req':<15}{'Allocated':<15}{'Internal Frag':<15}")
            
            for i in range(n_proc):
                mem_req = int(input(f"Memory for Process {i+1}: "))
                if processes_alloc < num_blocks:
                    if mem_req <= block_size:
                        frag = block_size - mem_req
                        internal_frag_total += frag
                        processes_alloc += 1
                        print(f"{i+1:<10}{mem_req:<15}{'YES':<15}{frag:<15}")
                    else:
                         print(f"{i+1:<10}{mem_req:<15}{'NO (Too Big)':<15}{'-':<15}")
                else:
                    print(f"{i+1:<10}{mem_req:<15}{'NO (Full)':<15}{'-':<15}")
            
            print(f"\nTotal Internal Fragmentation: {internal_frag_total}")

        elif choice == '2': # MVT
            current_mem = total_memory
            n = 0
            processes = []
            
            while True:
                mem_req = int(input(f"\nEnter memory for Process {n+1}: "))
                if mem_req <= current_mem:
                    print(f"Memory allocated for Process {n+1}")
                    current_mem -= mem_req
                    processes.append((n+1, mem_req))
                    n += 1
                else:
                    print("Memory is Full / Not enough space.")
                
                cont = input("Add another process? (y/n): ")
                if cont.lower() != 'y':
                    break
            
            print(f"\nTotal Memory: {total_memory}")
            print(f"Total Allocated: {total_memory - current_mem}")
            print(f"Total External Fragmentation (Remaining): {current_mem}")

    except ValueError:
        print("Invalid input.")

# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================

def main():
    while True:
        print("\n==========================================")
        print("   OS LAB ASSIGNMENT SIMULATION TOOL")
        print("==========================================")
        print("1. Priority Scheduling")
        print("2. Round Robin Scheduling")
        print("3. Sequential File Allocation")
        print("4. Indexed File Allocation")
        print("5. Memory Allocation (First/Best/Worst Fit)")
        print("6. MFT / MVT Simulation")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            priority_scheduling()
        elif choice == '2':
            round_robin_scheduling()
        elif choice == '3':
            sequential_allocation()
        elif choice == '4':
            indexed_allocation()
        elif choice == '5':
            memory_allocation_simulation()
        elif choice == '6':
            mft_mvt_simulation()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()