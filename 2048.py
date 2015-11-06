import random
import time
import tkinter

class Board:
	def __init__(self):
		self.board = []
		for row in range(4):
			new_row = []
			for col in range(4):
				new_row.append(Piece(0, row, col))
			self.board.append(new_row)
		self.new_random_piece()
		self.new_random_piece()
		self.quit = False

	def __str__(self):
		string = ""
		for row in self.board:
			col_count = 0
			for piece in row:
				max_col_len = max([len(str(t_piece.value)) for t_piece in [self.get_piece(0, col_count), self.get_piece(1, col_count), self.get_piece(2, col_count), self.get_piece(3, col_count)]])
				i = len(str(piece.value))
				while i < max_col_len:
					string += " "
					i += 1
				string = string + str(piece.value) + " "
				col_count += 1
			string += "\n"
		return string

	def new_random_piece(self):
		row, col, two_or_four = random.randint(0, 3), random.randint(0, 3), random.randint(0, 4)
		piece_to_change = self.get_piece(row, col)
		if piece_to_change.value == 0:
			if two_or_four < 3:
				piece_to_change.set_value(2)
			else:
				piece_to_change.set_value(4)
		else:
			if not self.is_full():
				self.new_random_piece()

	def get_piece(self, row, col):
		return self.board[row][col]

	def set_piece(self, row, col, value):
		self.board[row][col] = Piece(row, col, value)

	def is_full(self):
		full = True
		for row in self.board:
			for piece in row:
				if piece == 0:
					full = False
		return full


class Piece:

	max = 0

	def __init__(self, value, row, col):
		self.value = value
		self.row = row
		self.col = col

	def set_value(self, new_value):
		self.value = new_value
		if new_value > Piece.max:
			Piece.max = new_value


def play_game():
	board = Board()
	screen = tkinter.Tk()
	screen.title('2048')
	screen.geometry("600x600")
	canvas = tkinter.Canvas(screen, bg="#6e6e6e", height=600, width=600)
	canvas.pack()
	display_new(board, screen, canvas)
	def leftKey(event):
		if Piece.max < 2048:
			left_move(board)
			display_new(board, screen, canvas)
		else:
			screen.quit()
	def rightKey(event):
		if Piece.max < 2048:
			right_move(board)
			display_new(board, screen, canvas)
		else:
			screen.quit()
	def upKey(event):
		if Piece.max < 2048:
			up_move(board)
			display_new(board, screen, canvas)
		else:
			screen.quit()
	def downKey(event):
		if Piece.max < 2048:
			down_move(board)
			display_new(board, screen, canvas)
	def quit(event):
		screen.quit()
	screen.bind('<Left>', leftKey)
	screen.bind('<Right>', rightKey)
	screen.bind('<Up>', upKey)
	screen.bind('<Down>', downKey)
	screen.bind('<q>', quit)
	screen.mainloop()
	if Piece.max == 2048:
		canvas_id = canvas.create_text(30, 200, anchor="nw", fill = "black", font = ('Helvetica', '72'))
		canvas.insert(canvas_id, 12, "Congratulations!")
		canvas_id = canvas.create_text(30, 300, anchor="nw", fill = "black", font = ('Helvetica', '26'))
		canvas.insert(canvas_id, 12, "You made it to the 2048 tile!")
	else:
		canvas_id = canvas.create_text(30, 200, anchor="nw", fill = "black", font = ('Helvetica', '72'))
		canvas.insert(canvas_id, 12, "Game Over!")
		canvas_id = canvas.create_text(30, 300, anchor="nw", fill = "black", font = ('Helvetica', '26'))
		string = "You made it to the " + str(Piece.max) + " tile!"
		canvas.insert(canvas_id, 12, string)


