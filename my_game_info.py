from tkinter import *
import my_database as db
from tkinter import messagebox
import json
import time
import sys
import os

os.system('clear')

root = Tk()
root.title('Game Info')
root.iconbitmap('VariedLogo.ico')

my_window_width = 330
my_window_height = 160
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
	# x_name = player
	# print('|one two')
	root.destroy();


# def games_played(player, opponent, outcome, mark):
	# get info from database
	# player is the player or None
	# opponent is the opponent or None
	# outcome is played, won, lost, draw, or None
	# mark is x or o or None

	# 28 query types
	# 	all games | player = '', opponent = '', outcome = '', mark =''
	#   all won games | player = '', opponent = '', outcome = 'won', mark =''
	#   all lost games | player = '', opponent = '', outcome = 'lost', mark =''
	#   all draw games | player = '', opponent = '', outcome = 'draw', mark =''
	# 	all player games | player = '<player>', opponent = '', outcome = '', mark =''
	#   all player as x games | player = '<player>', opponent = '', outcome = '', mark ='x'
	#   all player as x won games | player = '', opponent = '', outcome = 'won', mark ='x'
	#   all player as x lost games | player = '', opponent = '', outcome = 'lost', mark ='x'
	#   all player as x draw games | player = '', opponent = '', outcome = 'draw', mark ='x'
	#   all player as o games | player = '', opponent = '', outcome = '', mark ='o'
	#   all player as o won games | player = '', opponent = '', outcome = 'won', mark ='o'
	#   all player as o lost games | player = '', opponent = '', outcome = 'lost', mark ='o'
	#   all player as o draw games | player = '', opponent = '', outcome = 'draw', mark ='o'
	# 	player won games | player = '<player>', opponent = '', outcome = 'won', mark =''
	#   player lost games | player = '<player>', opponent = '', outcome = 'lost', mark =''
	# 	player draw games | player = '<player>', opponent = '', outcome = 'draw', mark =''
	#   player against opponent games player = '<player>', opponent = '<opponent>', outcome = '', mark =''
	# 	player won games against opponent player = '<player>', opponent = '<opponent>', outcome = 'won', mark =''
	#   player lost games against opponent player = '<player>', opponent = '<opponent>', outcome = 'lost', mark =''
	#   player draw games against opponent player = '<player>', opponent = '<opponent>', outcome = 'draw', mark =''
	#   ----------------------------------
	#   all x games player = '', opponent = '', outcome = '', mark ='x'
	#   all x won games player = '', opponent = '', outcome = 'won', mark ='x'
	#   all x lost games player = '', opponent = '', outcome = 'lost', mark ='x'
	#   all x draw games player = '', opponent = '', outcome = 'draw', mark ='x'
	#   all o games player = '', opponent = '', outcome = '', mark ='o'
	#   all o won games player = '', opponent = '', outcome = 'won', mark ='o'
	#   all o lost games player = '', opponent = '', outcome = 'lost', mark ='o'
	#   all o draw games player = '', opponent = '', outcome = 'draw', mark ='o'

	# results = []
	# results = db.query(player, opponent, outcome, mark)

	# return results


def get_db_data():

	# messagebox.showinfo('My Game', 'Getting Data')

	the_player = player.get()
	the_opponent = opponent.get()
	if radio_select_int.get() >= len(game_selection):
		the_outcome = ''
	elif radio_select_int.get() < 0:
		the_outcome = ''
	else:
		the_outcome = game_selection[int(radio_select_int.get())]
	the_mark = mark_entry.get()

	# messagebox.showinfo('My Game', 'Got the criteria')
	
	results = []
	results = db.query(the_player, the_opponent, the_outcome, the_mark)

	# messagebox.showinfo('My Game', results)

	if len(results) == 0:
		# only include those parameters that have a value
		msg = 'The results: No results for '
		if the_player != '':
			msg = f'{msg}player {the_player}, '
		if the_opponent != '':
			msg = f'{msg}opponent {the_opponent}, '
		if the_outcome != '':
			msg = f'{msg}outcome {the_outcome}, '
		if the_mark != '':
			msg = f'{msg}mark {the_mark}.'
		if msg[-2] + msg[-1] == ', ':
			# if the last two characters are ', ' replace it with a '.'
			msg = f'{msg[:-2]}.'
		# messagebox.showinfo('My Game', 'sending a msg')
		print(msg)
	else:
		# messagebox.showinfo('My Game', 'sending results')
		print(f'The results: {results}')
				

