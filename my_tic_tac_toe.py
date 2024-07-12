from tkinter import *
import my_database as tk_db
from icecream import ic
import string
# import player_names as pn
# import game_info as gi
import my_results as ri
from tkinter import messagebox
import json
import asyncio
import ast
import time
import subprocess
import sys
import os
from win32api import GetMonitorInfo, MonitorFromPoint

os.system('clear')

# ic('start the root window')

root = Tk()
root.title('Tic Tac Toe')
root.iconbitmap('VariedLogo.ico')

my_window_width = 380
my_window_height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (my_window_width / 2))
y = int((screen_height / 2) - (my_window_height / 2))
window_info = (f'{my_window_width}x{my_window_height}+{x}+{y}')
root.geometry(window_info)

# need one of the two following statements or windows will place the 
#   window wherever it wants
# root.resizable(1, 1)    # resizable
root.resizable(0, 0)    # not resizable

root.attributes('-topmost', 1)
root.configure(bg='#C0C0C0')


# X goes first
clicked = True
count = 0

# ic('go to widgets construction')
# sys.stdout.flush()

# check to see if someone won
def check_if_a_winner(w):
	global winner, clicked
	global x_player_name, o_player_name

	winner = False

	if w == 'X':
		if len(x_player_name['text']) > 0:
			msg = x_player_name['text'] + ' is the winner!!!'
			w = x_player_name['text']
		else:
			msg = 'X is the winner!!!'
			w = 'won'
	elif w == 'O':
		if len(o_player_name['text']) > 0:
			msg = o_player_name['text'] + ' is the winner!!!'
			w = o_player_name['text']
		else:
			msg = 'O is the winner!!!'
			w = 'lost'
	else:
		msg = 'We have no winner!'
		w = 'draw'

	# messagebox.showinfo('Tic Tac Toe', msg)

	# send data to the database
	# messagebox.showinfo('Tic Tac Toe', f'{x_player_name['text']}, {o_player_name['text']}, {w}')
	tk_db.submit(1, x_player_name['text'], o_player_name['text'], w)

	response = messagebox.askyesno('Tic Tac Toe', 'Play Again?')
	if response:
		change_color('c')
		clear_buttons()
		clear_the_count_values()
		clicked = True    # X starts the game

		response = messagebox.askyesno('Tic Tac Toe', 'Do you want to change player names?')
		if response:
			get_player_names()
	else:
		# tk_db.query('Danno', 'Suezbo')
		# clear_buttons()
		# x_player_name.config(text='')
		# o_player_name.config(text='')
		sys.exit(0)

	winner = False


def clear_buttons():
	b1.config(text=' ')
	b2.config(text=' ')
	b3.config(text=' ')
	b4.config(text=' ')
	b5.config(text=' ')
	b6.config(text=' ')
	b7.config(text=' ')
	b8.config(text=' ')
	b9.config(text=' ')


# change the color to winner or button face
def change_color(color, line='all'):
	match color:
		case 'w':
			# change color of the winning buttons to red
			match line:
				case 'r0':
					# b1, b2, b3
					b1.config(bg='#00FF00', fg='#FFFFFF')
					b2.config(bg='#00FF00', fg='#FFFFFF')
					b3.config(bg='#00FF00', fg='#FFFFFF')

				case 'r1':
					# b4, b5, b6
					b4.config(bg='#00FF00', fg='#FFFFFF')
					b5.config(bg='#00FF00', fg='#FFFFFF')
					b6.config(bg='#00FF00', fg='#FFFFFF')

				case 'r2':
					# b7, b8, b9
					b7.config(bg='#00FF00', fg='#FFFFFF')
					b8.config(bg='#00FF00', fg='#FFFFFF')
					b9.config(bg='#00FF00', fg='#FFFFFF')

				case 'c0':
					# b1, b4, b7
					b1.config(bg='#00FF00', fg='#FFFFFF')
					b4.config(bg='#00FF00', fg='#FFFFFF')
					b7.config(bg='#00FF00', fg='#FFFFFF')

				case 'c1':
					# b2, b5, b8
					b2.config(bg='#00FF00', fg='#FFFFFF')
					b5.config(bg='#00FF00', fg='#FFFFFF')
					b8.config(bg='#00FF00', fg='#FFFFFF')

				case 'c2':
					# b3, b6, b9
					b3.config(bg='#00FF00', fg='#FFFFFF')
					b6.config(bg='#00FF00', fg='#FFFFFF')
					b9.config(bg='#00FF00', fg='#FFFFFF')

				case 'd0':
					# b1, b5, b9
					b1.config(bg='#00FF00', fg='#FFFFFF')
					b5.config(bg='#00FF00', fg='#FFFFFF')
					b9.config(bg='#00FF00', fg='#FFFFFF')

				case 'd1':
					# b3, b5, b7
					b3.config(bg='#00FF00', fg='#FFFFFF')
					b5.config(bg='#00FF00', fg='#FFFFFF')
					b7.config(bg='#00FF00', fg='#FFFFFF')
		case 'c':
			b1.config(bg='SystemButtonFace', fg='#000000')
			b2.config(bg='SystemButtonFace', fg='#000000')
			b3.config(bg='SystemButtonFace', fg='#000000')
			b4.config(bg='SystemButtonFace', fg='#000000')
			b5.config(bg='SystemButtonFace', fg='#000000')
			b6.config(bg='SystemButtonFace', fg='#000000')
			b7.config(bg='SystemButtonFace', fg='#000000')
			b8.config(bg='SystemButtonFace', fg='#000000')
			b9.config(bg='SystemButtonFace', fg='#000000')


