import psutil
import subprocess as sp
    
def cpu():
    # cpu_count = len(psutil.Process().cpu_affinity())
    percent_usage = psutil.cpu_percent(interval=1)
    return {
        "percentUsage": round(percent_usage),
        # "percentUsagePerCore": psutil.cpu_percent(percpu=True),
    }

def memory():
    available = psutil.virtual_memory().available
    used = psutil.virtual_memory().used
    return {
        "available": available,
        "used": used,
        "percent" : round(used/(used+available), 1),
    }

def isProcessingTask():
    '''
    Use the Process "vmrt" as an indicator as to whether a process is running
    or not. Saw it taking over 800% cpu in top so I'm assuming that's the
    process the tasks are running in.
    '''
    return _isProcessRunning('vmrt')

def _isProcessRunning(processName):
    try:
        sp.check_output("pidof '{}'".format(processName), shell=True)
        return True
    except sp.CalledProcessError:
        return False
