import random
import pygame
import math
from queue import PriorityQueue
import time
from math import sqrt
import numpy as np

from generalFunc import *


class Spot:
	def __init__(self, row, col, width, total_rowsx, total_rowsy):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = (255, 255, 255)
		self.neighbors = []
		self.width = width
		self.total_rowsx = total_rowsx
		self.total_rowsy = total_rowsy
		self.litteri = []

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == (255, 0, 0)

	def is_open(self):
		return self.color == (0, 255, 0)

	def is_barrier(self):
		return self.color == (0, 0, 0)

	def is_start(self):
		return self.color == (255, 165 ,0)

	def is_end(self):
		return self.color == (64, 224, 208)

	def reset(self):
		self.color = (255, 255, 255)

	def make_start(self):
		self.color = (255, 165 ,0)

	def make_closed(self):
		self.color = (255, 0, 0)

	def make_open(self):
		self.color = (0, 255, 0)

	def make_barrier(self):
		self.color = (0, 0, 0)

	def make_end(self):
		self.color = (64, 224, 208)

	def make_path(self):
		self.color = (128, 0, 128)

	def draw(self, win, f):
		pygame.draw.rect(win, self.color, (self.x * f, self.y * f, self.width * f, self.width * f))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rowsx - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append([grid[self.row + 1][self.col],0])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append([grid[self.row - 1][self.col],0])

		if self.col < self.total_rowsy - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append([grid[self.row][self.col + 1],0])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append([grid[self.row][self.col - 1],0])

		if self.col > 0 and self.row > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # UPLEFT
			self.neighbors.append([grid[self.row - 1][self.col - 1],1])

		if self.col > 0 and self.row < self.total_rowsx - 1 and not grid[self.row + 1][self.col - 1].is_barrier(): # DOWNLEFT
			self.neighbors.append([grid[self.row + 1][self.col - 1],1])

		if self.row < self.total_rowsx - 1 and self.col < self.total_rowsy - 1 and not grid[self.row + 1][self.col + 1].is_barrier():  # DOWNRIGHT
			self.neighbors.append([grid[self.row + 1][self.col + 1],1])

		if self.row > 0 and self.col < self.total_rowsy -1 and not grid[self.row - 1][self.col + 1].is_barrier(): #UPRIGHT
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

		coor = [current.x, current.y]
		path.insert(0,coor)
		if draw:
			draw()

	return path


def algorithm(grid, start, end, litters, draw = False):
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
		# print(end[i])
		# print((start.row, start.col))
		# print(h((start.row, start.col), end[i].get_pos()))
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

				# print([path, end[i].typeL, end[i].ind])

				# litters[end[i].litteri][end[i].ind].path = path
				for j in range(len(end[i].litteri)):
					litters[end[i].litteri[j][0]][end[i].litteri[j][1]].path = np.array(path)

				end[i].make_end()
				donecount += 1
				# print("donecount: ", donecount, "total litter: ", len(end))
				# if donecount == len(end):
				# 	return True

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
				# for i in range(len(end)):
				# 	f_score[neighbor] += h(neighbor.get_pos(), end[i].get_pos())
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


def make_grid(length, width, gap):
	grid = []
	rowsx = width // gap
	rowsy = length // gap
	for i in range(rowsx):
		grid.append([])
		for j in range(rowsy):
			spot = Spot(i, j, gap, rowsx, rowsy)
			grid[i].append(spot)

	return grid, rowsx, rowsy


def draw_grid(win, rowsx, rowsy, gap, length, width, f):
	for i in range(rowsy):
		pygame.draw.line(win, (128, 128, 128), (0, f * i * gap), (f * width, f * i * gap))
		for j in range(rowsx):
			pygame.draw.line(win, (128, 128, 128), (f * j * gap, 0), (f * j * gap, f * length))


def draw(win, grid, rowsx, rowsy, gap, length, width, f):
	win.fill((255, 255, 255))

	for row in grid:
		for spot in row:
			spot.draw(win, f)

	draw_grid(win, rowsx, rowsy, gap, length, width, f)
	pygame.display.update()


def get_clicked_pos(pos, gap):
	y, x = pos

	row = y // gap
	col = x // gap

	return int(row), int(col)

def main(grid, start, ends, gap, length, width, rowsx, rowsy, litters, animation, f):
	if animation:
		win = pygame.display.set_mode((f * width, f * length))
		pygame.display.set_caption("A* Path Finding Algorithm")
		dr = lambda: draw(win, grid, rowsx, rowsy, gap, length, width, f)
	else:
		win = False
		dr = False

	# run = True
	# while run:
	if win:
		draw(win, grid, rowsx, rowsy, gap, length, width, f)

	for row in grid:
		for spot in row:
			spot.update_neighbors(grid)


	done = algorithm(grid, start, ends, litters, draw=dr)
	# if done:
	# time.sleep(5)
	run = False

			# if event.key == pygame.K_c:
			# 	start = None
			# 	end = None
			# 	grid = make_grid(ROWS, width)

	if win:
		pygame.quit()

# ----------------------------------------------------------------------

# animation = True
# WIDTH = 800
# LENGTH = 800
# gap = 10
# gs = dict(x=100, y=100)
#
# # def main(width, rows, obstruct, gs, litters, win = False):
# class litter:
# 	def __init__(self, LENGTH, WIDTH):
# 		self.x = random.randint(0,WIDTH)
# 		self.y = random.randint(0,LENGTH)
# 		self.path = []
#
# litters = [[],[]]
#
# for i in range(2):
# 	for j in range(500):
# 		litters[i].append(litter(LENGTH, WIDTH))
#
# obst = []
# for i in range(0):
# 	obst.append((random.randint(0,WIDTH),random.randint(0,LENGTH)))


# grid, rowsx, rowsy = make_grid(LENGTH, WIDTH, gap)
#
#
# pos = (gs["x"], gs["y"])
# row, col = get_clicked_pos(pos, gap)
# spot = grid[row][col]
# start = spot
# start.make_start()
#
# ends = []
#
# indicesSquareCorners([(300,300),(200,200)], gap, LENGTH, WIDTH, grid)
# indicesSquareCorners([(790,500),(510,510)], gap, LENGTH, WIDTH, grid)
#
# for i in range(len(litters)):
# 	for j in range(len(litters[i])):
# 		pos = (litters[i][j].x, litters[i][j].y)
# 		row, col = get_clicked_pos(pos, gap)
# 		if row < len(grid) and col < len(grid[row]):
# 			spot = grid[row][col]
# 		elif row >= len(grid):
# 			spot = grid[row-1][col]
# 		elif col >= len(grid[row]):
# 			spot = grid[row][col-1]
# 		end = spot
#
# 		end.typeL = i
# 		end.ind = j
#
# 		ends.append(end)
# 		end.make_end()
# for i in range(len(obst)):
# 	pos = obst[i]
# 	row, col = get_clicked_pos(pos, gap)
# 	if row < len(grid) and col < len(grid[row]):
# 		spot = grid[row][col]
# 	elif row >= len(grid):
# 		spot = grid[row - 1][col]
# 	elif col >= len(grid[row]):
# 		spot = grid[row][col-1]
# 	bar = spot
# 	bar.make_barrier()
#
# t = time.time()
#
# main(grid, start, ends, gap, LENGTH, WIDTH, rowsx, rowsy, litters, animation)
#
# print(time.time() - t)
#
# notfound = 0
# for i in range(len(litters)):
# 	for j in range(len(litters[i])):
# 		if len(litters[i][j].path) == 0:
# 			notfound += 1
# print(notfound)