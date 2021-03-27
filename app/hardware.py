import psutil
import subprocess as sp
    
def cpu():
    cpu_count = len(psutil.Process().cpu_affinity())
    cmd = "top -bn 2 -d 0.5| sed -nE '/(yagna|ya-provider|vmrt)/ p' | awk '{ print $9 }' | awk '{ for(i=0; i<NF; i++) j+=$i; } END {print j/2}'"
    try:
        usage = float(sp.check_output(cmd, shell=True).decode())
        percent_usage = usage / cpu_count
    except:
        print('hardware: Failed to execute ', cmd)
        print('hardware: Defaulting back to psutil')
        percent_usage = psutil.cpu_percent(interval=1)
    return {
        "percentUsage": percent_usage,
    }

def memory():
    available = psutil.virtual_memory().available

    try: 
        used = sp.check_output(\
            'cat /sys/fs/cgroup/memory/memory.usage_in_bytes', \
            shell=True \
        )
        used = int(used)
    except:
        used = psutil.virtual_memory().used
    
    return {
        "available": available,
        "used": used,
        "percent" : round(used/(used+available) * 100),
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
