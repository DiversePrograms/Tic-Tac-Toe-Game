from tkinter import *
from icecream import ic
from tkinter import messagebox
from tkinter import ttk
import time
import sys
import os

os.system('clear')


def results_window(results, mode):
	# mode = 1 for tuple
	# mode = 0 for string
	root = Tk()
	root.title('DB Results')
	root.iconbitmap('VariedLogo.ico')

	# in order to get the vertical scrollbar to show, width has to be at least 400
	my_window_width = 760
	my_window_height = 300
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x = int((screen_width / 2) - (my_window_width / 2))
	y = int((screen_height / 2) - (my_window_height / 2))
	window_info = (f'{my_window_width}x{my_window_height}+{x}+{y}')
	root.geometry(window_info)

	# need one of the two following statements or windows will place the 
	#   window wherever it wants
	root.resizable(1, 1)    # resizable
	# root.resizable(0, 0)    # not resizable

	root.attributes('-topmost', 1)
	root.configure(bg='#C0C0C0')

	global my_canvas

	# create main frame
	main_frame = Frame(root, bg='#0000FF')
	main_frame.pack(fill=BOTH, expand=1)

	# create a canvas frame
	canvas_frame = Frame(main_frame, bg='#C0C0C0')
	canvas_frame.pack(side=LEFT, fill=BOTH, expand=1)

	# create a canvas
	my_canvas = Canvas(canvas_frame, bg='#C0C0C0')
	my_canvas.pack(side=TOP, fill=BOTH, expand=1)

	# create the vertical scrollbar for the labels
	text_scroll_h = ttk.Scrollbar(canvas_frame, orient=HORIZONTAL, command=my_canvas.xview)
	text_scroll_h.pack(side=BOTTOM, fill=X)

	# create the vertical scrollbar for the labels
	text_scroll_v = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
	text_scroll_v.pack(side=RIGHT, fill=Y)

	# configure the canvas
	my_canvas.configure(yscrollcommand=text_scroll_v.set, xscrollcommand=text_scroll_h.set)
	# ## my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

	# configure the canvas
	# my_canvas.configure(xscrollcommand=text_scroll_h.set)
	# my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

	# create the frame for the labels
	label_frame = Frame(my_canvas, bg='#C0C0C0', width=350)
	
	# add label frame to a window in the canvas
	my_canvas.create_window((0, 0), window=label_frame, anchor='nw')

	my_canvas.bind('<Configure>', on_canvas_configure)

	# print(f'at process, mode = {mode}')
	# sys.stdout.flush()

	if mode == 1:
		# create the grid system
		# place the header row
		header_text = ['OID', 'X Player', 'O Player', 'Outcome']
		header = []
		for i in range(len(header_text)):
			new_header = Label(label_frame, borderwidth=2, relief='raised', font=('Times New Roman', 16))
			header.append(new_header)
			header[i].config(text=header_text[i])
			header[i].grid(row=0, column=i, padx=5, pady=(10, 0), ipadx=10)

		# game result labels
		label = []
		for i, result_field in enumerate(results):  # row index
			# print()
			# print(f'result field {i}: {result_field}')
			# print()
			# ic(len(result_field), result_field)
			# sys.stdout.flush()
			for j in range(len(result_field)):   # field index
				# label width dependent on position
				if j == 0:
					label_width = 5
				elif j == 3:
					label_width = 5
				else:
					label_width = 15

				new_label = Label(label_frame, width=label_width, borderwidth=1, relief='solid', font=('Times New Roman', 20))
				label.append(new_label)
				label_index = i + j + (i * (len(result_field) - 1))
				# ic(i, j, label_index)
				# sys.stdout.flush()
				label[label_index].config(text=result_field[j])
				label[label_index].grid(row=i+1, column=j, padx=5, pady=(10, 0), ipadx=10)
	else:
		no_results = Label(label_frame, borderwidth=2, relief='sunken', bg='#C0C0C0', font=('Times New Roman', 14))
		no_results.config(text=results[1])
		no_results.grid(row=0, column=0, pady=30, padx=10, ipadx=5, ipady=5)
	# create text box
	# wrap values: 'none', 'word', 'char'
	# my_text = Text(my_frame, width=97, height=25, font=('Helvetica', 16), selectbackground='yellow', selectforeground='black', undo=True, yscrollcommand=text_scroll.set, wrap='none')
	# my_text.pack()

# bind the canvas to the scroll region
def on_canvas_configure(event):
	global my_canvas

	my_canvas.configure(scrollregion=my_canvas.bbox('all'))


