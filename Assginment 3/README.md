OS Lab Assignment Simulation Tool

Description

This project is a comprehensive Python-based simulation tool developed for the Operating Systems Laboratory (CS351). It integrates multiple OS concepts into a single interactive application, allowing users to experiment with various scheduling algorithms, file allocation strategies, and memory management techniques.

The tool provides a menu-driven interface to visualize and calculate results for different operating system algorithms without needing separate scripts for each task.

Features Implemented

1. CPU Scheduling Algorithms

Priority Scheduling (Non-Preemptive): Schedules processes based on priority values (lower value = higher priority). Calculates Waiting Time and Turnaround Time.

Round Robin Scheduling: Simulates time-sharing systems using a configurable Time Quantum.

2. File Allocation Strategies

Sequential File Allocation: Simulates contiguous storage allocation on a disk. Handles boundary checks and collision detection.

Indexed File Allocation: Simulates non-contiguous allocation using an index block to store pointers to data blocks.

3. Memory Management (Contiguous)

Allocation Strategies: Implements First Fit, Best Fit, and Worst Fit algorithms to allocate variable-sized processes into fixed memory blocks.

4. Memory Management (Partitioning)

MFT (Multiprogramming with a Fixed number of Tasks): Simulates fixed partitioning and calculates Internal Fragmentation.

MVT (Multiprogramming with a Variable number of Tasks): Simulates dynamic partitioning and calculates External Fragmentation.

Prerequisites

Python 3.x

How to Run

Ensure you have Python installed on your system.

Save the simulation script as os_lab_simulation.py.

Open a terminal or command prompt.

Run the following command:

python os_lab_simulation.py


Follow the on-screen interactive menu to select an algorithm and input data.

Usage Example

Upon running the script, you will see a main menu:

==========================================
   OS LAB ASSIGNMENT SIMULATION TOOL
==========================================
1. Priority Scheduling
2. Round Robin Scheduling
3. Sequential File Allocation
4. Indexed File Allocation
5. Memory Allocation (First/Best/Worst Fit)
6. MFT / MVT Simulation
0. Exit
...


Enter the number corresponding to the simulation you wish to run.