def on_entry_focus(event):
	if player.get().strip() == '':
		player.focus_set()


def clear_selections():
	# print('clear selections')
	if button_checked.get():
		radio_select_int.set(len(game_selection))
		# button_checked.set(0)		


def clear_the_clear():
	button_checked.set(0)


# create the main frame
main_frame = Frame(root, bg='#C0C0C0')
main_frame.pack(fill=BOTH, expand=1)

# create player info frame
player_info = Frame(main_frame, bg='#C0C0C0')
player_info.pack(fill=X, pady=(10, 0))

# create the radio buttons frame
radio_frame = Frame(main_frame, bg='#C0C0C0')
radio_frame.pack(fill=X, pady=(10, 0))

# create mark frame
mark_frame = Frame(main_frame, bg='#C0C0C0')
mark_frame.pack(fill=X, pady=(10, 0))

# create command buttons frame
command_frame = Frame(main_frame, bg='#C0C0C0')
command_frame.pack(fill=X, pady=(10,0))

# entry for the player
player_label = Label(player_info, text='Player:', anchor=W, bg='#C0C0C0')
player_label.grid(row=0, column=0, sticky=W, padx=(10, 0))

player = Entry(player_info, bg='#C0C0C0')
player.grid(row=0, column=1, padx=15)

# entry for the opponent
opponent_label = Label(player_info, text='Opponent:', anchor=W, bg='#C0C0C0')
opponent_label.grid(row=1, column=0, sticky=W, padx=(10, 0))

opponent = Entry(player_info, bg='#C0C0C0')
opponent.grid(row=1, column=1, padx=15)
opponent.bind('<FocusIn>', on_entry_focus)

# radio buttons for games played or wins or losses
radio_select_int = IntVar()
game_selection = ['played', 'won', 'lost', 'draw']
radio_select = []
for x in range(len(game_selection)):
	radio_select.append(Radiobutton(radio_frame, text=game_selection[x], state=NORMAL, variable=radio_select_int, value=x, bg='#C0C0C0', command=clear_the_clear))
	radio_select[x].grid(row=0, column=x, padx=(10, 0))
radio_select_int.set(len(game_selection))

# check box to clear the radiobuttons
button_checked = IntVar()
clear_button = Checkbutton(radio_frame, text='Clear', bg='#C0C0C0', variable=button_checked, command=clear_selections)
clear_button.grid(row=0, column=len(game_selection), padx=(10, 0))

# entry for player mark
mark_label = Label(mark_frame, text='Which Mark:', bg='#C0C0C0')
mark_label.grid(row=0, column=0, padx=(10, 0))

mark_entry = Entry(mark_frame, width=3, bg='#C0C0C0', justify='center')
mark_entry.grid(row=0, column=1, padx=(10, 0))

# get data from database
db_data = Button(command_frame, text='Get Data', command=get_db_data)
db_data.grid(row=0, column=0, padx=(10, 0))

# send data and close app button
send_data = Button(command_frame, text='Send Data', command=send_close)
send_data.grid(row=0, column=1, padx=(10, 0))

# labels for percentage wins and losses


# test
# outcome = 'won'
# sql_query = f'SELECT * results WHERE outcome = ?, ({outcome},)'
# print(sql_query)




if __name__ == "__main__":
    root.mainloop()


