#!/usr/bin/env python3

import os
import sys
import argparse


def check_load(warnings, criticals):
  try:
    load_avg = os.getloadavg()

    if (load_avg[0] > criticals[0]) or (load_avg[1] > criticals[1]) or (load_avg[2] > criticals[2]):
      # print("CRITICAL - 1 min: " + str(load_avg[0]) + " | 3 min: " + str(load_avg[1]) + " | 5 min: " + str(load_avg[2]))
      print(f"CRITICAL - custom load average: {load_avg[0]}, {load_avg[1]}, {load_avg[2]}")
      sys.exit(2)

    elif ((load_avg[0] > warnings[0]) and (load_avg[0] < criticals[0])) or ((load_avg[1] > warnings[1]) and (load_avg[1] < criticals[1])) or ((load_avg[2] > warnings [2]) and (load_avg[2] < criticals[2])):
      # print("WARNING - 1 min: " + str(load_avg[0]) + " | 3 min: " + str(load_avg[1]) + " | 5 min: " + str(load_avg[2]))
      print(f"WARNING - custom load average: {load_avg[0]}, {load_avg[1]}, {load_avg[2]}")
      sys.exit(1)

    else:
      # print("OK - 1 min: " + str(load_avg[0]) + " | 3 min: " + str(load_avg[1]) + " | 5 min: " + str(load_avg[2]))
      print(f"OK - custom load average: {load_avg[0]}, {load_avg[1]}, {load_avg[2]}")
      sys.exit(0)

  except Exception as e:
    print(f"UNKNOWN - An error occured: {e}")
    sys.exit(3)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Monitor CPU Load on a Linux System.')

  # Add command-line arguments
  parser.add_argument('-w', '--warnings', nargs=3, type=float, default=[0.9, 0.8, 0.7], help='CPU usage warning values (provide 3 values)')
  parser.add_argument('-c', '--criticals', nargs=3, type=float, default=[0.95, 0.85, 0.75], help='CPU usage critical values (provide 3 values)')
  args = parser.parse_args()

  warnings = args.warnings
  criticals = args.criticals

  check_load(warnings, criticals)