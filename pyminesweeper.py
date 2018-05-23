#!/usr/bin/python

'''

	MINE SWEEPER WITH PYGAME
	------------------------
	Python 2.x (macOS 10.13.x)

	THE M.I.T. LICENSE 
	Copyright 2018 Kaz Yoshikawa

	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
	associated documentation files (the "Software"), to deal in the Software without restriction, 
	including without limitation the rights to use, copy, modify, merge, publish, distribute, 
	sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all copies or 
	substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
	BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
	DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

NUM_OF_ROWS = 10
NUM_OF_COLS = 20
NUM_OF_BOMBS = 15

TOP_MARGIN = 64
CELL_SIZE = 32
CELL_WH = (CELL_SIZE, CELL_SIZE)
GAME_STATE_ICON_SIZE = 60

CELL_MINE_0 = 0
CELL_MINE_1 = 1
CELL_MINE_2 = 2
CELL_MINE_3 = 3
CELL_MINE_4 = 4
CELL_MINE_5 = 5
CELL_MINE_6 = 6
CELL_MINE_7 = 7
CELL_MINE_8 = 8
CELL_BOMB = 10

STATUS_UNOPENED = 0x100
STATUS_UNOPENED_QUESTION = 0x200
STATUS_UNOPENED_FLAG = 0x300
STATUS_OPEN = 0x400
STATUS_OPEN_EXPLODED = 0x500

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 3

GAME_STATE_INPLAY = 1
GAME_STATE_OVER = 2
GAME_STATE_COMPLETED = 3

FPS = 30


def load_image(name, size):
	image = pygame.image.load(name)
	image = pygame.transform.scale(image, size)
	return image	


class Cell(pygame.sprite.Sprite):

	image_mine_0 = load_image("0.png", CELL_WH)
	image_mine_1 = load_image("1.png", CELL_WH)
	image_mine_2 = load_image("2.png", CELL_WH)
	image_mine_3 = load_image("3.png", CELL_WH)
	image_mine_4 = load_image("4.png", CELL_WH)
	image_mine_5 = load_image("5.png", CELL_WH)
	image_mine_6 = load_image("6.png", CELL_WH)
	image_mine_7 = load_image("7.png", CELL_WH)
	image_mine_8 = load_image("8.png", CELL_WH)
	image_bomb = load_image("bomb.png", CELL_WH)
	image_unopened = load_image("unopened.png", CELL_WH)
	image_unopened_question = load_image("questionmark.png", CELL_WH)
	image_unopened_flag = load_image("flag.png", CELL_WH)
	image_open_exploded = load_image("bomb2.png", CELL_WH)

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.type = CELL_MINE_0
		self.status = STATUS_UNOPENED
		self.update()

	def cell_image(self):
		if (self.status == STATUS_UNOPENED): return Cell.image_unopened
		elif (self.status == STATUS_UNOPENED_QUESTION): return Cell.image_unopened_question
		elif (self.status == STATUS_UNOPENED_FLAG): return Cell.image_unopened_flag
		elif (self.status == STATUS_OPEN):
			dictionary = {
				CELL_MINE_0 : Cell.image_mine_0,
				CELL_MINE_1 : Cell.image_mine_1,
				CELL_MINE_2 : Cell.image_mine_2,
				CELL_MINE_3 : Cell.image_mine_3,
				CELL_MINE_4 : Cell.image_mine_4,
				CELL_MINE_5 : Cell.image_mine_5,
				CELL_MINE_6 : Cell.image_mine_6,
				CELL_MINE_7 : Cell.image_mine_7,
				CELL_MINE_8 : Cell.image_mine_8,
				CELL_BOMB : Cell.image_bomb
			}
			return dictionary[self.type]
		elif self.status == STATUS_OPEN_EXPLODED: return Cell.image_open_exploded

	def open(self, in_play = True):
		if self.is_unopened():
			if in_play and self.is_bomb():
				self.status = STATUS_OPEN_EXPLODED
			else:
				self.status = STATUS_OPEN
			self.update()

	def set_type(self, type):
		self.type = type
		self.update()

	def set_status(self, status):
		self.status = status
		self.update()

	def update(self):
		self.image = self.cell_image()

	def type_charactor(self):
		dictionary = {
			CELL_MINE_0 : "0",
			CELL_MINE_1 : "1",
			CELL_MINE_2 : "2",
			CELL_MINE_3 : "3",
			CELL_MINE_4 : "4",
			CELL_MINE_5 : "5",
			CELL_MINE_6 : "6",
			CELL_MINE_7 : "7",
			CELL_MINE_8 : "8",
			CELL_BOMB : "B"
		}
		return dictionary[self.type]

	def status_charactor(self):
		dictionary = {
			STATUS_UNOPENED : "U",
			STATUS_UNOPENED_QUESTION : "Q",
			STATUS_UNOPENED_FLAG : "F",
			STATUS_OPEN : "O",
			STATUS_OPEN_EXPLODED : "X",
		}
		return dictionary[self.status]

	def charactor(self):
		return self.type_charactor() + self.status_charactor()

	def is_bomb_nearby(self):
		return (CELL_MINE_1 <= self.type <= CELL_MINE_8) or (self.type == CELL_BOMB)

	def is_bomb(self):
		return self.type == CELL_BOMB
	
	def is_open(self):
		return self.status == STATUS_OPEN or self.status == STATUS_OPEN_EXPLODED
	
	def is_unopened(self):
		return not self.is_open()


class Cluster:

	def __init__(self, safe_positions, positions_bomb_nearby):

		# clustered cell positions that all the cells nearby are safe to open
		self.safe_positions = safe_positions

		# surrounding cell positions outside of safe positions, that a bomb
		# is nearby
		self.positions_bomb_nearby = positions_bomb_nearby

		# in order to reduce computation, this is a flag not to compute
		# whether entire positions of this cluster are revealed
		self.is_revealed = False


class Board:

	def __init__(self, width, height, number_of_mines):
		self.width = width
		self.height = height
		self.cells = {}
		self.sprites = pygame.sprite.Group()
		self.number_of_mines = number_of_mines
		self.game_state = GAME_STATE_INPLAY

		for row in range(0, self.height):
			for col in range(0, self.width):
				cell = Cell()
				self.cells[(col, row)] = cell
				self.sprites.add(cell)

		nom = number_of_mines
		while nom > 0:
			col = random.randrange(0, self.width)
			row = random.randrange(0, self.height)
			cell = self.cells[(col, row)]
			if (cell.type != CELL_BOMB):
				cell.set_type(CELL_BOMB)
				nom -= 1

		self.update()
		self.safe_clusters = self.compute_safe_clusters()
		self.reveal_a_safe_cluster()

		icon_size = (GAME_STATE_ICON_SIZE, GAME_STATE_ICON_SIZE)
		self.icon_inplay = self.load_image("face-smile.png", icon_size)
		self.icon_completed = self.load_image("face-cool.png", icon_size)
		self.icon_game_over = self.load_image("face-fear.png", icon_size)


	def font(self):
		return pygame.font.SysFont(None, 32)

	def nearby_vectors(self):
		return [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]

	def update(self):
		for row in range(0, self.height):
			for col in range(0, self.width):
				cell1 = self.cells[(col, row)]
				cell1.rect = self.cell_rect(col, row)
				if (cell1.type != CELL_BOMB):
					# count mines in neighborhood
					number_of_mines = 0
					for (vx, vy) in self.nearby_vectors():
						(col2, row2) = (col + vx, row + vy)
						if 0 <= col2 < self.width and 0 <= row2 < self.height:
							cell2 = self.cells[(col2, row2)]
							if cell2.type == CELL_BOMB:
								number_of_mines += 1
					cell1.set_type(number_of_mines)


	def banner_color(self):
		if self.game_state == GAME_STATE_INPLAY: return (0x00,0xa0,0xc0)
		elif self.game_state == GAME_STATE_COMPLETED: return (0x00,0x00,0xff)
		elif self.game_state == GAME_STATE_OVER: return (0xa0,0x00,0x00)
		else: return (0xff,0xff,0xff)

	def game_state_icon(self):

		if self.game_state == GAME_STATE_INPLAY: return self.icon_inplay
		elif self.game_state == GAME_STATE_COMPLETED: return self.icon_completed
		elif self.game_state == GAME_STATE_OVER: return self.icon_game_over
		else: return self.icon_inplay

	def load_image(self, name, size):
		image = pygame.image.load(name)
		image = pygame.transform.scale(image, size)
		return image

	def draw(self, window):
		self.sprites.draw(window)

		LEFT_MARGIN = 8
		RIGHT_MARGIN = 8
		window_rect = window.get_rect()

		surface = pygame.Surface((window.get_width(), TOP_MARGIN))
		surface.fill(self.banner_color())
		window.blit(surface, (0,  0))

		surface_message = self.font().render('MINE SWEEPER', True, (255, 255, 255))
		window.blit(surface_message, (LEFT_MARGIN,  (TOP_MARGIN - surface_message.get_height()) / 2))
	
		number_of_mines_left = self.number_of_mines - self.number_of_flags()
		surface_score = self.font().render(str(number_of_mines_left), True, (255, 255, 0))
		window.blit(surface_score, (window.get_width() - surface_score.get_width() - RIGHT_MARGIN,  (TOP_MARGIN - surface_score.get_height()) / 2))

		icon_image = self.game_state_icon()
		window.blit(icon_image, (window.get_width()/2 - GAME_STATE_ICON_SIZE/2, (TOP_MARGIN - icon_image.get_height())/2))
	
	def should_reveal_cells(self, col, row):
		if (0 <= col < self.width) and (0 <= row < self.height):
			cell = self.cells[(col, row)]
			return cell.is_unopened()
		else:
			return False

	def reveal_cells(self, col, row):

		# case: no bomb nearby, reveal safe cells
		cell1 = self.cells[(col, row)]
		if cell1.type == CELL_MINE_0:

			flags = self.make_map(False)

			# to process all safe cells nearby, keep adding safe cells nearby
			# and remove them when processed, and keep processing till reach
			# to the end of queue.
			queue = [(col, row)]
			flags[(col, row)] = True

			while len(queue) > 0:
				(col, row) = queue.pop()
				cell1 = self.cells[(col, row)]
				cell1.open()
				print(self.description())
				for (vx, vy) in self.nearby_vectors():
					(col2, row2) = (col + vx, row + vy)
					if (0 <= col2 < self.width) and (0 <= row2 < self.height):
						cell2 = self.cells[(col2, row2)]
						flag = flags[(col2, row2)]
						if not flag and not cell2.is_bomb_nearby():
							queue.append((col2, row2))
							cell2.open()
							flags[(col2, row2)] = True
						else:
							if cell2.status == STATUS_UNOPENED and not cell2.is_bomb():
								cell2.open()

		# case: unopened cell - try open it
		elif cell1.is_unopened():
			cell1.open()

	def compute_safe_clusters(self): #

		vectors = [(0,-1),(-1,0),(0,1),(1,0)] # [up, left, down, right]

		NO_GROUP = 0
		safe_cluster_dict = {} # key: group-id, value: [(col, row)] array of position tuple

		flags = self.make_map(False) # key: (col, row), value: Boolean - to avoid processing the same cell twice
		groups = self.make_map(NO_GROUP) # key: (col, row), value: group-id

		current_group = NO_GROUP
		for row in range(0, self.height):
			for col in range(0, self.width):
				cell0 = self.cells[(col, row)]
				group0 = groups[(col, row)]
				if cell0.type == CELL_MINE_0 and group0 == NO_GROUP:
					positions = [(col, row)]
					queue = [(col, row)]
					current_group += 1
					groups[(col, row)] = current_group
					while len(queue) > 0:
						(col, row) = queue.pop()
						cell1 = self.cells[(col, row)]
						for (vx, vy) in vectors:
							(col2, row2) = (col + vx, row + vy)
							if (0 <= col2 < self.width) and (0 <= row2 < self.height):
								cell2 = self.cells[(col2, row2)]
								group2 = groups[(col2, row2)]
								if cell2.type == CELL_MINE_0 and group2 == NO_GROUP:
									positions.append((col2, row2))
									queue.append((col2, row2))
									groups[(col2, row2)] = current_group
					safe_cluster_dict[current_group] = positions

		# now make a list of tuple - (number of positions, positions) to sort
		safe_cluster_tuples = []
		for key in safe_cluster_dict.keys():
			positions = safe_cluster_dict[key]
			safe_cluster_tuples.append((len(positions), positions))

		# should be sorted
		safe_clusters = []
		for (count, positions) in reversed(sorted(safe_cluster_tuples)):
			positions_bomb_nearby = self.compute_positions_bomb_nearby(positions)
			safe_cluster = Cluster(positions, positions_bomb_nearby)
			safe_clusters.append(safe_cluster)

		return safe_clusters

		'''
		string = ""
		for row in range(0, self.height):
			delimiter = ""
			line = "|"
			for col in range(0, self.width):
				cell = self.cells[(col, row)]
				group = groups[(col, row)]
				charactor = chr(ord('a')+group-1) if group > 0 else "."
				line += (delimiter + charactor)
				delimiter = "|"
			line += "|"
			string += (line + "\r\n")
		print(string)
		'''

	# make a generic map table -- key: (col, row), value: any
	def make_map(self, value):
		values = {}
		for row in range(0, self.height):
			for col in range(0, self.width):
				values[(col, row)] = value
		return values		

	# when a list of safe positions are given, find a list of postions
	# of a cell whose next cell is a bomb.
	def compute_positions_bomb_nearby(self, safe_positions):
		flags = self.make_map(False)
		positions = []
		for (col, row) in safe_positions:
			assert(0 <= col < self.width and 0 <= row < self.height)
			assert(self.cells[(col, row)].type == CELL_MINE_0)
			for (vx, vy) in self.nearby_vectors():
				(col2, row2) = (col + vx, row + vy)
				if 0 <= col2 < self.width and 0 <= row2 < self.height:
					if not flags[(col2, row2)]:
						flags[(col2, row2)] = True
						if self.cells[(col2, row2)].is_bomb_nearby():
							positions.append((col2, row2))
		return positions

	# check if given cluster 
	def is_cluster_revealed(self, cluster):
		for (col, row) in cluster.positions_bomb_nearby:
			if self.cells[(col, row)].is_unopened():
				return False
		for (col, row) in cluster.safe_positions:
			if self.cells[(col, row)].is_unopened():
				return False
		return True		

	def reveal_a_safe_cluster(self):
		for cluster in self.safe_clusters:
			if cluster.is_revealed:
				continue
			for (col, row) in cluster.positions_bomb_nearby:
				cell = self.cells[(col, row)]
				assert(cell.type != CELL_BOMB)
				cell.set_status(STATUS_OPEN)
			for (col, row) in cluster.safe_positions:
				cell = self.cells[(col, row)]
				assert(cell.type != CELL_BOMB)
				cell.set_status(STATUS_OPEN)
			cluster.is_revealed = True
			return True
		return False

	def reveal_all_cells(self, in_play):
		for row in range(0, self.height):
			for col in range(0, self.width):
				cell = self.cells[(col, row)]
				cell.open(in_play)
				
	def cell_rect(self, col, row):
		left = col * CELL_SIZE
		top = (row * CELL_SIZE) + TOP_MARGIN
		return pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)

	def cell_position(self, x, y):
		return (x / CELL_SIZE, (y - TOP_MARGIN) / CELL_SIZE)

	def number_of_flags(self):
		number_of_flags = 0
		for row in range(0, self.height):
			for col in range(0, self.width):
				cell = self.cells[(col, row)]
				if cell.status == STATUS_UNOPENED_FLAG:
					number_of_flags += 1
		return number_of_flags

	def description(self):
		string = ""
		for y in range(0, self.height):
			delimiter = ""
			line = "|"
			for x in range(0, self.width):
				cell = self.cells[(x, y)]
				line += (delimiter + cell.charactor())
				delimiter = "|"
			line += "|"
			string += (line + "\r\n")
		return string

	def left_click(self, (x, y)):
		(col, row) = self.cell_position(x, y)
		if (0 <= col < self.width) and (0 <= row < self.height):
			cell = self.cells[(col, row)]
			if self.should_reveal_cells(col, row):
				self.reveal_cells(col, row)
		self.check_game_state()

	def right_click(self, (x, y)):
		(col, row) = self.cell_position(x, y)
		if (0 <= col < self.width) and (0 <= row < self.height):
			cell = self.cells[(col, row)]
			if cell.status == STATUS_UNOPENED:
				cell.set_status(STATUS_UNOPENED_FLAG)
			elif cell.status == STATUS_UNOPENED_FLAG:
				cell.set_status(STATUS_UNOPENED_QUESTION)
			elif cell.status == STATUS_UNOPENED_QUESTION:
				cell.set_status(STATUS_UNOPENED)
		self.check_game_state()

	def is_safe_cluster_open(self, positions):
		for (col, row) in positions:
			for (vx, vy) in self.nearby_vectors():
				(col2, row2) = (col + vx, row + vy)
				if 0 <= row2 < self.height and 0 <= col2 < self.width:
					cell = self.cells[(col2, row2)]
					if cell.is_unopened():
						return False
		return True

	def is_game_over(self):
		for row in range(0, self.height):
			for col in range(0, self.width):
				cell = self.cells[(col, row)]
				if cell.status == STATUS_OPEN_EXPLODED:
					return True
		return False

	def is_game_completed(self):
		for row in range(0, self.height):
			for col in range(0, self.width):
				cell = self.cells[(col, row)]
				if cell.type == CELL_BOMB and cell.status == STATUS_UNOPENED_FLAG:
					continue
				elif cell.is_unopened():
					return False
		return True
		
	def check_game_state(self):
		if self.is_game_over():
			self.game_state = GAME_STATE_OVER
			print("minesweeper: Game Over")
		elif self.is_game_completed():
			self.game_state = GAME_STATE_COMPLETED
			print("minesweeper: Game Cleared")
	

class Game:

	@staticmethod
	def load_image(name, size):
		image = pygame.image.load(name)
		image = pygame.transform.scale(image, size)
		return image

	def __init__(self):
		self.number_of_rows = NUM_OF_ROWS
		self.number_of_cols = NUM_OF_COLS

		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Mine Sweeper")
		self.clock = pygame.time.Clock()

		self.running = True
		self.sprite = pygame.sprite.Group()
		self.board = Board(self.number_of_cols, self.number_of_rows, NUM_OF_BOMBS)
		self.sprite.add(self.board.sprites)
		self.fps = FPS
		print(self.board.description())

		self.image_flag = Game.load_image("flag.png", (CELL_SIZE, CELL_SIZE))

#		self.safe_clusters = self.board.safe_clusters()
#		if len(self.safe_clusters) > 0:
#			positions = self.safe_clusters.pop()
#			print("what", positions[0])
#			(col, row) = positions[0]
#			self.board.reveal_cells(col, row)


	def draw(self):
		self.board.draw(self.window)
		pygame.display.update()
		pygame.display.flip()

	def run(self):
		self.draw()
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					position = event.pos
					if event.button == MOUSE_BUTTON_LEFT:
						self.board.left_click(position)
						if self.board.is_game_over():
							in_play = False
							self.board.reveal_all_cells(in_play)
					elif event.button == MOUSE_BUTTON_RIGHT:
						self.board.right_click(position)

					self.draw()
			

def main():

	pygame.init()

	game = Game()
	game.run()

	pygame.quit()
	

main()
