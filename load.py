import psutil
#import os
import argparse
import time

def get_cpu_avg_load():
    try:
        # Run the uptime command and capture its output

        # Windows
        load_avg_1min, load_avg_5min, load_avg_15min = psutil.getloadavg()

        # Linux
        # Get the load averages for 1, 5, and 15 minutes
        # load_avg_1min, load_avg_5min, load_avg_15min = os.getloadavg()

        return load_avg_1min, load_avg_5min, load_avg_15min
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_cpu_load():
    try:
        cpu_load = psutil.cpu_percent(interval=1)
        return cpu_load
    except Exception as e:
        print(f"Error: {e}")
        return None

def print_cpu_status(cpu_load, cpu_avg, warnings=[0.9, 0.8, 0.7], criticals=[0.95, 0.85, 0.75]):
    print(f"Current CPU Load is {cpu_load}%")



    if (cpu_avg[0] > criticals[0]) or (cpu_avg[1] > criticals[1]) or (cpu_avg[2] > criticals[2]):
        print("CRITICAL - 1 min: " + str(cpu_avg[0]) + " | 3 min: " + str(cpu_avg[1]) + " | 5 min: " + str(cpu_avg[2]))
    elif ((cpu_avg[0] > warnings[0]) and (cpu_avg[0] < criticals[0])) or ((cpu_avg[1] > warnings[1]) and (cpu_avg[1] < criticals[1])) or ((cpu_avg[2] > warnings [2]) and (cpu_avg[2] < criticals[2])):
        print("WARNING - 1 min: " + str(cpu_avg[0]) + " | 3 min: " + str(cpu_avg[1]) + " | 5 min: " + str(cpu_avg[2]))
    else:
        print("OK - 1 min: " + str(cpu_avg[0]) + " | 3 min: " + str(cpu_avg[1]) + " | 5 min: " + str(cpu_avg[2]))

def main():
    parser = argparse.ArgumentParser(description='Monitor CPU Load on a Linux System.')

    # Add command-line arguments
    parser.add_argument('-w', '--warnings', nargs=3, type=float, help='CPU usage warning values (provide 3 values)')
    parser.add_argument('-c', '--criticals', nargs=3, type=float, help='CPU usage critical values (provide 3 values)')
    parser.add_argument('-i', '--interval', type=int, default=10, help='Interval for checking CPU Load in seconds.')
    args = parser.parse_args()

    print("start")
    print("interval in seconds")
    interval = args.interval
    print(interval)

    print("warning levels")
    warnings = args.warnings
    print(warnings)

    print("critical levels")
    criticals = args.criticals
    print(criticals)

    try:
        while True:
            cpu_avg = get_cpu_avg_load()
            cpu_load = get_cpu_load()
            print_cpu_status(cpu_load, cpu_avg, warnings, criticals)
            #print(f"Status: {status} - {message}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    main()
