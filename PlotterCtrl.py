#! python
# -*- encoding: utf-8 -*-
#

from pathlib import Path
from time import sleep
from datetime import datetime
import signal
import sys
import os
from shutil import disk_usage
import yaml

################################################## Global vars
StartTime = datetime.now()
SleepTime = 60
DelLockedFile = False
AppPath = Path('.')
# Create a locled file to indicate that an instance of script in running
LockedFile = AppPath / "PlotterCtrl.lock"
PlotSize = 108797952330 # MadMax plot's size in bytes
################################################## Global vars => End

################################################## Plotter parameters
# Note: tmp and destination path must have trail "/"
# PlotterPath = Path('/home/mdvinh/madmax/build/chia_plot')
# NumOfThreads = 16
# tmp1 = './tmpplot/'
# tmp2 = '/mnt/nvme980/tmp2/'
# dest = '/mnt/sas201/hpool/'
# PoolKey = 'ad1f1da3c152e8d27c9565f35c60b9981a9034ab06a3c59db18efe41ae4255fb88f4605c51bf05d3856461f63a342631'
# FarmerKey = 'b5bdf57ebf4c5a02264ae7573a2a8be24cf06aa69ed89a7a4bcffb4e048f8132a8c72c226f193961583b818c958fbf6d'

# if len(sys.argv) == 2:
#     try:
#         NumOfPlot = int(sys.argv[1])
#         print("NumOfPlot: ", NumOfPlot)
#     except ValueError:
#         print("Invalid value")
#         sys.exit(0)
# elif len(sys.argv) == 1:
#     DiskTatol, DiskUsed, DiskFree = disk_usage(dest)
#     NumOfPlot = int(DiskFree/PlotSize)
#     if NumOfPlot == 0:
#         print('Not engouh space for plots')
#         sys.exit(0)
#     print("NumOfPlot: ", NumOfPlot)
# else:
#     print("Bớt điên giùm tao")
#     sys.exit(0)

# PlotterCmd = f'{PlotterPath} -n {NumOfPlot} -r {NumOfThreads} -t {tmp1} -2 {tmp2} -d {dest} -p {PoolKey} -f {FarmerKey}'
################################################## Plotter parameters => End

################################################## Function to catch ctrl-c
# Handle ctr-c
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')

    if DelLockedFile:
        os.remove(LockedFile)

    RunTime()
    sys.exit(0)
################################################## Function to catch ctrl-c => End

################################################## Function Run timme
def RunTime():
    Duration = datetime.now() - StartTime
    print('Run in', Duration)
################################################## Function Run timme => End



################################################## Main function
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    # If locked file existed then wait for other instance to complte
    # while Path(LockedFile).is_file():
    #     sleep (SleepTime)
        # print(".", end =" ", flush=True)

    # Create locked file for this instance
    # open(LockedFile, 'w').close()
    # DelLockedFile = True

    # This block is for testing only
    # print("Testing block")
    # while True:
    #     sleep(5)
    #     print(".", end =" ", flush=True)
    
    # Execute plotter commnad
    # os.system(f'{PlotterCmd}')

    # Remove locked file when done
    # os.remove(LockedFile)
    RunTime()
    print('Done')
