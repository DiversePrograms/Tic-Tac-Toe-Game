from tkinter import *
from tkinter import messagebox
from icecream import ic
import time
import sys
import os

os.system('clear')

root = Tk()
root.title('Get Names')
root.iconbitmap('VariedLogo.ico')

my_window_width = 250
my_window_height = 125
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (my_window_width / 2))
y = int((screen_height / 2) - (my_window_height / 2))
window_info = (f'{my_window_width}x{my_window_height}+{x}+{y}')
root.geometry(window_info)

# need one of the two following statements or windows will place the 
#   window wherever it wants
# players.resizable(1, 1)    # resizable
root.resizable(0, 0)    # not resizable

root.attributes('-topmost', 1)
root.configure(bg='#C0C0C0')


def send_close():
	x_name = x_player.get()
	o_name = o_player.get()
	print(f'|{x_name} {o_name}')
	root.destroy();


# entry for the player
x_player_label = Label(root, text='X Player:', anchor=W, bg='#C0C0C0')
x_player_label.grid(row=0, column=0, sticky=W, pady=(20, 0), padx=(10, 0))

x_player = Entry(root)
x_player.grid(row=0, column=1, pady=(20, 0), padx=(10, 0))

# entry for the opponent
o_player_label = Label(root, text='Opponent:', anchor=W, bg='#C0C0C0')
o_player_label.grid(row=1, column=0, sticky=W, padx=(10, 0))

o_player = Entry(root)
o_player.grid(row=1, column=1, padx=(10, 0))

# send data and close app button
send_data = Button(root, text='Send Names', command=send_close)
send_data.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=(10, 0))






if __name__ == "__main__":
    root.mainloop()

