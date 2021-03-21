import psutil

def cpu():
    return {
        "percentUsage": psutil.cpu_percent(),
        "percentUsagePerCore": psutil.cpu_percent(percpu=True),
    }

def memory():
    mem = psutil.virtual_memory()
    return {
        "available": mem.available,
        "used": mem.used,
        "percent" : mem.percent,
    }

def isProcessingTask():
    '''
    Use the Process "vmrt" as an indicator as to whether a process is running
    or not. Saw it taking over 800% cpu in top so I'm assuming that's the
    process the tasks are running in.
    '''
    return _isProcessRunning('vmrt')

def _isProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False