# clear the count levels
def clear_the_count_values():
	global xr0, xc0, xr1, xc1, xr2, xc2, xd0, xd1
	global or0, oc0, or1, oc1, or2, oc2, od0, od1
	global count
	
	xr0 = 0
	xc0 = 0
	xr1 = 0
	xc1 = 0
	xr2 = 0
	xc2 = 0

	xd0 = 0
	xd1 = 0

	or0 = 0
	oc0 = 0
	or1 = 0
	oc1 = 0
	or2 = 0
	oc2 = 0

	od0 = 0
	od1 = 0

	count = 0


def b_click(b, name):
	global clicked, count, winner
	global xr0, xc0, xr1, xc1, xr2, xc2, xd0, xd1
	global or0, oc0, or1, oc1, or2, oc2, od0, od1

	# messagebox.showinfo('Tic Tac Toe', f'Count = {count}')

	if b['text'] == ' ' and clicked == True:
		b['text'] = 'X'
		clicked = False
		count += 1
	elif b['text'] == ' ' and clicked == False:
		b['text'] = 'O'
		clicked = True
		count += 1
	else:
		msg = 'Hey! That box is already used by ' + b['text'] + '!\nPick another box.'
		messagebox.showerror('Tic Tac Toe', msg)
		return

	match name:
		case 'b1':
			match b['text']:
				case 'X':
					xr0 += 1
					xc0 += 1
					xd0 += 1

					# change the button color to red if a winner is found
					if xr0 == 3 or xc0 == 3 or xd0 == 3:
						if xr0 == 3:
							change_color('w', 'r0')
						elif xc0 == 3:
							change_color('w', 'c0')
						else:
							change_color('w', 'd0')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or0 += 1
					oc0 += 1
					od0 += 1

					# change the button color to red if a winner is found
					if or0 == 3 or oc0 == 3 or od0 == 3:
						if or0 == 3:
							change_color('w', 'r0')
						elif oc0 == 3:
							change_color('w', 'c0')
						else:
							change_color('w', 'd0')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b1')
		case 'b2':
			match b['text']:
				case 'X':
					xr0 += 1
					xc1 += 1

					if xr0 == 3 or xc1 == 3:
						if xr0 == 3:
							change_color('w', 'r0')
						else:
							change_color('w', 'c1')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or0 += 1
					oc1 += 1

					if or0 == 3 or oc0 == 3:
						if or0 == 3:
							change_color('w', 'r0')
						else:
							change_color('w', 'c1')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b2')
		case 'b3':
			match b['text']:
				case 'X':
					xr0 += 1
					xc2 += 1
					xd1 += 1

					if xr0 == 3 or xc2 == 3 or xd1 == 3:
						if xr0 == 3:
							change_color('w', 'r0')
						elif xc2 == 3:
							change_color('w', 'c2')
						else:
							change_color('w', 'd1')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or0 += 1
					oc2 += 1
					od1 += 1

					if or0 == 3 or oc2 == 3 or od1 == 3:
						if or0 == 3:
							change_color('w', 'r0')
						elif oc2 == 3:
							change_color('w', 'c2')
						else:
							change_color('w', 'd1')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b3')
		case 'b4':
			match b['text']:
				case 'X':
					xr1 += 1
					xc0 += 1

					if xr1 == 3 or xc0 == 3:
						if xr1 == 3:
							change_color('w', 'r1')
						else:
							change_color('w', 'c0')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or1 += 1
					oc0 += 1

					if or1 == 3 or oc0 == 3:
						if or1 == 3:
							change_color('w', 'r1')
						else:
							change_color('w', 'c0')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b4')
		case 'b5':
			match b['text']:
				case 'X':
					xr1 += 1
					xc1 += 1
					xd0 += 1
					xd1 += 1

					if xr1 == 3 or xc1 == 3 or xd0 == 3 or xd1 == 3:
						if xr1 == 3:
							change_color('w', 'r1')
						elif xc1 == 3:
							change_color('w', 'c1')
						elif xd0 == 3:
							change_color('w', 'd0')
						else:
							change_color('w', 'd1')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or1 += 1
					oc1 += 1
					od0 += 1
					od1 += 1

					if or1 == 3 or oc1 == 3 or od0 == 3 or od1 == 3:
						if or1 == 3:
							change_color('w', 'r1')
						elif oc1 == 3:
							change_color('w', 'c1')
						elif od0 == 3:
							change_color('w', 'd0')
						else:
							change_color('w', 'd1')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b5')
		case 'b6':
			match b['text']:
				case 'X':
					xr1 += 1
					xc2 += 1

					if xr1 == 3 or xc2 == 3:
						if xr1 == 3:
							change_color('w', 'r1')
						else:
							change_color('w', 'c2')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or1 += 1
					oc2 += 1

					if or1 == 3 or oc2 == 3:
						if or1 == 3:
							change_color('w', 'r1')
						else:
							change_color('w', 'c2')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b6')
		case 'b7':
			match b['text']:
				case 'X':
					xr2 += 1
					xc0 += 1
					xd1 += 1

					if xr2 == 3 or xc0 == 3 or xd1 == 3:
						if xr2 == 3:
							change_color('w', 'r2')
						elif xc0 == 3:
							change_color('w', 'c0')
						else:
							change_color('w', 'd1')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or2 += 1
					oc0 += 1
					od1 += 1

					if or2 == 3 or oc0 == 3 or od1 == 3:
						if or2 == 3:
							change_color('w', 'r2')
						elif oc0 == 3:
							change_color('w', 'c0')
						else:
							change_color('w', 'd1')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b7')
		case 'b8':
			match b['text']:
				case 'X':
					xr2 += 1
					xc1 += 1

					if xr2 == 3 or xc1 == 3:
						if xr2 == 3:
							change_color('w', 'r2')
						else:
							change_color('w', 'c1')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or2 += 1
					oc1 += 1

					if or2 == 3 or oc1 == 3:
						if or2 == 3:
							change_color('w', 'r2')
						else:
							change_color('w', 'c1')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b8')
		case 'b9':
			match b['text']:
				case 'X':
					xr2 += 1
					xc2 += 1
					xd0 += 1

					if xr2 == 3 or xc2 == 3 or xd0 == 3:
						if xr2 == 3:
							change_color('w', 'r2')
						elif xc2 == 3:
							change_color('w', 'c2')
						else:
							change_color('w', 'd0')

						# declare the winner
						winner = True
						check_if_a_winner('X')
				case 'O':
					or2 += 1
					oc2 += 1
					od0 += 1

					if or2 == 3 or oc2 == 3 or xd0 == 3:
						if or2 == 3:
							change_color('w', 'r2')
						elif oc2 == 3:
							change_color('w', 'c2')
						else:
							change_color('w', 'd0')

						# declare the winner
						winner = True
						check_if_a_winner('O')
			# messagebox.showinfo('Tic Tac Toe', 'You clicked b9')

	# msg1 = f'{xr0}, {xr1}, {xr2}, {xc0}, {xc1}, {xc2}, {xd0}, {xd1}'
	# msg2 = f'{or0}, {or1}, {or2}, {oc0}, {oc1}, {oc2}, {od0}, {od1}'
	# msg3 = f'{msg1}\n{msg2}'
	# messagebox.showinfo('Tic Tac Toe', msg3)

	if count >= 9 and winner == False:
		# messagebox.showinfo('Tic Tac Toe', f'Count = {count}')
		check_if_a_winner('none')


