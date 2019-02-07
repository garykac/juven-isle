#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Global count of valid cards
valid = 0

sides = [0,1,3,4,6,7]
side_map = ['000','001','010','011','100','101','110','111']

res_land = ['b','c','h']
res_water = ['f','s','t']
resources = res_land + res_water

deck = []

# [land, water, connections, topo, card-resource-info]
# topo:
#  l: all land
#  w: all water
#  lw: land-water connections
#  dlp: dead-end (land) or port
#  dwp: dead-end (water) or port
#  2d: double-deadend (-land or -water)
#  2dl: land-water or double-deadend-land
#  2dw: land-water or double-deadend-water
# -x: can pirate
#
# r = resource, p = port, x = pirate
card_info = {
	   0: [0, 4, 'wwww', 'w-x',		[
	     	['3rw', 'fst'],
	     	['xw', 'fst']]],
	  14: [0, 4, 'wwww', 'w-x',		[
	     	['rw', 'f'],
	     	['xw', 'fst'],
	     	['xw', 'fst']]],
	  16: [1, 3, 'lwww', 'dl-p',	[
	     	['pl', 'c', 'Davenport'],
	     	['pw', 's', 'Port Cullis'],
	     	['rdl', 'b']]],
	  34: [1, 3, 'lwww', 'dl-p',	[
	     	['pl', 'h', 'Rose Port'],
	     	['pw', 'f', 'Port Ico'],
	     	['rdl', 'c']]],
	  36: [2, 2, 'llww', 'lw-p-x',	[
	     	['pw', 'f', 'Port Folio'],
	     	['rl', 'b'],
	     	['rw', 's']]],
	 174: [1, 3, 'lwww', 'dl-p',	[
	     	['pl', 'c', 'Port-au-Bella'],
	     	['pw', 's', 'Port Manteau'],
	     	['rdl', 'h']]],
	 176: [2, 2, 'llww', 'lw-p-x',	[
	     	['pl', 'b', 'Port Lee'],
	     	['pw', 't', 'Ruby Port'],
	     	['rl', 'h']]],
	 374: [2, 2, 'llww', 'lw-p-x',	[
	     	['pl', 'h', 'Port Starboard'],
	     	['pw', 'f', 'Spoils Port'],
	     	['rw', 't']]],
	 376: [3, 1, 'lllw', 'dw-p',	[
	     	['pl', 'b', 'Crusted Port'],
	     	['pw', 's', 'Port Royale'],
	     	['rdw', 't']]],
	1414: [0, 4, 'wwww', 'w-x',		[
	     	['rw', 's', 'Kidneystone Pass'],
	     	['xw', 'fst', 'Noneshall Pass']]],
	1416: [1, 3, 'lwww', 'dl-p',	[
	     	['pl', 'c', 'Port-au-Potée'],
	     	['pw', 't', 'Port Hole'],
	     	['rdl', 'h']]],
	1434: [1, 3, 'lwww', 'dl-p',	[
	     	['pl', 'h', 'Back Port'],
	     	['pw', 'f', 'Tawny Port'],
	     	['rdl', 'b'],
	     	['rdl', 'c']]],
	1436: [2, 2, 'llww', '2dw-p-x',	[
	     	['pl', 'b', 'Port Judgement'],
	     	['pw', 't', 'Port Able'],		# s -> t
	     	['2rdw', 'fs'],
	     	['rw', 't']]],
	1616: [2, 2, 'llww', '2d',		[
	     	['2rdl', 'bc'],
	     	['2rdw', 'tf']]],
	1634: [2, 2, 'llww', '2dl-p-x',	[
	     	['pl', 'c', 'Serial Port'],
	     	['pw', 't', 'Newport'],
	     	['2rdl', 'hb', 'Letme Inlet'],
	     	['rl','c']]],
	1636: [3, 1, 'lllw', 'dw-p',	[
	     	['pl', 'h', 'Grande Port'],
	     	['pw', 'f', 'Watersport'],
	     	['rdw', 's'],
	     	['rdw', 't']]],
	1774: [2, 2, 'llww', 'lw-p-x',	[
	     	['pl', 'c', 'Freeport'],
	     	['rl', 'b'],
	     	['rw', 'f']]],
	1776: [3, 1, 'lllw', 'dw-p',	[
	     	['pl', 'b', 'Port End'],
	     	['pw', 's', 'Port Tristam'],
	     	['rdw', 'f']]],
	3434: [2, 2, 'llww', '2d',		[
	     	['2rdl', 'ch'],
	     	['2rdw', 'st']]],
	3436: [3, 1, 'lllw', 'dw-p',	[
	     	['pl', 'h', 'Morgansport'],
	     	['pw', 's', 'Port Ray'],		# t -> s
	     	['rdw', 's']]],
	3636: [4, 0, 'llll', 'l-x',		[
	     	['rl', 'c'],
	     	['xl', 'bch']]],
	3774: [3, 1, 'lllw', 'dw-p',	[
	     	['pl', 'b', 'Port Quinta'],
	     	['pw', 't', 'Port Roberts'],
	     	['rdw', 'f']]],
	3776: [4, 0, 'llll', 'l-p',		[
	     	['rl', 'h'],
	     	['xl', 'bch'],
	     	['xl', 'bch']]],
	7777: [4, 0, 'llll', 'l-p',		[
	     	['3rl', 'bch'],
	     	['xl', 'bch']]],
}

card_types = [
	'pl',	# port land
	'pw',	# port water
	'rl',	# resource land
	'rw',	# resource water
	'rdl',	# resource land deadend
	'rdw',	# resource water deadend
	'2rdl',	# 2 resource land (deadends)
	'2rdw',	# 2 resource water (deadends)
	'3rl',	# 3 resource land (fully connected)
	'3rw',	# 3 resource water (fully connected)
	'xl',	# pirate land
	'xw',	# pirate water
]

