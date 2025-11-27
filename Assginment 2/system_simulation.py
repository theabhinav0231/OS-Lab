import multiprocessing
import logging
import time

# -------------------------------
# Sub-Task 1: Initialize Logging
# -------------------------------
logging.basicConfig(
    filename='process_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)

# -----------------------------------------------
# Sub-Task 2: Define a dummy system process task
# -----------------------------------------------
def system_process(task_name):
    logging.info(f"{task_name} started")
    time.sleep(2)   # simulate work
    logging.info(f"{task_name} ended")

# -----------------------------------------------
# Sub-Task 3 & 4: Create, start, join processes
# -----------------------------------------------
if __name__ == '__main__':
    print("System Starting...")

    # Create at least two processes
    p1 = multiprocessing.Process(target=system_process, args=('Process-1',))
    p2 = multiprocessing.Process(target=system_process, args=('Process-2',))

    # Start processes
    p1.start()
    p2.start()

    # Wait for processes to finish
    p1.join()
    p2.join()

    print("System Shutdown.")