def games_info():
	# print('Games Info Definition')

	asyncio.run(call_games_info())


async def call_games_info():
	global result_tuples

	# run the external program
	process = await asyncio.create_subprocess_exec(
		'python', 'my_game_info.py',
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE
		)

	stdout, stderr = await process.communicate()

	# ic(stdout)
	# sys.stdout.flush()
	return_code = process.returncode
	results_list = []
	# sys.stdout.flush()
	# print(f'Length of STDOUT: {len(stdout)}')
	# sys.stdout.flush()
	db_results = stdout.decode()

	# ic(db_results)
	# ic('Ready to check')
	# sys.stdout.flush()

	try:
		# ic('Try the results')
		# sys.stdout.flush()
		results_string = db_results.split('The results: ')
		# ic(type(results_string))
		result_tuples = ast.literal_eval(results_string[1].strip())
		# ic(f'Tuples to list : {result_tuples}')
		# sys.stdout.flush()
	except Exception as e:
		# ic('Error found')
		# ic(e)
		# print(e)
		# # sys.stdout.flush()
		# results_string = ast.literal_eval(db_results.strip())
		if len(results_string) < 2:
			results_string[0] = 'No data returned'
		else:
			results_string[1] = stdout.decode('utf-8')
			clean_string = ''.join(char for char in results_string[1].strip() if char in string.printable)
			# ic(clean_string)
			result_tuples = clean_string.split('The results: ')
			# ic(result_tuples[1])
			# extracted_string = ast.literal_eval(clean_string)
			# ic(extracted_string)
			# sys.stdout.flush()
			
	# for element in result_tuples:
	# 	ic('the elements')
	# 	ic(element)
	# 	sys.stdout.flush()
	# messagebox.showinfo('test', db_results)
	# print(f'db_results: {db_results}')
	# print(f'STDOUT: {stdout.decode()}')
	# sys.stdout.flush()
	# print(f'Length of results = {len(db_results)}')
	# sys.stdout.flush()
	# print(f'STDERR: {stderr.decode()}')
	# sys.stdout.flush()
	# print(f'Return Code: {return_code}')
	# sys.stdout.flush()