print 'island test - square, resources=6'

# Track card topo types (lw, dl, ...)
card_topo_types = {}
for k,v in card_info.iteritems():
	type = v[3]
	card_topo_types[type] = 0

card_type_info = {}
for t in card_types:
	card_type_info[t] = 0

res_count = {}
for t in card_types:
	res_count[t] = {}
	for r in resources:
		res_count[t][r] = 0
	
# Track count of edge type.
# If type occurs twice on a single card, it is counted twice.
edge_count = {}
# Track cards with at least one edge of type X
# If type occurs twice on a single card, it is counted once.
edge_count_cards = {}
for x in range(8):
	edge_count[x] = 0
	edge_count_cards[x] = 0

# Corner (2 edge) count
corner_count = []
corner_count_cards = []
for s in range(8):
	corner_count.append([])
	corner_count_cards.append([])
	for l in range(8):
		corner_count[s].append(0)
		corner_count_cards[s].append(0)

def card2string(card):
	return ''.join([str(x) for x in card])

def card2val(card):
	return card[0]*1000 + card[1]*100 + card[2]*10 + card[3]

def validate(card):
	# Make sure the edges have a valid connection.
	for i in range(len(card)):
		next = i + 1
		if next >= len(card):
			next = 0
		if side_map[card[i]][-1] != side_map[card[next]][0]:
			return False

	# Remove symmetry tiles.
	if True:
		val = card2val(card)

		# Remove 90-degree rotation duplicates.
		if val > card2val(card[1:] + card[:1]):
			return False

		# Remove 180-degree rotation duplicates.
		if val > card2val(card[2:] + card[:2]):
			return False

		# Remove 270-degree rotation duplicates.
		if val > card2val(card[3:] + card[:3]):
			return False

	# Make sure we have card info for this card.
	if not card2val(card) in card_info:
		print 'no card info for', card
		sys.exit(1)

	return True

def add_card(card, info):
	global valid
	valid += 1

	deck.append(card)

	general_card_info = card_info[card2val(card)]
	card_topo_types[general_card_info[3]] += 1

	type = info[0]
	res = info[1]
	card_type_info[type] += 1
	for r in res:
		res_count[type][r] += 1;
	
	edges = {}
	for x in xrange(0,4):
		edge_count[card[x]] += 1
		edges[card[x]] = True
	for edge in edges:
		edge_count_cards[edge] += 1

	corners = {}
	for x in xrange(0,4):
		edge1 = card[x]
		edge2 = card[(x+1)%4]
		corner_count[edge1][edge2] += 1
		corner = '%d-%d' % (edge1, edge2)
		corners[corner] = True
	for corner in corners:
		(edge1, edge2) = corner.split('-')
		corner_count_cards[int(edge1)][int(edge2)] += 1

def print_card(card):
	out = '.'.join([side_map[x] for x in card])
	num = ''.join([str(x) for x in card])
	print '%s = %s' % (out, num)

def print_global_stats():
	print_card_types()
	print_resources()
	print_edge_count()
	print_corner_count()

def print_card_types():
	print
	print 'card topo types'
	for k in sorted(card_topo_types.iterkeys()):
		print k, card_topo_types[k]

	print
	print 'card types'
	for k in sorted(card_type_info.iterkeys()):
		print k, card_type_info[k]

def print_resources():
	print
	print 'resource count'

	print '%-5s' % '',
	for r in resources:
		print '%-3s' % r,
	print

	for t in card_types:
		res_type = 'land'
		res_list = res_land
		if t[-1] == 'w':
			res_type = 'water'
			res_list = res_water
			
		print '%-5s' % t,
		if res_type == 'water':
			for x in xrange(3):
				print '%-3s' % '-',

		first = True
		all_match = True
		val = 0
		for r in res_list:
			print '%-3s' % res_count[t][r],
			if first:
				val = res_count[t][r]
				first = False
			else:
				if val != res_count[t][r]:
					all_match = False

		if res_type == 'land':
			for x in xrange(3):
				print '%-3s' % '-',

		if not all_match:
			print '  *** mitmatch',
		print
		
def print_edge_count():
	print
	print 'edge count'
	for x in sides:
		print 'sides', side_map[x], '=', edge_count[x], '(edges)', edge_count_cards[x], '(cards)'

def print_corner_count():
	edge_count_check = 0

	print
	print 'edge1-edge2 (total corners)'
	print ' '.join(list('      edge2'))
	print ' ', ' ',
	for x in range(8):
		print '%2d' % x,
	print
	col_label = ' edge1   '
	for s in range(8):
		print col_label[s], s,
		for l in range(8):
			if side_map[s][-1] != side_map[l][0]:
				print ' -',
			else:
				print '%2d' % corner_count[s][l],
				edge_count_check += corner_count[s][l]
		print

	print 'total edges', edge_count_check
	print 'total cards (calc from edges)', (edge_count_check / 4)

	print
	print 'edge1-edge2 (total cards with corners)'
	print ' '.join(list('      edge2'))
	print ' ', ' ',
	for x in range(8):
		print '%2d' % x,
	print
	col_label = ' edge1   '
	for s in range(8):
		print col_label[s], s,
		for l in range(8):
			if side_map[s][-1] != side_map[l][0]:
				print ' -',
			else:
				print '%2d' % corner_count_cards[s][l],
		print

for s1 in sides:
	for l1 in sides:
		for s2 in sides:
			for l2 in sides:
				card = [s1, l1, s2, l2]
				if validate(card):
					print_card(card)
					info = card_info[card2val(card)]
					for i in info[4]:
						add_card(card, i)

print 'auto-gen cards', valid

print_global_stats()
