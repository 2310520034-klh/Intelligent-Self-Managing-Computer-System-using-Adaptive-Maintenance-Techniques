import psutil
import platform
import os
import shutil
import time
from datetime import datetime

# ---------------------------
# SYSTEM INFORMATION
# ---------------------------
def get_system_info():
    print("\n🖥️ SYSTEM INFORMATION")
    print("OS:", platform.system(), platform.release())
    print("Processor:", platform.processor())
    print("Machine:", platform.machine())
    print("CPU Cores:", psutil.cpu_count(logical=False), "Physical /", psutil.cpu_count(), "Logical")
    print("RAM:", round(psutil.virtual_memory().total / (1024**3),2), "GB")

# ---------------------------
# PERFORMANCE MONITORING
# ---------------------------
def check_performance():
    print("\n📊 PERFORMANCE STATUS")

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    print("CPU Usage:", cpu,"%")
    print("Memory Usage:", memory,"%")
    print("Disk Usage:", disk,"%")

    issues = []

    if cpu > 85:
        issues.append("High CPU Usage")

    if memory > 80:
        issues.append("High Memory Usage")

    if disk > 90:
        issues.append("Low Disk Space")

    return issues

# ---------------------------
# PROCESS MONITORING
# ---------------------------
def check_heavy_processes():
    print("\n⚙️ PROCESS MONITOR")

    for proc in psutil.process_iter(['pid','name','cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 80:
                print("⚠️ High CPU Process:",proc.info['name'],
                      "CPU:",proc.info['cpu_percent'],"%")
        except:
            pass

# ---------------------------
# DISK HEALTH CHECK
# ---------------------------
def check_disk_health():
    print("\n💾 DISK HEALTH")

    partitions = psutil.disk_partitions()

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            print("Drive:", partition.device)
            print("Used:", usage.percent,"%")
        except:
            pass

# ---------------------------
# NETWORK MONITORING
# ---------------------------
def check_network():
    print("\n🌐 NETWORK STATUS")

    net = psutil.net_io_counters()

    print("Bytes Sent:", net.bytes_sent)
    print("Bytes Received:", net.bytes_recv)

# ---------------------------
# BATTERY STATUS
# ---------------------------
def check_battery():
    print("\n🔋 BATTERY STATUS")

    battery = psutil.sensors_battery()

    if battery:
        print("Battery:", battery.percent,"%")
        print("Charging:", battery.power_plugged)

        if battery.percent < 25 and not battery.power_plugged:
            print("⚠️ Battery Low!")
    else:
        print("No Battery Detected")

# ---------------------------
# TEMPERATURE MONITOR
# ---------------------------
def check_temperature():
    print("\n🌡️ TEMPERATURE STATUS")

    temps = psutil.sensors_temperatures()

    if temps:
        for name,entries in temps.items():
            for entry in entries:
                print(name,":",entry.current,"°C")
    else:
        print("Temperature sensors not available")

# ---------------------------
# CLEAN TEMP FILES
# ---------------------------
def cleanup_temp_files():
    print("\n🧹 CLEANING TEMP FILES")

    temp = os.getenv("TEMP") or "/tmp"

    try:
        before = len(os.listdir(temp))

        shutil.rmtree(temp, ignore_errors=True)
        os.makedirs(temp, exist_ok=True)

        print("Removed", before,"temporary files")
    except Exception as e:
        print("Cleanup failed:", e)

# ---------------------------
# SYSTEM LOG
# ---------------------------
def log_system_status():
    with open("system_log.txt","a") as f:
        f.write("System checked at "+str(datetime.now())+"\n")

# ---------------------------
# REPORT GENERATION
# ---------------------------
def generate_report(issues):

    filename = "System_Report_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".txt"

    with open(filename,"w") as f:

        f.write("SYSTEM DIAGNOSTIC REPORT\n")
        f.write("Generated at: "+str(datetime.now())+"\n\n")

        f.write("Detected Issues:\n")

        if issues:
            for i in issues:
                f.write("- "+i+"\n")
        else:
            f.write("No major issues detected\n")

    print("\nReport saved as",filename)

# ---------------------------
# MAIN PROGRAM
# ---------------------------
def main():

    print("🔧 INTELLIGENT SELF-MANAGING SYSTEM 🔧")

    get_system_info()

    issues = check_performance()

    check_heavy_processes()

    check_disk_health()

    check_network()

    check_battery()

    check_temperature()

    cleanup_temp_files()

    generate_report(issues)

    log_system_status()

    print("\n✅ System Diagnostics Completed")

if __name__ == "__main__":
    main()
