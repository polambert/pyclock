#!/usr/bin/env python3

import datetime
import time
from math import pi, sin, cos, floor

WIDTH = 60
HEIGHT = 30

# Fill the grid
grid = []
for i in range(HEIGHT):
	l = []
	for j in range(WIDTH):
		l.append(False)
	grid.append(l)

def clamp(a, b, val):
	return max(a, min(val, b))

def dot(x, y):
	global grid
	grid[clamp(0, HEIGHT-1, y)][clamp(0, WIDTH-1, x)] = True

def raytrace(x0, y0, x1, y1):
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	x = x0
	y = y0
	n = 1 + dx + dy
	x_inc = (x1 > x0) and 1 or -1
	y_inc = (y1 > y0) and 1 or -1
	error = dx - dy
	dx *= 2
	dy *= 2

	while n > 0:
		n -= 1

		if error > 0:
			x += x_inc
			error -= dy
		else:
			y += y_inc
			error += dx
		dot(x, y)

def clear():
	global grid
	for i in range(HEIGHT):
		for j in range(WIDTH):
			grid[i][j] = False

def draw():
	second = datetime.datetime.now().second
	if second < 15:
		delta = second - 15
		second = 60 + delta
	else:
		second -= 15
	angle = (second / 60) * (2 * pi)

	# Draw the dot in the center of the screen
	centery = HEIGHT // 2
	centerx = WIDTH // 2
	dot(centerx, centery)

	# Draw the dot at the end of the clock hand
	endx = floor(cos(angle) * centerx) + centerx
	endy = floor(sin(angle) * centery) + centery
	dot(endx, endy)

	# Draw all of the dots in between
	raytrace(centerx, centery, endx, endy)

	# Draw out the entire grid
	for i in range(HEIGHT):
		for j in range(WIDTH):
			if grid[i][j]:
				print("\033[7m", end="")
			print(" ", end="")
			print("\033[0m", end="")
		print()

def backspace():
	for i in range(HEIGHT):
		print("\033[F", end="")

if __name__ == "__main__":
	while True:
		clear()
		draw()
		backspace()
		time.sleep(1)

