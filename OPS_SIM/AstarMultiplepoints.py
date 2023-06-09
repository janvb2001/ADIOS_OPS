import random
import pygame
import math
from queue import PriorityQueue
import time
from math import sqrt

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append([grid[self.row + 1][self.col],0])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append([grid[self.row - 1][self.col],0])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append([grid[self.row][self.col + 1],0])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append([grid[self.row][self.col - 1],0])

		if self.col > 0 and self.row > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # UPLEFT
			self.neighbors.append([grid[self.row - 1][self.col - 1],1])

		if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier(): # DOWNLEFT
			self.neighbors.append([grid[self.row + 1][self.col - 1],1])

		if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col + 1].is_barrier():  # DOWNRIGHT
			self.neighbors.append([grid[self.row + 1][self.col + 1],1])

		if self.row > 0 and self.col < self.total_rows -1 and not grid[self.row - 1][self.col + 1].is_barrier(): #UPRIGHT
			self.neighbors.append([grid[self.row - 1][self.col +1 ],1])

		# if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier():  # UPRIGHT
		# 	self.neighbors.append(grid[self.row + 1][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	path = []

	while current in came_from:
		current = came_from[current]
		current.make_path()

		coor = (current.x, current.y)
		path.append(coor)
		if draw:
			draw()

	return path

def algorithm(grid, start, end, draw = False):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	# for i in range(len(litters)):
	# 	for j in range(len(litters[i])):
	# 		f_score[start] += h(start.get_pos(), end.get_pos())
	for i in range(len(end)):
		print(end[i])
		print((start.row, start.col))
		print(h((start.row, start.col), end[i].get_pos()))
		# f_score[start] = f_score[start] + h((start.row, start.col), end[i])
		f_score[start] += h(start.get_pos(), end[i].get_pos())
	open_set_hash = {start}

	donecount = 0

	while not open_set.empty():
		if draw:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		for i in range(len(end)):
			if current == end[i]:
				path = reconstruct_path(came_from, end[i], draw)
				print("mooie taak voor morgen:")
				print(path)
				end[i].make_end()
				donecount += 1
				print("donecount: ", donecount, "total litter: ", len(end))
				if donecount == len(end):
					return True

		for neighbor in current.neighbors:
			if neighbor[1] == 0:
				temp_g_score = g_score[current] + 1
			elif neighbor[1] == 1:
				temp_g_score = g_score[current] + sqrt(2)

			neighbor = neighbor[0]
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score
				for i in range(len(end)):
					f_score[neighbor] += h(neighbor.get_pos(), end[i].get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		if draw:
			draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(width, rows, obstruct, gs, litters, animation):
	if animation:
		win = pygame.display.set_mode((WIDTH, WIDTH))
		pygame.display.set_caption("A* Path Finding Algorithm")
		dr = lambda: draw(win, grid, ROWS, width)
	else:
		win = False
		dr = False

	ROWS = rows
	grid = make_grid(ROWS, width)

	pos = (gs["x"], gs["y"])
	row, col = get_clicked_pos(pos, ROWS, width)
	spot = grid[row][col]
	start = spot
	start.make_start()

	ends = []
	for i in range(len(litters)):
		for j in range(len(litters[i])):
			pos = (litters[i][j].x, litters[i][j].y)
			row, col = get_clicked_pos(pos, ROWS, width)
			if row < len(grid) and col < len(grid[row]):
				spot = grid[row][col]
			end = spot
			ends.append(end)
			end.make_end()
	for i in range(len(obstruct)):
		pos = obstruct[i]
		row, col = get_clicked_pos(pos, ROWS, width)
		if row < len(grid) and col < len(grid[row]):
			spot = grid[row][col]
		bar = spot
		bar.make_barrier()

	# run = True
	# while run:
	if win:
		draw(win, grid, ROWS, width)

	for row in grid:
		for spot in row:
			spot.update_neighbors(grid)


	done = algorithm(grid, start, ends, draw=dr)
	# if done:
	time.sleep(5)
	run = False

			# if event.key == pygame.K_c:
			# 	start = None
			# 	end = None
			# 	grid = make_grid(ROWS, width)

	if win:
		pygame.quit()



animation = True
WIDTH = 800

# def main(width, rows, obstruct, gs, litters, win = False):
class litter:
	def __init__(self, WIDTH):
		self.x = random.randint(0,WIDTH)
		self.y = random.randint(0,WIDTH)

litters = [[],[]]

for i in range(2):
	for j in range(20):
		litters[i].append(litter(WIDTH))

obst = []
for i in range(100):
	obst.append((random.randint(0,WIDTH),random.randint(0,WIDTH)))



main(WIDTH, 30, obst, dict(x=400,y=400), litters, animation)