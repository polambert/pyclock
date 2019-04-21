#!/usr/bin/env python3

import datetime
import calendar
import time
from math import pi, sin, cos, floor
import sys
import argparse

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store", dest="size", default="20x10")
parser.add_argument("-short", action="store_true", dest="shorten_time_text")

args = parser.parse_args()

arg_size = args.size
arg_short = args.shorten_time_text

WIDTH = int(arg_size.split("x")[0])
HEIGHT = int(arg_size.split("x")[1])

class state:
	second = 0
	minute = 1
	hour = 2
	none = 3

# Fill the grid (and chars)
grid = []
chars = []
for i in range(HEIGHT):
	g = []
	c = []
	for j in range(WIDTH):
		g.append(state.none)
		c.append(" ")
	grid.append(g)
	chars.append(c)

def clamp(a, b, val):
	return max(a, min(val, b))

def dot(x, y, t=state.none):
	global grid
	
	grid[clamp(0, HEIGHT-1, y)][clamp(0, WIDTH-1, x)] = t

def raytrace(x0, y0, x1, y1, i):
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
		dot(x, y, i)

def clear():
	global grid
	for i in range(HEIGHT):
		for j in range(WIDTH):
			grid[i][j] = state.none

def write(string, x, y):
	global chars

	for i in range(len(string)):
		chars[y][clamp(0, WIDTH-1, x + i)] = string[i]

def draw():
	now = datetime.datetime.now()
	times = []

	times.append(now.second)
	times.append(now.minute)
	times.append(now.hour % 12)

	for i in range(len(times)):
		if i <= 1:
			top = 60
		else:
			top = 12

		top /= 4

		if times[i] < top:
			delta = times[i] - top
			times[i] = (top * 4) + delta
		else:
			times[i] -= top

	angles = []
	
	for i in range(len(times)):
		if i <= 1:
			top = 60
		else:
			top = 12
		angle = (times[i] / top) * (2 * pi)
		angles.append(angle)

	# Draw the dot in the center of the screen
	centery = HEIGHT // 2
	centerx = WIDTH // 2
	dot(centerx, centery)

	# Draw the dot at the end of the clock hand
	ends = [] # 2d array

	for i in range(len(angles)):
		ends.append([])
		if i <= 1:
			ends[i].append(floor(cos(angles[i]) * centerx) + centerx)
			ends[i].append(floor(sin(angles[i]) * centery) + centery)
		else:
			# Hour hand, shorter
			ends[i].append(floor(cos(angles[i]) * (centerx * 0.75)) + centerx)
			ends[i].append(floor(sin(angles[i]) * (centery * 0.75)) + centery)
		
	# Draw all of the dots in between
	for i in range(len(ends)):
		raytrace(centerx, centery, ends[i][0], ends[i][1], i)

	# Draw text
	if arg_short:
		write((now.strftime("%A")[:3].upper()) + (now.strftime(" %B")[:4].upper()) + now.strftime(" %d %Y"), 3, HEIGHT - 2)
	else:
		write(now.strftime("%A, %B %d %Y"), 3, HEIGHT - 2)

	# Draw out the entire grid
	for i in range(HEIGHT):
		for j in range(WIDTH):
			color = "232"
			
			if grid[i][j] == state.second:
				color = "255" # White
			elif grid[i][j] == state.minute:
				color = "246" # Dark Gray
			elif grid[i][j] == state.hour:
				color = "239" # Dark Dark Gray
			elif grid[i][j] == state.none:
				pass

			fg = "255"
			bg = color

			if bg != "232" or chars[i][j] != " ":
				if bg != "232":
					print(u"\u001b[48;5;" + bg + "m", end="")
				print(u"\u001b[38;5;" + fg + "m" + chars[i][j], end="")
			else:
				print(" ", end="")
			print("\033[0m", end="")
		print()

def backspace():
	for i in range(HEIGHT):
		print("\033[F", end="")

if __name__ == "__main__":
	while True:
		try:
			clear()
			draw()
			backspace()
			time.sleep(1)
		except KeyboardInterrupt:
			clear()
			draw()
			sys.exit()

