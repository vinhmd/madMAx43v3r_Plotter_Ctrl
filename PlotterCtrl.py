#! python
# -*- encoding: utf-8 -*-
#

from datetime import datetime
from shutil import disk_usage
import signal
import sys
import os
import yaml

################################################## Global vars
StartTime = datetime.now()
ConFile = "config.yaml"


################################################## Function Generate Plotter command
def GenCmd(NumOfPlot, Config):
    Dest = False
    while len(Config['MadPlotter']['d']):
        d = Config['MadPlotter']['d'][0]
        try:
            PlotAvailable = CalPlot(d, Config['Main']['PlotSize'])
            if PlotAvailable:
                Dest = d
                Config['MadPlotter']['d'].remove(d)
                print(f'{d} has enough free space for {PlotAvailable} plot(s).')
                if not NumOfPlot:
                    NumOfPlot = PlotAvailable
                    break
                if NumOfPlot > PlotAvailable:
                    print(f'You manage to create too many plot than the destination can handle.')
                    Answer = input('Are you sure? (Y/n): ')
                    if Answer.lower() == 'n':
                        exit()
                    if (Answer.lower() == 'y') or (Answer == ''):
                        break
                    else:
                        return False
            Config['MadPlotter']['d'].remove(d)
        except FileNotFoundError:
            print(d, 'is not exist')
            Config['MadPlotter']['d'].remove(d)
    
    if not Dest:
        print('There is no destination suitable')
        return False

    PlotterCmd = f"{Config['MadPlotter']['PlotterPath']} -n {NumOfPlot} -d {Dest}"

    for key in Config['MadPlotter']:
        if (key not in ['PlotterPath', 'd']) and (Config['MadPlotter'][key] != None):
            PlotterCmd = f"{PlotterCmd} -{key} {Config['MadPlotter'][key]}"
    
    return PlotterCmd


################################################## Function Calculate number of plots base on Dest free space
def CalPlot(Dest, PlotSize):
    DiskTatol, DiskUsed, DiskFree = disk_usage(Dest)
    return int(DiskFree/PlotSize)


################################################## Function to catch ctrl-c
# Handle ctr-c
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    RunTime()
    sys.exit(0)


################################################## Function Run timme
def RunTime():
    print('Run in', datetime.now() - StartTime)




################################################## Main function
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    # Load config
    try:
        with open(ConFile, 'r') as file:
            Config = yaml.safe_load(file)
    except FileNotFoundError:
        print("Configuration file is missing")
        exit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        exit()
    
    # Check NumOfPlot to create
    if len(sys.argv) == 2:
        try:
            NumOfPlotArg = int(sys.argv[1])
            if NumOfPlotArg <= 0:
                print("Number of plot must be greater than 0")
                exit()
        except ValueError:
            print("Invalid value")
            exit()
    elif len(sys.argv) == 1:
        NumOfPlotArg = False
    else:
        print("python3 PlotterCtrl.py [optional: Num of plot to create]")
        exit()

    if not os.path.isfile(Config['MadPlotter']['PlotterPath']):
        print('Please check for plotter path')
        exit()

    RunYet = False

    while True:
        PlotterCmd = GenCmd(NumOfPlotArg, Config)
        if PlotterCmd:
            RunYet = True
            os.system(f'{PlotterCmd}')
            
        if (not PlotterCmd) and (not RunYet):
            print('There is something wrong in your configuration.\nPlease check and run again.')
            break
        
        if (not PlotterCmd):
            print('Task completed')
            break
        
        if NumOfPlotArg:
            print('Task completed')
            break

    RunTime()