def display_new(board, screen, canvas):
	print(board)
	canvas.delete("all")
	y = 20
	for row in board.board:
		x = 20
		for piece in row:
			if piece.value == 0:
				canvas.create_oval(x, y, x + 100, y + 100, fill="#e2e2e2")
			else:
				colors = {2: "#bababa", 4: "#d4c893", 8: "#ffa07a", 16: "#e97e1c", 32: "#f08080", 64: "#c01920", 128: "#f5bd35", 256: "#f5bd35", 512: "#f5bd35", 1024: "#f5bd35", 2048: "#f5bd35"}
				canvas.create_oval(x, y, x + 100, y + 100, fill = colors[piece.value])
				canvas_id = canvas.create_text(x + (50 - (10 * len(str(piece.value)))), y + 30, anchor="nw", fill = "white", font = ('Helvetica', '36'))
				canvas.insert(canvas_id, 12, str(piece.value))
			x += 150
		y += 150
	board.new_random_piece()


def down_move(board):
	pieces_combined = []
	down_helper(board)
	for row in [2, 1, 0]:
		for col in range(4):
			piece, other_piece = board.get_piece(row, col), board.get_piece(row + 1, col)
			if piece.value == other_piece.value and piece not in pieces_combined:
					change_pieces(piece, other_piece, piece.value * 2)
					pieces_combined += [other_piece]
	down_helper(board)


def down_helper(board):
	for row in [2, 1, 0]:
		for col in range(4):	
			piece, other_piece, i = board.get_piece(row, col), board.get_piece(row + 1, col), 2
			while other_piece.value == 0 and (row + i) <= 4:
				change_pieces(piece, other_piece, piece.value)
				if (row + i) < 4:
					piece, other_piece = other_piece, board.get_piece(row + i, col)
				i += 1
	

def up_move(board):
	pieces_combined = []
	up_helper(board)
	for row in [1, 2, 3]:
		for col in range(4):
			piece, other_piece = board.get_piece(row, col), board.get_piece(row - 1, col)
			if piece.value == other_piece.value and piece not in pieces_combined:
					change_pieces(piece, other_piece, piece.value * 2)
					pieces_combined += [other_piece]	
	up_helper(board)


def up_helper(board):
	for row in [1, 2, 3]:
		for col in range(4):	
			piece, other_piece, i = board.get_piece(row, col), board.get_piece(row - 1, col), 2
			while other_piece.value == 0 and (row - i) >= -1:
				change_pieces(piece, other_piece, piece.value)
				if (row + i) > -1:
					piece, other_piece = other_piece, board.get_piece(row - i, col)
				i += 1


def right_move(board):
	pieces_combined = []
	right_helper(board)
	for row in range(4):
		for col in [2, 1, 0]:
			piece, other_piece = board.get_piece(row, col), board.get_piece(row, col + 1)
			if piece.value == other_piece.value and piece not in pieces_combined:
					change_pieces(piece, other_piece, piece.value * 2)
					pieces_combined += [other_piece]
	right_helper(board)


def right_helper(board):
	for row in range(4):
		for col in [2, 1, 0]:	
			piece, other_piece, i = board.get_piece(row, col), board.get_piece(row, col + 1), 2
			while other_piece.value == 0 and (col + i) <= 4:
				change_pieces(piece, other_piece, piece.value)
				if (col + i) < 4:
					piece, other_piece = other_piece, board.get_piece(row, col + i)
				i += 1


def left_move(board):
	pieces_combined = []
	left_helper(board)
	for row in range(4):
		for col in [1, 2, 3]:
			piece, other_piece = board.get_piece(row, col), board.get_piece(row, col - 1)
			if piece.value == other_piece.value and piece not in pieces_combined:
					change_pieces(piece, other_piece, piece.value * 2)
					pieces_combined += [other_piece]	
	left_helper(board)


def left_helper(board):
	for row in range(4):
		for col in [1, 2, 3]:
			piece, other_piece, i = board.get_piece(row, col), board.get_piece(row, col - 1), 2
			while other_piece.value == 0 and (col - i) >= -1:
				change_pieces(piece, other_piece, piece.value)
				if (col - i) > -1:
					piece, other_piece = other_piece, board.get_piece(row, col - i)
				i += 1


def change_pieces(old_piece, new_piece, new_value):
	new_piece.set_value(new_value)
	old_piece.set_value(0)


play_game()