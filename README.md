# OS Lab Assignment 1: Process Management in Python

This repository contains the solution for the "Process Creation and Management" lab experiment for the ENCS351 Operating System course. The project uses Python's `os` module to simulate fundamental process management operations in a Linux environment.

## Description

The core of this project is a Python script, `process_management.py`, which demonstrates the lifecycle and management of system processes. It provides practical implementations of concepts such as process creation with `os.fork()`, command execution with `os.execvp()`, and process state inspection using the `/proc` filesystem. The script is organized into functions, with each function addressing a specific task from the lab assignment.

## Tasks Covered

The script successfully implements the following five tasks:

1.  **Process Creation Utility:** Creates a user-specified number of child processes, demonstrating the parent-child relationship and process termination synchronization using `os.wait()`.
2.  **Command Execution:** Utilizes the `fork-exec` model to have child processes execute standard Linux commands like `ls`, `date`, and `ps`.
3.  **Zombie & Orphan Processes:** Simulates the conditions required to create both "defunct" (zombie) and orphan processes to understand process lifecycle states.
4.  **Process Inspection:** Reads and parses data from the `/proc` virtual filesystem to display details about a running process, such as its name, state, memory usage, and open file descriptors.
5.  **Process Prioritization:** Demonstrates the effect of `nice()` values on the Linux process scheduler by creating a CPU-bound scenario with more processes than available cores, showing that higher-priority processes are favored.

## Requirements

* A Linux-based environment (e.g., Ubuntu, Debian, or Windows Subsystem for Linux - WSL).
* Python 3.x

## How to Run

1.  Clone the repository to your local machine:
    ```bash
    git clone https://github.com/theabhinav0231/OS-Lab
    ```
2.  Navigate into the project directory:
    ```bash
    cd OS-Lab
    ```
3.  Execute the main script using Python 3:
    ```bash
    python3 process_management.py
    ```
4.  To run the Process Prioritization task (Task 5) with the ability to set higher priorities (negative `nice` values), you must run the script with administrator privileges:
    ```bash
    sudo python3 process_management.py
    ```

## Files in this Repository

* **`process_management.py`**: The main Python script containing the source code for all five tasks.
* **`output.txt`**: A sample output file generated from a successful run of the script.
* **`report.pdf`**: A detailed lab report summarizing the objectives, implementation, code snapshots, results, and complexity analysis.
* **`README.md`**: This file, providing an overview and instructions for the project.
