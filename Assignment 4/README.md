OS Lab Assignment 4: System Calls & File System Simulation (Interactive)

Description

This project is a Python-based simulation tool developed for the Operating Systems Laboratory (Lab Sheet 4). It demonstrates how to interact with the operating system kernel using Python's standard libraries (os, platform, subprocess, shutil).

The script provides an interactive command-line interface (CLI) where users can manually select specific tasks to retrieve system information, manage processes, detect virtual environments, and perform file system operations.

Features Implemented

The tool implements the following five tasks, selectable via a main menu:

1. Process Information & System Calls

Retrieves the Process ID (PID) and Parent Process ID (PPID).

Displays the current working directory.

Simulates the creation of a child process using subprocess.

2. System Statistics

Fetches low-level system details using the platform module.

Displays OS Name, Release Version, Machine Architecture, and Processor details.

3. Virtual Machine (VM) Detection

Analyzes the system's MAC Address OUI (Organizationally Unique Identifier) to detect common hypervisors (VMware, VirtualBox, Parallels).

On Linux systems, it checks specific system files (like /sys/class/dmi/) for hypervisor signatures.

4. File System Operations

Demonstrates programmatic Create, Read, Update, and Delete (CRUD) operations.

Creates a test directory and file, writes content, renames the file, and performs cleanup.

5. Recursive Directory Traversal

Simulates the functionality of the ls -R or tree command.

Recursively walks through a directory structure and lists all subdirectories and files.

Prerequisites

OS: Windows, Linux, or macOS.

Python: Version 3.x or higher.

How to Run

Save the simulation script as os_lab_4_simulation.py.

Open a terminal or command prompt.

Run the script:

python os_lab_4_simulation.py


The script will enter an interactive loop. Enter a number (1-6) from the menu to execute a specific task or '0' to exit.

Usage Example

Upon execution, the following menu is displayed:

========================================
   OS LAB 4: SYSTEM CALLS & VM DETECTION
========================================
1. Process Info (Task 1)
2. System Stats (Task 2)
3. VM Detection (Task 3)
4. File Ops Simulation (Task 4)
5. Directory Walk (Task 5)
6. Run All Tasks
0. Exit

Enter Choice: 


Logging

The script automatically logs key activities (like process creation and file modifications) to a local file named system_log.txt with timestamps.