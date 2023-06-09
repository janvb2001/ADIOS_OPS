import pygame
from math import sqrt
from queue import PriorityQueue
import numpy as np

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A star Finding Algorithm")

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

	def is_end1(self):
		return self.color == TURQUOISE

	def is_end2(self):
		return self.color == TURQUOISE

	def is_end3(self):
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
		obstructcor.append(self.get_pos())

	def make_end1(self):
		self.color = TURQUOISE

	def make_end2(self):
		self.color = TURQUOISE
	def make_end3(self):
		self.color = TURQUOISE

	def make_path1(self):
		self.color = PURPLE

	def make_path2(self):
		self.color = PURPLE

	def make_path3(self):
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


	def __lt__(self, other):
		return False

pathcor1 = []
pathcor2 = []
pathcor3 = []
obstructcor = []

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path1(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path1()
		pathcor1.append(current.get_pos())  # Store the path coordinates
		draw()

def reconstruct_path2(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path2()
		pathcor2.append(current.get_pos())  # Store the path coordinates
		draw()

def reconstruct_path3(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path3()
		pathcor3.append(current.get_pos())  # Store the path coordinates
		draw()

def determine_corners(path):
    corners = []
    for i in range(1,len(path)-1):
        x1,y1 = path[i-1]
        x2,y2 = path[i]
        x3,y3 = path[i+1]
        if abs(x1-x2)>0 and abs(y2-y3)>0 or abs(y1-y2)>0 and abs(x2-x3)>0:
            corners.append((x2,y2))
    return corners

def algorithm(draw, grid, start, end1, end2, end3):
	count = 0
	quitter = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f1_score = {spot: float("inf") for row in grid for spot in row}
	f1_score[start] = h(start.get_pos(), end1.get_pos())
	f2_score = {spot: float("inf") for row in grid for spot in row}
	f2_score[start] = h(start.get_pos(), end2.get_pos())
	f3_score = {spot: float("inf") for row in grid for spot in row}
	f3_score[start] = h(start.get_pos(), end3.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end1:
			reconstruct_path1(came_from, end1, draw)
			end1.make_end1()
			print(pathcor1)
			print('the coordinates of the corners of path 1 are: ', determine_corners(pathcor1))
			quitter +=1

		if current == end2:
			reconstruct_path2(came_from, end2, draw)
			end2.make_end2()
			print(pathcor2)
			print('the coordinates of the corners of path 2 are: ', determine_corners(pathcor2))
			quitter += 1

		if current == end3:
			reconstruct_path3(came_from, end3, draw)
			end3.make_end3()
			print(pathcor3)
			print('the coordinates of the corners of path 3 are: ', determine_corners(pathcor3))
			quitter += 1

		if quitter == 3:
			print('the coordinates of the barriers are: ', obstructcor)
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

				if neighbor.row < neighbor.total_rows - 1 and neighbor.row > 0 and neighbor.col < neighbor.total_rows - 1 and neighbor.col > 0 and (grid[neighbor.row + 1][neighbor.col].is_barrier() or grid[neighbor.row - 1][neighbor.col].is_barrier() or grid[neighbor.row][neighbor.col + 1].is_barrier() or grid[neighbor.row][neighbor.col - 1].is_barrier()):
					f1_score[neighbor] = temp_g_score + 1000 + h(neighbor.get_pos(), end1.get_pos())
					f2_score[neighbor] = temp_g_score + 1000 + h(neighbor.get_pos(), end2.get_pos())
					f3_score[neighbor] = temp_g_score + 1000 + h(neighbor.get_pos(), end3.get_pos())

				#This one did not check for boundaries
				# if grid[neighbor.row + 1][neighbor.col].is_barrier() or grid[neighbor.row - 1][neighbor.col].is_barrier() or grid[neighbor.row][neighbor.col + 1].is_barrier() or grid[neighbor.row][neighbor.col - 1].is_barrier():
				# 	f1_score[neighbor] = temp_g_score + 100 + h(neighbor.get_pos(), end1.get_pos())

				else:
					f1_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end1.get_pos())
					f2_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end2.get_pos())
					f3_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end3.get_pos())

				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f1_score[neighbor]+f2_score[neighbor]+f3_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

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

def main(win, width):
	ROWS = 40
	grid = make_grid(ROWS, width)

	start = None
	end1 = None
	end2 = None
	end3 = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end1 and spot != end2 and spot != end3:
					start = spot
					start.make_start()

				elif not end1 and spot != start and spot != end2 and spot != end3:
					end1 = spot
					end1.make_end1()

				elif not end2 and spot != start and spot != end1 and spot != end3:
					end2 = spot
					end2.make_end2()

				elif not end3 and spot != start and spot != end2 and spot != end1:
					end3 = spot
					end3.make_end3()

				elif spot != end1 and spot != end2 and spot != end3 and spot != start:
					spot.make_barrier()


			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end1:
					end1 = None
				elif spot == end2:
					end2 = None
				elif spot == end3:
					end3 = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE: # and start and end1 and end2 and end3
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end1, end2, end3)

				#MAKE GRIDS FOR BOTH PATH AND OBSTRUCTS
				# OBSTRUCT:
				obstructgrid = np.zeros((ROWS, ROWS))
				for i in range(len(obstructcor)):
					obstructgrid[obstructcor[i][1]][obstructcor[i][0]] = 1
				print('grid of obstruction: ',obstructgrid)
				pathgrid = np.zeros((ROWS, ROWS))
				for i in range(len([pathcor1])):
					pathgrid[pathcor1[i][1]][pathcor1[i][0]] = 1
				print('grid of path1: ',pathgrid)



				if event.key == pygame.K_c:
					start = None
					end1 = None
					end2 = None
					end3 = None
					grid = make_grid(ROWS, width)

	#make path grid

	#make obstruct grid

	pygame.quit()

main(WIN, WIDTH)
