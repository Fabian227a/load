import psutil
import argparse
import time

def get_cpu_avg_load():
    try:
        load_avg_1min, load_avg_5min, load_avg_15min = psutil.getloadavg()
        return load_avg_1min, load_avg_5min, load_avg_15min
    except Exception as e:
        print(f"Error in get_cpu_avg_load: {e}")
        return (0, 0, 0)  # Default-Werte zurückgeben oder einen anderen Platzhalterwert verwenden

def get_cpu_load():
    try:
        cpu_load = psutil.cpu_percent(interval=1)
        return cpu_load
    except Exception as e:
        print(f"Error in get_cpu_load: {e}")
        return None

def print_cpu_status(cpu_load, cpu_avg, warnings, criticals):
    print(f"Current CPU Load is {cpu_load}%")

    if cpu_avg is not None and all(isinstance(avg, (int, float)) for avg in cpu_avg):
        if warnings is not None and criticals is not None:
            if len(criticals) == 3 and len(warnings) == 3:
                if any(avg > crit for avg, crit in zip(cpu_avg, criticals)):
                    print(f"CRITICAL - 1 min: {cpu_avg[0]} | 5 min: {cpu_avg[1]} | 15 min: {cpu_avg[2]}")
                elif any(warn < avg < crit for avg, warn, crit in zip(cpu_avg, warnings, criticals)):
                    print(f"WARNING - 1 min: {cpu_avg[0]} | 5 min: {cpu_avg[1]} | 15 min: {cpu_avg[2]}")
                else:
                    print(f"OK - 1 min: {cpu_avg[0]} | 5 min: {cpu_avg[1]} | 15 min: {cpu_avg[2]}")
            else:
                print("Invalid number of values in warnings or criticals.")
        else:
            print("Warnings or criticals are None.")
    else:
        print("Invalid values in CPU average load or unable to retrieve CPU average load.")

def main():
    parser = argparse.ArgumentParser(description='Monitor CPU Load on a Linux System.')
    parser.add_argument('-w', '--warnings', nargs=3, type=float, default=[0.9, 0.8, 0.7], help='CPU usage warning values (provide 3 values)')
    parser.add_argument('-c', '--criticals', nargs=3, type=float, default=[0.95, 0.85, 0.75], help='CPU usage critical values (provide 3 values)')
    parser.add_argument('-i', '--interval', type=int, default=10, help='Interval for checking CPU Load in seconds.')
    args = parser.parse_args()

    interval = args.interval
    warnings = args.warnings
    criticals = args.criticals

    try:
        while True:
            cpu_avg = get_cpu_avg_load()
            cpu_load = get_cpu_load()
            print_cpu_status(cpu_load, cpu_avg, warnings, criticals)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    main()