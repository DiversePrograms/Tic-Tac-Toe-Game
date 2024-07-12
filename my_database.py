from tkinter import *
import sqlite3
import my_results as ri
import re
import icecream
from tkinter import messagebox
from icecream import ic
import sys
import os

os.system('clear')

# ic('starting my database')
# sys.stdout.flush()


def init_db():
	# create (and/or connect to) a database with a cursor
	conn = sqlite3.connect('tictactoe.db')

	# creat a cursor
	c = conn.cursor()

	# five datatypes in a table
	# 	text (string)
	# 	integers
	# 	decimal
	# 	null
	# 	blob

	# If table does not exist, create it.
	sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='results'"
	c.execute(sql_query)
	result = c.fetchone()

	if result is None:
		c.execute('''
				CREATE TABLE results (
					x_player text,
					o_player text,
					outcome text
					)
				''')

		# messagebox.showinfo('my_database', 'results table created in tictactoe')
	else:
		sql_query = 'SELECT * FROM results'
		c.execute(sql_query)
		result = c.fetchall()

		found_records = []
		for record in result:
			found_records.append(record)
			# print_records += str(record[0]) + '\t' + str(record[1]) + ' ' + str(record[2]) + '\n'

		# messagebox.showinfo('tictactoe', found_records)


def submit(mode, player='', opponent='', result=''):
	global x_player
	global o_player
	global outcome
	global init_db

	# make sure table is created
	# init_db()
	init_db()

	# connect to the database with a cursor
	conn = sqlite3.connect('tictactoe.db')
	c = conn.cursor()

	# # five datatypes in a table
	# # 	text (string)
	# # 	integers
	# # 	decimal
	# # 	null
	# # 	blob

	# # If table does not exist, create it.
	# sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='results'"
	# c.execute(sql_query)
	# result = c.fetchone()

	# if result is None:
	# 	c.execute('''
	# 			CREATE TABLE results (
	# 				x_player text,
	# 				o_player text,
	# 				outcome text,
	# 				mark text
	# 				)
	# 			''')

	# messagebox.showinfo('The DB', f'{x_player}, {o_player}, {outcome}')
	# insert record into the database
	if mode == 0:
		# ic(f'X Player: {x_player.get()}')
		# ic(f'O Player: {o_player.get()}')
		# ic(f'Outcome: {outcome.get()}')
		# sys.stdout.flush()

		c.execute('INSERT INTO results VALUES(:x_name, :o_name, :outcome)',
				{
					'x_name': x_player.get(),
					'o_name': o_player.get(),
					'outcome': outcome.get(),
				}
			)

		x_player.delete(0, END)
		o_player.delete(0, END)
		outcome.delete(0, END)
	elif mode == 1:
		# ic(f'PLayer: {player}')
		# ic(f'Opponent: {opponent}')
		# ic(f'Result: {result}')
		# sys.stdout.flush()

		c.execute("INSERT INTO results VALUES(:x_name, :o_name, :outcome)",
				{
					'x_name' : player,
					'o_name' : opponent,
					'outcome': result,
				}
			)
	else:
		# we shouldn't be here
		messagebox.showerror('My Database', 'Invalid mode!')
		conn.close()
		return

	# commit changes to the database
	conn.commit()

	# close the database
	conn.close()


