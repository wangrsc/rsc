#!/usr/bin/env python3

import numpy as np


def shift_array(input_2d_array, x, y):
	"""
	This program shift the array from (1,1) to (x,y)
	args:
		input_2d_array: 2D array to be shifted
		x, y: shift from (1,1) to (x,y)

	:return:
		shifted 2D array
	"""

	input_2d_array = np.squeeze(np.array(input_2d_array))

	shape = input_2d_array.shape

	if len(shape) != 2:
		print('Input is not a 2D array. Nothing is done.')
		return input_2d_array

	mx = shape[0]
	my = shape[1]

	if x > mx or y > my or x < 1 or y < 1:
		print("shift is out of range")

	out = np.zeros([mx, my])
	out[x-1:mx, y-1:my] = input_2d_array[1-1:mx-x+1, 1-1:my-y+1]
	out[1-1: x - 1, 1-1: y - 1] = input_2d_array[mx - x + 2-1:mx, my-y+2-1:my]
	out[1-1: x - 1, y-1: my] = input_2d_array[mx - x + 2-1:mx, 1-1:my-y+1]
	out[x-1: mx, 1-1: y - 1] = input_2d_array[1-1:mx-x+1, my-y+2-1:my]

	return out


if __name__ == "__main__":
	data = np.arange(20).reshape(4, 5)
	b = shift_array(data, 3, 4)
	print(data)
	print('--------------')
	print(b)
