# script to read a candump log file and send it to vcan0
import cantools
import can
import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "inductEV_J1939_2pad.dump")


bus = can.interface.Bus(bustype = 'socketcan', channel = 'vcan0', bitrate = 250000)

# 
with open(filepath) as file:
    # x = 0
    time_delay = 000.000000
    for i in file: 
        # x +=1 # to test a few lines without running the whole file   
        line = i.strip().split() # this makes each line a list
        timestamp = line[0]
        timestamp = timestamp.strip('()')
        timestamp = float(timestamp)
        delay = timestamp - time_delay
        time_delay = timestamp
        # interface = line[1]
        frame_id = line[2]
        # dlc = line[3]
        payload = line[4:]
        data_str = ' '.join(str(x) for x in payload)
        # print(f"timestamp = {timestamp},interface = {interface}, frame_id = {frame_id}, dlc = {dlc}, payload = {payload}") #test the output
        # print(f"data_string = {data_str}")
        # print(type(dlc))
        print(i)
        bus.send(frame_id, data_str)
        time.sleep(delay)
        # if x > 2: # stop doing lines here
            # break