'''	
	index = 0
	# get the stdout data line by line
	while True:
		line = await process.stdout.readline()
		if not line:
			# no more lines available
			break

		# process the stdout data
		if line != '':
			index += 1
			if index == 1:
				print('starting')

			# format the line into a string
			linestring = line.decode('utf-8')

			# linestring = line
			linestring = linestring.strip()
			# remove trailing ',\r\n'
			if linestring[-1:] == ',':
				print('removing the \',\'')
				linestring = linestring[:-1]
			print(f'linestring last character: {linestring[-1:]}')
			print(f'linestring: {linestring}')
			# print()
			# split the string into a list
			linelist = linestring.strip().split(', ')

			# if index == 2:
			# 	for char in linestring:
			# 		print(f'Character code for {char} is {ord(char)}')
			# 	print(len(linelist))
			# 	# print(f'linelist[3] = |{linelist[3]}|')
			# 	# print(f'linelist[3] length = {len(linelist[3])}')
			# 	print(f'linelist[2] = {linelist[2]}')
			# 	print(f'length of linelist[2] = {len(linelist[2])}')
			# 	print(f'last character in linelist[2] = {linelist[2][-1:]}')
			# 	if linelist[2][-1:] == ',':
			# 		linelist[2] = linelist[2][:-1]
			# 		print('success')

			# if linelist[2][len(linelist[2])-1] == ',':
			# 	linelist[2] = linelist[2][:-1]

			print(f'linelist: {linelist}')
			print()
			# append the linelist to a list of lists
			linelistlist.append(linelist)

	# print(f'line: {linelistlist}: {len(linelist)};   {len(linelistlist)}')

	# drop the last and first items
	# they do not contain a valid list item
	# print()
	# print(f'Length of list of lists:  {len(linelistlist)}')
	# print()

	print(len(linelistlist))
	
	# del linelistlist[16]
	# del linelistlist[0]
	print()
	print(f'list of lists: {linelistlist}: {len(linelistlist)}')
	print()
	print(f'{linelistlist[0]}')
	print()

	# my_list = [['one', 'two', 'three'], ['four', 'five', 'six'], ['seven', 'eight', 'nine']]
	# print()
	# print(my_list)
	# print(my_list[1])

	# print()
	# print(f'first item: {linelist[0]}')
	# print(f'third item: {linelist[2]}')

	await process.wait()

	# run the external script
	# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	# stdout, stderr = process.communicate()
	
	# call_process_stdout(stdout)
'''

