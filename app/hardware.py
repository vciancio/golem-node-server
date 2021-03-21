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