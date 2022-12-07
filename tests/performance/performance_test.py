import os 
from subprocess import PIPE, run
import datetime
import pkg_resources  # part of setuptools 
import cpuinfo
import csv
# python -m cProfile -o program.prof 4000_canvas_40000_annotations.py
# we keep track of the following parameters
#'real_time_sec','user_time_sec','sys_time_sec','version','date','python_version','arch_string_raw','vendor_id_raw','brand_raw','hz_advertised_friendly'

version = pkg_resources.require("pyIIIFpres")[0].version   


write = True
infos = cpuinfo.get_cpu_info()

# First test not optimized
command = ["time","python","4000_canvas_40000_annotations.py"]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
times = result.stderr.split()

fields=[times[0],times[2],times[4],version,datetime.datetime.now(),
infos['python_version'],infos['arch_string_raw'],infos['vendor_id_raw'],
infos['brand_raw'],infos['hz_advertised_friendly']]
if write:
    with open(r'performance_log_4000_canvas_40000_annotations.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
else:
    print(fields)


# Second test optimized
command = ["time","python","-O","4000_canvas_40000_annotations.py"]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
times = result.stderr.split()

fields=[times[0],times[2],times[4],version,datetime.datetime.now(),
infos['python_version'],infos['arch_string_raw'],infos['vendor_id_raw'],
infos['brand_raw'],infos['hz_advertised_friendly']]
if write:
    with open(r'performance_log_4000_canvas_40000_annotations_Optimized.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
else:
    print(fields)

# third test not optimized
command = ["time","python","2000_canvas_2000_annotations.py"]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
times = result.stderr.split()

fields=[times[0],times[2],times[4],version,datetime.datetime.now(),
infos['python_version'],infos['arch_string_raw'],infos['vendor_id_raw'],
infos['brand_raw'],infos['hz_advertised_friendly']]
if write:
    with open(r'performance_log_2000_canvas_2000_annotations.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
else: 
    print(fields)


# Forth test optimized
command = ["time","python","-O","2000_canvas_2000_annotations.py"]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
times = result.stderr.split()

fields=[times[0],times[2],times[4],version,datetime.datetime.now(),
infos['python_version'],infos['arch_string_raw'],infos['vendor_id_raw'],
infos['brand_raw'],infos['hz_advertised_friendly']]
if write:
    with open(r'performance_log_2000_canvas_2000_annotations_Optimized.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
else: 
    print(fields)

# Fifth test not optimized orjson
command = ["time","python","4000_canvas_40000_annotations_orjson.py"]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
times = result.stderr.split()

fields=[times[0],times[2],times[4],version,datetime.datetime.now(),
infos['python_version'],infos['arch_string_raw'],infos['vendor_id_raw'],
infos['brand_raw'],infos['hz_advertised_friendly']]
if write:
    with open(r'performance_log_4000_canvas_40000_annotations_orjson.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
else:
    print(fields)


# Sixith test optimized orjson
command = ["time","python","-O","4000_canvas_40000_annotations_orjson.py"]
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
times = result.stderr.split()

fields=[times[0],times[2],times[4],version,datetime.datetime.now(),
infos['python_version'],infos['arch_string_raw'],infos['vendor_id_raw'],
infos['brand_raw'],infos['hz_advertised_friendly']]
if write:
    with open(r'performance_log_4000_canvas_40000_annotations_Optimized_orjson.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
else:
    print(fields)
