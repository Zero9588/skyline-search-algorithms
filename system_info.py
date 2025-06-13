import platform
import sys
import os
import psutil

def print_system_info():
    print("\n🔍 System Information")
    
    # Language and Python
    print(f"Programming language: Python")
    print(f"Python version: Python {platform.python_version()}")
    
    # OS and Kernel
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    print(f"OS: {system} {machine}")
    print(f"Kernel: {release}")

    # Shell (best-effort, fallback to environment)
    shell_path = os.environ.get("SHELL") or os.environ.get("COMSPEC") or "Unknown"
    shell_name = os.path.basename(shell_path)
    print(f"Shell: {shell_name}")

    # CPU info
    cpu = platform.processor()
    if not cpu and system == "Darwin":
        cpu = os.popen("sysctl -n machdep.cpu.brand_string").read().strip()
    print(f"CPU: {cpu if cpu else 'Unknown'}")

    # Memory usage
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    used = (mem.total - mem.available) / (1024 ** 3)
    percent = mem.percent
    print(f"Memory: {used:.2f}GiB / {total:.2f}GiB ({percent}%)")

print_system_info()