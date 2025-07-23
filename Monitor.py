import cantools
import can
import tkinter as tk
import subprocess

# load tkinter
gui = tk.Tk()
gui.title("CANbus Signal Monitor")

# CANbus signals and values to be displayed
labels = {}
row_map = {}  # keeps track of row index for each signal
next_row = 0  # global counter for grid rows 

def update_signals(CAN_messages):
    global next_row
    for name, value in CAN_messages.items():
        if name not in labels:
            # Create static label for the name
            tk.Label(gui, text=f"{name}:", font=("Droid Sans Fallback", 12)).grid(row=next_row, column=0, sticky="e", padx=10, pady=2)

            # Create dynamic label for the value and store it
            value_label = tk.Label(gui, text="", font=("Droid Sans Fallback", 12), anchor="w")
            value_label.grid(row=next_row, column=1, sticky="w", padx=10, pady=2)
            labels[name] = value_label

            # Track which row this signal uses
            row_map[name] = next_row
            next_row += 1

        # Update value in existing label
        labels[name].config(text=f"{value}")


# load dbc
dbc = cantools.database.load_file("j1939.dbc")

# prep cantools 
bus = can.interface.Bus(bustype = 'socketcan', channel = 'vcan0', bitrate = 250000)


# read CAN traffic and decode
def read_can():
	frame = bus.recv(0.1) # check for new CAN frames every 0.1 secs
	if frame:
		try:
			dmsg = dbc.decode_message(frame.arbitration_id, frame.data) # dmsg is a dict -> {"BMS SOC": 62}
			update_signals(dmsg) # pass it to the gui
		except:
			pass 
	gui.after(10, read_can) # update gui every 10 seconds


read_can()
gui.mainloop()
subprocess.Popen(['python', 'candump_parser.py'])

