import cantools
import can
import tkinter as tk 


# >>>>>>>>>>>>>>>>>>>>>>>>
# load tkinter
gui = tk.Tk()
gui.title("Decoded CAN Signals")

# storing the names of the signals
labels = {}

# method that updates live CAN signal values
def update_signals(CAN_messages):
	for name, value in CAN_messages.items():
		if name not in labels:
			labels[name] = tk.Label(gui, text="", font=("Courier", 14))
			labels[name].pack(pady=5)
		labels[name].config(text=f"{name}: {value}")



# load dbc
dbc = cantools.database.load_file("filename.dbc")

# prep cantools 
bus = can.interface.Bus(bustype = 'socketcan', channel = 'can0', bitrate = 250000)


# read CAN traffic and decode
def read_can():
	frame = bus.recv(0.1) # check for new CAN frames every 0.1 secs
	if frame:
		try:
			dmsg = dbc.decode_message(frame.arbitration_id, frame_data) # this is a dict -> {"BMS SOC": 62}
			update_signals(dmsg)
		except:
			pass 
	gui.after(10, read_can)


read_can()
gui.mainloop()