def query(the_player, the_opponent='', the_outcome='', the_mark=''):
	# condition the arguments
	player = the_player.strip()
	opponent = the_opponent.strip()
	outcome = the_outcome.strip()
	mark = the_mark.strip()

	# msg = f'Received Parameter:\nplayer = {player}\nopponent = {opponent}\noutcome = {outcome}\nmark = {mark}'

	# messagebox.showinfo('My Database', msg)

	# make sure the table exists
	init_db()

	# connect to the database with a cursor
	conn = sqlite3.connect('tictactoe.db')

	c = conn.cursor()

	# 28 query types
	# 	(1)  all games | player = '', opponent = '', outcome = '', mark =''
	#
	#   (2)  all win games | player = '', opponent = '', outcome = 'win', mark =''
	#   (3)  all lose games | player = '', opponent = '', outcome = 'lose', mark =''
	#   (4)  all draw games | player = '', opponent = '', outcome = 'draw', mark =''
	#
	# 	(5)  all player games | player = '<player>', opponent = '', outcome = '', mark =''
	#
	# 	(6)  player win games | player = '<player>', opponent = '', outcome = 'win', mark =''
	#   (7)  player lose games | player = '<player>', opponent = '', outcome = 'lose', mark =''
	# 	(8)  player draw games | player = '<player>', opponent = '', outcome = 'draw', mark =''
	#
	#   (9)  all player as x games | player = '<player>', opponent = '', outcome = '', mark ='x'
	#
	#   (10) all player as x win games | player = '', opponent = '', outcome = 'win', mark ='x'
	#   (11) all player as x lose games | player = '', opponent = '', outcome = 'lose', mark ='x'
	#   (12) all player as x draw games | player = '', opponent = '', outcome = 'draw', mark ='x'
	#
	#   (13) all player as o games | player = '', opponent = '', outcome = '', mark ='o'
	#
	#   (14) all player as o win games | player = '', opponent = '', outcome = 'win', mark ='o'
	#   (15) all player as o lose games | player = '', opponent = '', outcome = 'lose', mark ='o'
	#   (16) all player as o draw games | player = '', opponent = '', outcome = 'draw', mark ='o'
	#
	#   (17) player against opponent games | player = '<player>', opponent = '<opponent>', outcome = '', mark =''
	#
	# 	(18) player win games against opponent | player = '<player>', opponent = '<opponent>', outcome = 'win', mark =''
	#   (19) player lose games against opponent | player = '<player>', opponent = '<opponent>', outcome = 'lose', mark =''
	#   (20) player draw games against opponent | player = '<player>', opponent = '<opponent>', outcome = 'draw', mark =''
	#   ----------------------------------
	#   //all x games | player = '', opponent = '', outcome = '', mark ='x'
	#   (21) all x win games | player = '', opponent = '', outcome = 'win', mark ='x'
	#   all x lose games | player = '', opponent = '', outcome = 'lose', mark ='x'
	#   all x draw games | player = '', opponent = '', outcome = 'draw', mark ='x'
	#   all player against opponent any outcome as x
	#   all o games player = '', opponent = '', outcome = '', mark ='o'
	#   all o win games player = '', opponent = '', outcome = 'win', mark ='o'
	#   all o lose games player = '', opponent = '', outcome = 'lose', mark ='o'
	#   all o draw games player = '', opponent = '', outcome = 'draw', mark ='o'
	#   all player against opponent any outcome as o

	# msg = f'player: {player}, opponent: {opponent}, outcome: {outcome}, mark: {mark}'
	# messagebox.showinfo('The DB', msg)
	
	# set up the query
	sql_query = ''
	if player == '' and opponent == '' and outcome == '' and mark =='':
		# all games
		sql_query = 'SELECT oid, * FROM results'
		c.execute(sql_query)
	elif player == '' and opponent == '' and outcome != '' and mark =='':
		# all games with an outcome		sql_query = f'SELECT oid, * results WHERE outcome = ?'
		c.execute(sql_query, (outcome))
	elif player != '' and opponent == '' and outcome == '' and mark =='':
		# all player games
		sql_query = f'SELECT oid, * FROM results WHERE x_player = ? OR o_player = ?'
		c.execute(sql_query, (player, player))
	elif player != '' and opponent == '' and outcome != '' and mark =='':
		# all player games with an outcome
		sql_query = f'SELECT oid, * FROM results WHERE (x_player = ? OR o_player = ?) AND outcome = ?'
		c.execute(sql_query, (player, player, outcome))
	elif player != '' and opponent == '' and outcome == '' and mark =='x':
		# all player games as x player
		sql_query = f'SELECT oid, * FROM results WHERE x_player = ?'
		c.execute(sql_query, (player))
	elif player != '' and opponent == '' and outcome != '' and mark == 'x':
		# all player games as x player with an outcome
		sql_query = f'SELECT oid, * FROM results WHERE x_player = ? AND outcome = ?'
		c.execute(sql_query, (player, outcome))
	elif player != '' and opponent == '' and outcome == '' and mark == 'o':
		# all player games as o player
		sql_query = f'SELECT oid, * FROM results WHERE o_player = ?'
		c.execute(sql_query, (player))
	elif player != '' and opponent == '' and outcome != '' and mark == 'o':
		# all player games as o player with an outcome
		sql_query = f'SELECT oid, * FROM results WHERE o_player = ? AND outcome = ?'
		c.execute(sql_query, (player, outcome))
	elif player != '' and opponent != '' and outcome == '' and mark == '':
		# all player against opponent games
		sql_query = f'''
		SELECT oid, * FROM results
		WHERE (x_player = ? AND o_player = ?)
		OR (x_player = ? AND o_player = ?)
		'''
		c.execute(sql_query, (player, opponent, opponent, player))
	elif player != '' and opponent != '' and outcome != '' and mark =='':
		# all player against opponent with an outcome
		sql_query = f'''
		SELECT oid, * FROM results
		WHERE ((x_player = ? AND o_player = ?)
		OR (x_player = ? AND o_player = ?)) AND outcome = ?
		'''
		c.execute(sql_query, (player, opponent, opponent, player, outcome))
	elif player == '' and opponent == '' and outcome != '' and mark == '':
		# all games according to an outcome
		sql_query = f'''
		SELECT oid, * FROM results
		WHERE outcome = ?
		'''
		c.execute(sql_query, (outcome))
	# elif player == '' and opponent == '' and outcome == '' and mark == 'o':
	# 	# all x games
	# 	sentry = 12
	# 	sql_query = f'SELECT * FROM results WHERE mark = ?, ({mark})'
	# elif player == '' and opponent == '' and outcome != '' and mark == 'o':
	# 	# all x games with an outcome
	# 	sentry = 13
	# 	sql_query = f'SELECT * FROM results WHERE outcome = ? AND mark = ?, ({outcome}, {mark})'
	# elif player != '' and opponent != '' and outcome != '' and mark != '':
	# 	# all games player against opponent with an outcome any mark
	# 	sentry = True
	# 	sql_query = f'''
	# 	SELECT * FROM results
	# 	WHERE (x_player = ? AND o_player = ?) OR (x_player = ? AND o_player = ?) AND outcome = ?,
	# 	({player}, {opponent}, {opponent}, {player}, {outcome})
	# 	'''
	elif player != '' and opponent != '' and outcome != '' and mark == 'x':
		# player games against opponent with an outcome and mark is x
		# messagebox.showinfo('The DB', 'query for x')
		sql_query = f'''
		SELECT oid, * FROM results
		WHERE x_player = ? AND o_player = ? AND outcome = ?
		'''
		# messagebox.showinfo('The DB', 'back from query')
		c.execute(sql_query, (player, opponent, outcome))
		# messagebox.showinfo('The DB', 'executed query')
	elif player != '' and opponent != '' and outcome != '' and mark == 'o':
		# player games against opponent with an outcome and mark is o
		sql_query = f'''
		SELECT oid, * FROM results
		WHERE x_player = ? AND o_player = ? AND outcome = ?
		'''
		c.execute(sql_query, (opponent, player, outcome))
	else:
		messagebox.showerror('My Database', 'No parameters or mismatched parameters received!')

	# messagebox.showinfo('The DB', 'query created')

	# query = "SELECT name FROM sqlite_master WHERE type='table' AND name='results'"
	# c.execute(query)
	# result = c.fetchone()

	# messagebox.showinfo('tictactoe', result)

	# sentry = True
	# sql_query = f'''
	# SELECT * FROM results WHERE x_player = ? OR o_player = ?
	# '''

	# if sentry:
	# 	c.execute(sql_query, (player, player))

	# if o_player == '':
	# 	# player against player2
	# 	sql_query = "SELECT * FROM results WHERE (x_player=? OR o_player=?) AND (x_player=? OR o_player=?)"
	# 	c.execute(sql_query, (player1, player1, player2, player2))
	# else:
	# 	# player1 against anybody
	# 	sql_query = "SELECT * FROM results WHERE x_player=? OR o_player=?"
	# 	c.execute(sql_query, (player1, player1))

	records = c.fetchall()

	# c.fetchone()      - get 1 record
	# c.fetchmany(20)   - get 20 records

	# make a list of returned records
	found_records = []
	index = 0
	for record in records:
		found_records.append(record)
		# print_records += str(record[0]) + '\t' + str(record[1]) + ' ' + str(record[2]) + '\n'

	# commit changes to the database
	# conn.commit()

	# close the database
	conn.close()

	# return the record
	# print(f'DB fournd: {found_records}')
	# messagebox.showinfo('The DB', 'send found records back')
	return found_records


