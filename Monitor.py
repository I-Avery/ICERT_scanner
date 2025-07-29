import cantools
import can
import tkinter as tk
import subprocess
import time
import os


# dbc_dir = os.path.dirname(os.path.abspath(__file__))
# dbc_filepath = os.path.join(dbc_dir, "j1939.dbc")
# # parser_filepath = os.path.join(dbc_dir, "candump_parser.py") # removing to test joining the logic

# # >>>>>>>>>>>
# # Test that combines the parser logic into this file
# script_dir = os.path.dirname(os.path.abspath(__file__))
# filepath = os.path.join(script_dir, "inductEV_J1939_2pad.dump")
# # >>>>>>>>>>>


# # load tkinter
# gui = tk.Tk()
# gui.title("CANbus Signal Monitor")

# # CANbus signals and values to be displayed
# labels = {}
# row_map = {}  # keeps track of row index for each signal
# next_row = 0  # global counter for grid rows 

# def update_signals(CAN_messages):
# 	parser_function()
# 	print(f"received at the gui: {CAN_messages}")
# 	global next_row
# 	for name, value in CAN_messages.items():
# 		if name not in labels:
#             # Create static label for the name
# 			tk.Label(gui, text=f"{name}:", font=("Droid Sans Fallback", 12)).grid(row=next_row, column=0, sticky="e", padx=10, pady=2)
			

#             # Create dynamic label for the value and store it
# 			value_label = tk.Label(gui, text="", font=("Droid Sans Fallback", 12), anchor="w")
# 			value_label.grid(row=next_row, column=1, sticky="w", padx=10, pady=2)
# 			labels[name] = value_label

#             # Track which row this signal uses
# 			row_map[name] = next_row
# 			next_row += 1

#         # Update value in existing label
# 		labels[name].config(text=f"{value}")


# # load dbc
# dbc = cantools.database.load_file(dbc_filepath)

# # prep cantools 
# bus = can.interface.Bus(interface = 'virtual', channel = 'vcan0', bitrate = 250000)

# # >>>>>>>>>>>>>>
# # # Parser loop
# # def parser_loop():
# #     with open(filepath) as file:
# #         # x = 0
# #         time_delay = 000.000000
# #         for i in file: 
# #             # x +=1 # to test a few lines without running the whole file   
# #             line = i.strip().split() # this makes each line a list
# #             timestamp = line[0].strip('()')
# #             timestamp = float(timestamp)
# #             delay = timestamp - time_delay
# #             time_delay = timestamp
# #             # interface = line[1]
# #             frame_id = int(line[2], 16) #typecast the str to hex
# #             # dlc = line[3]
# #             payload_str = line[4:]
# #             payload_int = [int(x,16) for x in payload_str]
# #             payload_byte = bytes(payload_int)
# #             # data_str = ' '.join(str(x) for x in payload) #wrong approach, it needs to be a bytes object
# #             # print(f"timestamp = {timestamp},interface = {interface}, frame_id = {frame_id}, dlc = {dlc}, payload = {payload}") #test the output
# #             # print(f"data_string = {data_str}")
# #             # print(type(dlc))
# #             # print(i) #check the output
# #             msg = can.Message(
# #                 arbitration_id=frame_id,
# #                 data=payload_byte,
# #                 is_extended_id=True #true for 29 bit IDs
# #             )
# #             print(f"sending: {msg}")
# #             bus.send(msg)
# #             print(f"sent: {msg}")
# #             time.sleep(delay) # mimic the timing of the messages from the log
# #             # if x > 2: # stop doing lines here
# #                 # break

# # >>>>>>>>>>>>>>>>>>

# # read CAN traffic and decode
# def read_can():
# 	frame = bus.recv(0.1) # check for new CAN frames every 0.001 secs
# 	if frame:
# 		print("received:", frame) # debug check
# 		try:
# 			print("trying")
# 			dmsg = dbc.decode_message(frame.arbitration_id, frame.data) # dmsg is a dict -> {"BMS SOC": 62}
# 			print(f"decoded message: {dmsg}")
# 			update_signals(dmsg) # pass it to the gui
# 			print("sent to the gui")
# 		except:
# 			pass 
# 	# gui.after(100, read_can) # update gui every 1 seconds


# # subprocess.Popen(['python', parser_filepath])

# # subprocess.Popen(['python', parser_filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# # read_can()
# gui.mainloop()
# # parser_loop()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# TESTING


dbc_dir = os.path.dirname(os.path.abspath(__file__))
dbc_filepath = os.path.join(dbc_dir, "j1939.dbc")
# parser_filepath = os.path.join(dbc_dir, "candump_parser.py") # removing to test joining the logic

# # >>>>>>>>>>>
# # Test that combines the parser logic into this file
script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "inductEV_J1939_2pad.dump")
# # >>>>>>>>>>>


# load tkinter
gui = tk.Tk()
gui.title("CANbus Signal Monitor")

# CANbus signals and values to be displayed
labels = {}
# row_map = {}  # keeps track of row index for each signal

labels = {}

def update_signals(signal_dict):
    print(f"Received at gui: {signal_dict}")
    for name, value in signal_dict.items():
        if name not in labels:
            # Create label (key on left, value on right)
            name_label = tk.Label(gui, text=f"{name}:", anchor="e", width=15)
            value_label = tk.Label(gui, text=str(value), anchor="w", width=15)

            row = len(labels)
            name_label.grid(row=row, column=0, sticky="e", padx=5, pady=2)
            value_label.grid(row=row, column=1, sticky="w", padx=5, pady=2)

            labels[name] = value_label
        else:
            # Update value
            labels[name].config(text=str(value))
    parser_loop()


# load dbc
dbc = cantools.database.load_file(dbc_filepath)

# prep cantools 
bus = can.interface.Bus(interface = 'virtual', channel = 'vcan0', bitrate = 250000)

# >>>>>>>>>>>>>>
# Parser loop
def parser_loop():
    print("parser called")
    with open(filepath) as file:
        # x = 0
        time_delay = 000.000000
        for i in file: 
            line = i.strip().split() # this makes each line a list
            timestamp = line[0].strip('()')
            timestamp = float(timestamp)
            delay = timestamp - time_delay
            time_delay = timestamp
            frame_id = int(line[2], 16) #typecast the str to hex
            payload_str = line[4:]
            payload_int = [int(x,16) for x in payload_str]
            payload_byte = bytes(payload_int)
            msg = can.Message(
                arbitration_id=frame_id,
                data=payload_byte,
                is_extended_id=True #true for 29 bit IDs
            )
            # print(f"sending: {msg}")
            bus.send(msg)
            print(f"message sent: {msg}")
            read_can()
            time.sleep(delay) # mimic the timing of the messages from the log

# >>>>>>>>>>>>>>>>>>

# read CAN traffic and decode
def read_can():
    print("read can called")
    frame = bus.recv(0.001) # check for new CAN frames every 0.001 secs
    if frame:
        try:
            print("trying attempted")
            dmsg = dbc.decode_message(frame.arbitration_id, frame.data) # this is a dict -> {BMS SOC: 62}
            update_signals(dmsg)
            print(f"dmsg attempted to send: {dmsg}")
        except:
            pass
        


# subprocess.Popen(['python', parser_filepath])

# subprocess.Popen(['python', parser_filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# read_can()
# parser_loop()
gui.after(0, parser_loop)
gui.mainloop()



