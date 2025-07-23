# script to read a candump log file and send it to vcan0
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "inductEV_J1939_2pad.dump")

# def message_assembler(can_message):



with open(filepath) as file:
    x = 0
    for i in file: 
        x +=1 # to test a few lines without running the whole file   
        line = i.strip().split()
        timestamp = line[0]
        interface = line[1]
        frame_id = line[2]
        dlc = line[3]
        payload = line[4:]
        data_str = ', '.join(str(x) for x in payload)
        print(f"timestamp = {timestamp},interface = {interface}, frame_id = {frame_id}, dlc = {dlc}, payload = {payload}") #test the output
        print(f"data_string = {data_str}")
        print(type(dlc))
        if x > 0: # stop doing lines here
            break