def call_process_stdout():
	global result_tuples

	# check to see if result_tuples exists
	try:
		if len(result_tuples) <= 0:
			messagebox.showinfo('Tic Tac Toe', 'No results to process')
			return
	except Exception as e:
		messagebox.showinfo('Tic Tac Toe', f'An error was encounter with the results:\n{e}')
		return

	# if process.returncode != 0:
	# 	print('an error occurred')

	# print('back from external process')

	# print('processing')

	# for element in result_tuples:
	# 	print(f'{element}')

	# sys.stdout.flush()
	# ic(type(result_tuples))
	# ic(len(result_tuples[0]))
	if len(result_tuples[0]) == 4:
		mode = 1
	else:
		mode = 0


	# print(f'going to process, mode = {mode}')
	# sys.stdout.flush()

	ri.results_window(result_tuples, mode)
	
	# del stdout[0]
	# linestring = line.decode('utf-8')
	# linelist.append(linestring.strip())

	# print(f'linestring: {linestring.strip()}')


	# print(f'stdout slice: {stdout[1:]}')
	# stdout.replace('\0', '')
	# stdstring = stdout
	# print(f'stdstring: {stdstring}')
	# print(f'stdstring slice: {stdstring[1:]}')

	# # deserialize the result in stdout
	# results = json.loads(stdout.strip())

	# # # find the start of the real list
	# # pos = stdout.find('[[\'')
	# # if pos != -1:
	# # 	games = stdout[pos:]
	# # else:
	# # 	games = stdout

	# games_list = []
	# games_list = results.strip().split('],')

	# for x in range(len(games_list)):
	# 	game = games_list[x]
	# 	game = game.replace('[[', '')
	# 	game = game.replace(' [', '')
	# 	game = game.replace(']]', '')
	# 	game = game.replace('] ', '')
	# 	print(game)

	# display the output in the text widget
	# pos = stdout.find('|')
	# if pos != -1:
	# 	name_string= stdout[pos+1:]
	# else:
	# 	name_string = 'None None'


# def games_played():
# 	print('A lot!')


def get_player_names():
	global x_player_name
	global o_player_name

	# define the program to be called
	command = ['python', 'my_get_names.py']

	# run the external script
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	stdout, stderr = process.communicate()

	# ic(stdout)
	# sys.stdout.flush()
	
	# display the output in the text widget
	pos = stdout.find('|')
	if pos != -1:
		name_string= stdout[pos+1:]
	else:
		name_string = 'None None'

	names = []
	names = name_string.split()
	# x_player_name_entry.insert(0, names[0])
	# o_player_name_entry.insert(0, names[1])
	x_player_name.config(text= names[0])
	o_player_name.config(text=names[1])


def fix_db():
# 	ic('enter fix db')
# 	sys.stdout.flush()

	# asyncio.run(call_fix_db())

	tk_db.db_window()
	

# async def call_fix_db():
# 	# run the external program
# 	process = await asyncio.create_subprocess_exec(
# 		'python', 'my_database.py',
# 		stdout=asyncio.subprocess.PIPE,
# 		stderr=asyncio.subprocess.PIPE
# 		)

# 	return_code = process.returncode

# 	ic('leaving call fix db')
# 	sys.stdout.flush()


# ic('start widgets build')
# sys.stdout.flush()

# clear the count values
global result_tuples

result_tuples = []

clear_the_count_values()
winner = False
linelist = []
linelistlist = []

# create the main frame
main_frame = Frame(root, bg='#C0C0C0')
main_frame.pack()

# create a toolbar frame
toolbar_frame = Frame(main_frame, bg='#C0C0C0')
toolbar_frame.pack(pady=(5, 0))

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add games menu
games_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Games', menu=games_menu)
# games_won_menu = Menu(games_menu, tearoff=0)
# games_menu.add_cascade(label='Games Won', menu=games_won_menu)
# games_won_menu.add_command(label='Total Wins', command=games_won)
# games_won_menu.add_command(label='Against Opponent', command=games_won)
# games_menu.add_command(label='Total Games', command=lambda: games_played(player))
# games_menu.add_command(label='Games Won', command=games_won)
# games_menu.add_command(label='Against A Player', command=new_file)
# games_menu.add_command(label='Against All', command=open_file)
# games_menu.add_command(label='Save', command=save_file)
# games_menu.add_command(label='Save As...', command=save_as_file)
# games_menu.add_separator()
# games_menu.add_command(label='Print File', command=print_file)
# games_menu.add_separator()
games_menu.add_command(label='Exit', command=root.quit)

