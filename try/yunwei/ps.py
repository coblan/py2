import psutil
mem=psutil.virtual_memory()
print(mem.total,mem.used)
ss = psutil.cpu_times()
print(ss)