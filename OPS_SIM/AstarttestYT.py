import pygame
import math
from queue import PriorityQueue

WIDTH = 800
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
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path1(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path1()
		draw()

def reconstruct_path2(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path2()
		draw()

def reconstruct_path3(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path3()
		draw()


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
			#return True
			quitter +=1

		if current == end2:
			reconstruct_path2(came_from, end2, draw)
			end2.make_end2()
			#return True
			quitter += 1

		if current == end3:
			reconstruct_path3(came_from, end3, draw)
			end3.make_end3()
			#return True
			quitter += 1

		if quitter == 3:
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
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
	ROWS = 50
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
				if event.key == pygame.K_SPACE and start and end1 and end2 and end3:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end1, end2, end3)

				if event.key == pygame.K_c:
					start = None
					end1 = None
					end2 = None
					end3 = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