# add edit menu
# edit_menu = Menu(my_menu, tearoff=0)
# my_menu.add_cascade(label='Edit', menu=edit_menu)
# edit_menu.add_command(label='Cut', command=lambda: cut_text(False), accelerator='(Ctrl+x)')
# edit_menu.add_command(label='Copy', command=lambda: copy_text(False), accelerator='(Ctrl+c)')
# edit_menu.add_command(label='Paste             ', command=lambda: paste_text(False), accelerator='(Ctrl+v)')
# edit_menu.add_separator()
# edit_menu.add_command(label='Undo', command=my_text.edit_undo, accelerator='(Ctrl+z)')
# edit_menu.add_command(label='Redo', command=my_text.edit_redo, accelerator='(Ctrl+y)')
# edit_menu.add_separator()
# edit_menu.add_command(label='Select All', command=lambda: select_all(True), accelerator='(Ctrl+a)')
# edit_menu.add_command(label='Clear', command=lambda: clear_all(True), accelerator='(Ctrl+d)')

# add color menu
# color_menu = Menu(my_menu, tearoff=0)
# my_menu.add_cascade(label='Colors', menu=color_menu)
# color_menu.add_command(label='Selected Text', command=text_color)
# color_menu.add_command(label='All Text', command=all_text_color)
# color_menu.add_command(label='Background', command=bg_color)

# add options menu
# global check_state

# check_state = IntVar()
# options_menu = Menu(my_menu, tearoff=0)
# my_menu.add_cascade(label='Options', menu=options_menu)
# options_menu.add_checkbutton(label='Night Mode', variable=check_state, command=night_mode)
# options_menu.add_command(label='Night Mode Off', command=new_file)
# options_menu.add_command(label='Open', command=open_file)

# add status bar
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# create game frame
game_frame = Frame(main_frame)
game_frame.pack(pady=(5, 0))

# build our buttons
b1 = Button(game_frame, name='b1', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b1, 'b1'))
b2 = Button(game_frame, name='b2', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b2, 'b2'))
b3 = Button(game_frame, name='b3', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b3, 'b3'))

b4 = Button(game_frame, name='b4', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b4, 'b4'))
b5 = Button(game_frame, name='b5', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b5, 'b5'))
b6 = Button(game_frame, name='b6', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b6, 'b6'))

b7 = Button(game_frame, name='b7', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b7, 'b7'))
b8 = Button(game_frame, name='b8', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b8, 'b8'))
b9 = Button(game_frame, name='b9', text=' ', font=("Helvetica", 20), height=3, width=6, bg='SystemButtonFace', command=lambda: b_click(b9, 'b9'))

# place buttons on the screen using grid
b1.grid(row=0, column=0)
b2.grid(row=0, column=1)
b3.grid(row=0, column=2)

b4.grid(row=1, column=0)
b5.grid(row=1, column=1)
b6.grid(row=1, column=2)

b7.grid(row=2, column=0)
b8.grid(row=2, column=1)
b9.grid(row=2, column=2)

# create the name labels and entry boxes
x_player_name_label = Label(toolbar_frame, text='X Player:')
o_player_name_label = Label(toolbar_frame, text='O Player:')

x_player_name_label.grid(row=0, column=0, padx=(5, 0))
o_player_name_label.grid(row=1, column=0, padx=(5, 0))

# x_player_name_entry = Entry(toolbar_frame)
# o_player_name_entry = Entry(toolbar_frame)

# x_player_name_entry.grid(row=0, column=1, padx=(5, 0))
# o_player_name_entry.grid(row=1, column=1, padx=(5, 0))

x_player_name = Label(toolbar_frame, width=20)
o_player_name = Label(toolbar_frame, width=20)

x_player_name.grid(row=0, column=1, padx=(5, 0))
o_player_name.grid(row=1, column=1, padx=(5, 0))

# create games button
games_button = Button(toolbar_frame, text='Games Info', width=8, command=games_info)
games_button.grid(row=0, column=2, padx=(5, 0))

# create get names button
player_names_button = Button(toolbar_frame, text='Get Names', width=8, command=get_player_names)
player_names_button.grid(row=0, column=3, padx=(5, 0))

# print the info
print_info_button = Button(toolbar_frame, text='Print Info', width=8, command=call_process_stdout)
print_info_button.grid(row=1, column=2, padx=(5, 0))

# fix db button
fix_db_button = Button(toolbar_frame, text='Fix DB', width=8, command=fix_db)
fix_db_button.grid(row=1, column=3, padx=(5, 0))

# ic('end widgets build')
# sys.stdout.flush()

# xplayeer, oplayer = get_player_names()

# print(xplayer)
# print(oplayer)





if __name__ == "__main__":
    root.mainloop()