def db_window():
	global init_db

	root = Tk()
	root.title('The Database')
	root.iconbitmap('VariedLogo.ico')
	# root.geometry('380x400')

	my_window_width = 400
	my_window_height = 200
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


	# def save():
	# 	# connect to the database with a cursor
	# 	conn = sqlite3.connect('tictactoe.db')
	# 	c = conn.cursor()

	# 	# record_id = select_oid.get()

	# 	c.execute('''
	# 		UPDATE results SET
	# 			x_player = :field1_data,
	# 			o_player = :field2_data,
	# 			outcome = :field3_data

	# 			WHERE oid = :oid''',
	# 			{
	# 				'field1_data' : x_player.get().strip(),
	# 				'field2_data' : o_player.get().strip(),
	# 				'field3_data' : outcome.get().strip(),
	# 				'oid' : record_id
	# 			})

	# 	# commit changes to the database
	# 	conn.commit()

	# 	# close the database
	# 	conn.close()

	# 	updater.destroy()


	def doevents():
		root.update_idletasks()
		updater.update_idletasks()


	def do_update():
		response = update()

		# messagebox.showinfo('The DB', f'back from the updater:\n{response}')

		# updater.destroy()

		root.lift()
		root.attributes('-topmost', True)
		# root.after_idle(updater.attributes, '-topmost', False)
		root.focus_force()

		# if updater.winfo_exists():
		# 	doevents()
		# 	updater.destroy()
		# else:
		# 	messagebox.showinfo('The DB', 'updater is not visible')

		# updater.destroy()


	def update():
		global updater
		global record_id
		global x_name_updater
		global o_name_updater
		global outcome_updater
		
		# updater = Tk()
		# updater.title('Update A Record')
		# updater.iconbitmap('VariedLogo.ico')
		# updater.geometry('380x200')

		# ic('updating...')
		# sys.stdout.flush()

		# create a database with a cursor
		conn = sqlite3.connect('tictactoe.db')
		c = conn.cursor()

		records = list()
		record_id = select_oid.get()  # make sure there is only one oid
		record_id_list = list()
		record_id_list = record_id.split(', ')

		# ic(f'record to update: {record_id_list}')
		# sys.stdout.flush()

		if len(record_id_list) != 1:
			messagebox.showerror('The DB', 'Error in number of oid listed!\nPlease check that only 1 oid is entered.')
			conn.close()
			return False

		if record_id_list[0] == '':
			messagebox.showerror('The DB', 'No record to update!\nPlease check your oid entry.')
			conn.close()
			return False

		# check to see what fields are to be updated
		# 7
		if x_player.get().strip() != '' and o_player.get().strip() != '' and outcome.get().strip() != '':
			sql_cmd = f'''
			UPDATE results SET
				x_player = ?,
				o_player = ?,
				outcome = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (x_player.get().strip(), o_player.get().strip(), outcome.get().strip(), select_oid.get().strip())) 

		# 6
		if x_player.get().strip() != '' and o_player.get().strip() != '' and outcome.get().strip() == '':
			sql_cmd = f'''
			UPDATE results SET
				x_player = ?,
				o_player = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (x_player.get().strip(), o_player.get().strip(), select_oid.get().strip())) 

		# 5
		if x_player.get().strip() != '' and o_player.get().strip() == '' and outcome.get().strip() != '':
			sql_cmd = f'''
			UPDATE results SET
				x_player = ?,
				outcome = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (x_player.get().strip(), outcome.get().strip(), select_oid.get().strip())) 

		# 4
		if x_player.get().strip() != '' and o_player.get().strip() == '' and outcome.get().strip() == '':
			sql_cmd = f'''
			UPDATE results SET
				x_player = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (x_player.get().strip(), select_oid.get().strip())) 

		# 3
		if x_player.get().strip() == '' and o_player.get().strip() != '' and outcome.get().strip() != '':
			sql_cmd = f'''
			UPDATE results SET
				o_player = ?,
				outcome = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (o_player.get().strip(), outcome.get().strip(), select_oid.get().strip())) 

		# 2
		if x_player.get().strip() == '' and o_player.get().strip() != '' and outcome.get().strip() == '':
			sql_cmd = f'''
			UPDATE results SET
				o_player = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (o_player.get().strip(), select_oid.get().strip())) 

		# 1
		if x_player.get().strip() == '' and o_player.get().strip() == '' and outcome.get().strip() != '':
			sql_cmd = f'''
			UPDATE results SET
				outcome = ?
			WHERE oid = ?
			'''
			c.execute(sql_cmd, (outcome.get().strip(), select_oid.get().strip())) 

		# 0
		if x_player.get().strip() == '' and o_player.get().strip() == '' and outcome.get().strip() == '':
			conn.close()
			messagebox.showinfo('The DB', 'No fields to change!\nNothing was updated.')
			return True
		
		conn.commit()
		conn.close()

		return True


		# c.execute('''
		# 	UPDATE results SET
		# 		x_player = :field1_data,
		# 		o_player = :field2_data,
		# 		outcome = :field3_data

		# 		WHERE oid = :oid''',
		# 		{
		# 			'field1_data' : x_player.get().strip(),
		# 			'field2_data' : o_player.get().strip(),,
		# 			'field3_data' : outcome.get().strip(),
		# 			'oid' : record_id
		# 		})


		# x_name_updater = Entry(updater, width=40)
		# x_name_updater.grid(row=0, column=1, pady=(10, 0))
		# o_name_updater = Entry(updater, width=40)
		# o_name_updater.grid(row=1, column=1)
		# outcome_updater = Entry(updater, width=40)
		# outcome_updater.grid(row=2, column=1)

		# x_name_label = Label(updater, text='First Name: ', width=10, anchor=W)
		# x_name_label.grid(row=0, column=0, padx=10, sticky=E+W, pady=(10, 0))
		# o_name_label = Label(updater, text='Last Name: ', width=10, anchor=W)
		# o_name_label.grid(row=1, column=0, padx=10, sticky=E+W)
		# outcome_label = Label(updater, text='Address: ', width=10, anchor=W)
		# outcome_label.grid(row=2, column=0, padx=10, sticky=E+W)

		# for record in records:
		# 	x_name_updater.insert(0, record[0])
		# 	o_name_updater.insert(0, record[1])
		# 	outcome_updater.insert(0, record[2])

		# update_btn = Button(updater, text='Save Record', command=save)
		# update_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=20, ipadx=141)


	def delete():
		# create a database with a cursor
		conn = sqlite3.connect('tictactoe.db')
		c = conn.cursor()

		# get the list of oids from the display
		oid_string = select_oid.get()
		# ic(oid_string)
		# ic(type(oid_string))
		# oid_list = oid_string.split(',', ', ')
		oid_list = re.split(r'[, ]+', oid_string)
		oid_list.sort(reverse=True)
		# ic(oid_list)
		# ic(oid_list)
		# sys.stdout.flush()

		if check_oid_list(oid_list):
			for oid in oid_list:
				c.execute('DELETE FROM results WHERE oid = ' + oid)

			# commit changes to the database
			conn.commit()

			refresh_oid('tictactoe.db', 'results')

		# clear the oid entry
		select_oid.delete(0, END)

		# close the database
		conn.close()


	def check_oid_list(oid_list):
		if len(oid_list) == 0:
			return False

		new_list = []
		for oid in oid_list:
			if bool(re.match(r'^-?\d+$', oid)):
				new_list.append(oid)

		if len(new_list) == 0:
			return False
		else:
			return True


	def show_records():
		# open the database with a cursor
		conn = sqlite3.connect('tictactoe.db')

		c = conn.cursor()

		# get the records
		c.execute('SELECT oid,* FROM results')
		records = c.fetchall()

		# c.fetchone()      - get 1 record
		# c.fetchmany(20)   - get 20 records

		# commit changes to the database
		# conn.commit()

		# close the database
		conn.close()

		# display results
		ri.results_window(records, 1)
		

	def refresh_oid(database, table_name):
		# connect to the database
		conn = sqlite3.connect('tictactoe.db')
		# create a cursor
		c = conn.cursor()

		# define the temporary table name
		temp_table = f'{table_name}_temp'

		# get the table schema
		# query_str = f'SELECT sql FROM sqlite_master WHERE type=\'table\' AND name=\'{table_name}\''
		# ic(query_str)
		# sys.stdout.flush()

		c.execute(f'SELECT sql FROM sqlite_master WHERE type=\'table\' AND name=\'{table_name}\'')
		# sql_return = c.fetchone()
		# ic(sql_return)
		# sys.stdout.flush()

		create_table_sql = c.fetchone()[0]

		# modify the schema to create the temporary table
		create_temp_table_sql = create_table_sql.replace(table_name, temp_table)
		c.execute(create_temp_table_sql)

		# insert data into the temporary table
		c.execute(f'INSERT INTO {temp_table} SELECT * FROM {table_name}')

		# drop the original table
		c.execute(f'DROP TABLE {table_name}')

		# rename the temporary table to the original table name
		c.execute(f'ALTER TABLE {temp_table} RENAME TO {table_name}')

		# commit and close
		conn.commit()
		conn.close()


	global x_player
	global o_player
	global outcome

	# create menu
	my_menu = Menu(root)
	root.config(menu=my_menu)

	# add games menu
	games_menu = Menu(my_menu, tearoff=0)
	my_menu.add_cascade(label='Games', menu=games_menu)
	games_menu.add_command(label='Refresh Table', command=lambda: refresh_oid('tictactoe.db', 'results'))
	games_menu.add_separator()
	games_menu.add_command(label='Exit', command=root.quit)

	# create entry boxes and associated labels
	x_player_label = Label(root, text='X Player', width=10)
	x_player_label.grid(row=0, column=0, padx=10, pady=(10, 0))
	x_player = Entry(root, width=10)
	x_player.grid(row=1, column=0, pady=(10, 0))

	o_player_label = Label(root, text='O player', width=10)
	o_player_label.grid(row=0, column=1, padx=10, pady=(10, 0))
	o_player = Entry(root, width=10)
	o_player.grid(row = 1, column=1, pady=(10, 0))

	outcome_label = Label(root, text='Outcome', width=10)
	outcome_label.grid(row=0, column=2, padx=10, pady=(10, 0))
	outcome = Entry(root, width=10)
	outcome.grid(row=1, column=2, pady=(10, 0))

	select_oid_label = Label(root, text='Select OID\'s', width=10)
	select_oid_label.grid(row=2, column=0, padx=10, pady=(10, 0))
	select_oid = Entry(root, width=40)
	select_oid.grid(row=2, column=1, columnspan=2, pady=(10, 0))

	# create submit button
	submit_btn = Button(root, text='Add Record to Database', command=lambda: submit(0))
	submit_btn.grid(row=4, column=0, columnspan=3, padx=(10, 0), pady=(10, 0))

	# create update button
	update_btn = Button(root, text='Update Record', command=do_update)
	update_btn.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))

	# create query button
	show_records_btn = Button(root, text='Show Records', command=show_records)
	show_records_btn.grid(row=3, column=1, padx=(10, 0), pady=(10, 0))

	delete_btn = Button(root, text='Delete Bad Records', command=delete)
	delete_btn.grid(row=3, column=2, padx=(10, 0), pady=(10, 0))







if __name__ == "__main__":
    root.mainloop()

