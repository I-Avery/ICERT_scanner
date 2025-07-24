# script to read a candump log file and send it to vcan0
import cantools
import can
import time
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "inductEV_J1939_2pad.dump")


bus = can.interface.Bus(interface = 'virtual', channel = 'vcan0', bitrate = 250000)

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
        frame_id = int(line[2], 16) #typecast the str to hex
        # dlc = line[3]
        payload_str = line[4:]
        payload_int = [int(x,16) for x in payload_str]
        payload_byte = bytes(payload_int)
        # data_str = ' '.join(str(x) for x in payload) #wrong approach, it needs to be a bytes object
        # print(f"timestamp = {timestamp},interface = {interface}, frame_id = {frame_id}, dlc = {dlc}, payload = {payload}") #test the output
        # print(f"data_string = {data_str}")
        # print(type(dlc))
        # print(i) #check the output
        msg = can.Message(
            arbitration_id=frame_id,
            data=payload_byte,
            is_extended_id=True #true for 29 bit IDs
        )
        bus.send(msg)
        time.sleep(delay)
        # if x > 2: # stop doing lines here
            # break



