#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#import re
#import subprocess
#import sys

from svglib.svggen import SvgGen
from svglib.svgdef import *

class Gen12Up(object):
	def __init__(self):
		self.svg = SvgGen()
		
		# 8.5" x 11" @ 90dpi
		self.width = 765
		self.height = 990

		self.cards_per_row = 3
		self.cards_per_column = 4
		self.cards_per_page = self.cards_per_row * self.cards_per_column
				
		# True if we have a currently open page.
		self.in_page = False
		
		# Current page index.
		self.curr_page = 0

		# Number of cards on the current page.
		self.num_cards = 0
	
	def start_page(self):
		self.curr_page += 1
		print 'starting page', self.curr_page
		self.in_page = True
		self.svg.reset()
		self.svg.set_size(self.width, self.height)
		self.svg.set_filename('sheets-out/letter12-%02d.svg' % self.curr_page)
		self.svg.begin()
	
	def end_page(self):
		print 'ending page'
		self.svg.end()
		self.in_page = False
		self.num_cards = 0
			
	def add_card(self, name):
		if not self.in_page:
			self.start_page()
		
		ix = self.num_cards % self.cards_per_row
		iy = int(self.num_cards / self.cards_per_row)
		print '  adding', name, 'at', ix, iy
		
		x_offset = [20.435625, 260.12457, 499.81354]
		y_offset = [14.481866, 254.17081, 493.85983, 733.54871]
		x = x_offset[ix]
		y = y_offset[iy]

		self.svg.image(x, y, 246.6, 246.6, '../png-out/%s' % name)

		self.num_cards += 1		
		if self.num_cards == self.cards_per_page:
			self.end_page()
		
	def gen(self):
		for filename in sorted(os.listdir('png-out')):
			if filename[0] != '.':
				self.add_card(filename)

		if self.in_page:
			self.end_page()
			
def main():
	output = Gen12Up()
	output.gen()

if __name__ == '__main__':
	main()
