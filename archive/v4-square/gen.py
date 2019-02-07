import sys

# Global count of valid cards
valid = 0

sides = [0,1,3,4,6,7]

side_map = ['000','001','010','011','100','101','110','111']

# Number of auto-gen decks (excluding extra cards)
decks = 2

deck = []

process_extra_cards = True

extra_cards = [
	[0, 1, 7, 4],
	[0, 1, 7, 6],
	[0, 3, 7, 4],
	[0, 3, 7, 6],

	[0, 0, 3, 6],
	[1, 7, 7, 4],

	[0, 0, 1, 4],
	[3, 7, 7, 6],

	#[0, 0, 0, 0],

	[0, 0, 1, 4],
	[0, 0, 1, 6],
	[0, 0, 3, 4],
	[0, 0, 3, 6],

	[0, 1, 7, 4],
	[0, 1, 7, 6],
	[0, 3, 7, 4],
	[0, 3, 7, 6],

	[1, 4, 1, 4],
	[1, 4, 1, 6],
	[1, 4, 3, 4],	# 1
	#[1, 4, 3, 6],	# 2

	[1, 6, 1, 6],
	#[1, 6, 3, 4],	# 2
	[1, 6, 3, 6],	# 1

	[1, 7, 7, 4],
	[1, 7, 7, 6],

	[3, 4, 3, 4],
	[3, 4, 3, 6],
	[3, 6, 3, 6],

	[3, 7, 7, 4],
	[3, 7, 7, 6],

	#[7, 7, 7, 7],
]

"""
Corners:
		0014	0034
		0016	0036	1434	0014	0174	1414
		1414	3434	1436	0016	0176	1416	1616			3434
		1416	3436	1634	0034	0374	1434	1634	1774	3436	3774
		1616	3636	1636	0036	0376	1436	1636	1776	3636	3776	|
00 x8	..		..				....													|
01 x4	..						..		..												|
03 x4			..				..		..												|
14 x6	....			..		.				.....									|
16 x6	....			..		.				.		....							|
17 x4									..						..						|
34 x6			....	..		.				.		.				..				|
36 x6			....	..		.				.		.				..				|
37 x4									..										..		|
40 x4	.		.				..		..												|
41 x6	...				..						....	.		.						|
43 x6			...		..						..						..		.		|
60 x4	.		.				..		..												|
61 x6	...				..						..		...		.						|
63 x6			...		..								..				..		.		|
74 x4									..						.				.		|
76 x4									..						.				.		|
77 x8															..				..		|
"""

# [land, water, topo, resources]
# topo:
#  l: all land
#  w: all water
#  lw: land-water connections
#  dlp: dead-end (land) or port
#  dwp: dead-end (water) or port
#  2p: double port or double-deadend (-land or -water)
#  2pl: double port or land-water or double-deadend-land
#  2pw: double port or land-water or double-deadend-water

# Initial random dist
"""
card_info_orig = {
	   0: [0, 4, 'w',	[['p:w', 'b:w', 'h:w', 'c:w'], ['fjst:wwww']]],
	  14: [0, 4, 'w',	[['f:wwww'], ['s:wwww'], ['t:wwww'], ['j:wwww']]],
	  16: [1, 3, 'dlp',	[['f:lwww'], ['h:l', ':www'], ['b:l', ':www']]],
	  34: [1, 3, 'dlp',	[['b:l', ':www'], ['j:lwww'], ['c:l', ':www']]],
	  36: [2, 2, 'lw',	[[':ll', 't:ww'], [':ll', 's:ww'], ['h:ll', ':ww'], ['p:ll', ':ww']]],
	 174: [1, 3, 'dlp',	[['b:lwww'], ['f:lwww'], ['h:l', ':www'], ['c:l', ':www']]],
	 176: [2, 2, 'lw',	[[':ll', 't:ww'], ['c:ll', ':ww'], ['h:ll', ':ww'], [':ll', 's:ww']]],
	 374: [2, 2, 'lw',	[['b:ll', ':ww'], [':ll', 'f:ww'], ['c:ll', ':ww'], [':ll', 'j:ww']]],
	 376: [3, 1, 'dwp',	[[':lll', 't:w'], ['s:lllw'], [':lll', 'j:w'], ['b:lllw']]],
	1414: [0, 4, 'w',	[['s:wwww'], ['t:wwww'], [':ww', 'j:ww']]],
	1416: [1, 3, 'dlp',	[['t:lwww'], ['p:l', ':www'], ['c:lw', ':ww']]],
	1434: [1, 3, 'dlp',	[['p:lw', ':ww'], ['t:lwww'], ['p:l', ':www']]],
	1436: [2, 2, '2pw',	[[':ll', 'f:ww'], ['bs:llww']]],
	1616: [2, 2, '2p',	[['cj:llww'], [':ll', 'f:w', 's:w'], ['c:l', 'p:l', ':ww']]],
	1634: [2, 2, '2pl',	[['b:ll', ':ww'], ['pt:llww']]],
	1636: [3, 1, 'dwp',	[[':lll', 's:w'], [':ll', 'h:lw'], ['j:lllw']]],
	1774: [2, 2, 'lw',	[['p:ll', ':ww'], [':ll', 'j:ww'], [':ll', 'f:ww'], ['b:ll', ':ww']]],
	1776: [3, 1, 'dwp',	[['p:lllw'], [':lll', 's:w'], [':lll', 'f:w']]],
	3434: [2, 2, '2p',	[[':ll', 'j:w', 't:w'], ['b:l', 'h:l', ':ww'], ['fh:llww']]],
	3436: [3, 1, 'dwp',	[[':ll', 'c:lw'], ['s:lllw'], [':lll', 'f:w']]],
	3636: [4, 0, 'l',	[['h:llll'], ['c:llll'], [':ll', 'p:ll']]],
	3774: [3, 1, 'dwp',	[[':lll', 't:w'], ['h:lllw'], [':lll', 'j:w']]],
	3776: [4, 0, 'l',	[['h:llll'], ['p:llll'], ['c:llll'], ['b:llll']]],
	7777: [4, 0, 'l',	[['f:l', 'j:l', 's:l', 't:l'], ['bchp:llll']]],
}
"""

# Test redistribution:
# Balance edges connected to each resource
# Snapshot 0:
# 174: [1, 3, 'dlp',	[['b:lwww'], ['f:lwww'], ['h:l', ':www'], ['c:l', ':www']]],
#1416: [1, 3, 'dlp',	[['t:lwww'], ['p:l', ':www'], ['c:lw', ':ww']]],
#1434: [1, 3, 'dlp',	[['p:lw', ':ww'], ['t:lwww'], ['p:l', ':www']]],
#1616: [2, 2, '2p',	[['cj:llww'], [':ll', 'f:w', 's:w'], ['c:l', 'p:l', ':ww']]],
#3436: [3, 1, 'dwp',	[[':ll', 'c:lw'], ['s:lllw'], [':lll', 'f:w']]],
#3774: [3, 1, 'dwp',	[[':lll', 't:w'], ['h:lllw'], [':lll', 'j:w']]],

card_info = {
	   0: [0, 4, 'w',	[['p:w:0', 'b:w:0', 'h:w:0', 'c:w:0'], ['fjst:wwww:0000']]],
	  14: [0, 4, 'w',	[['f:wwww:0014'], ['s:wwww:0014'], ['t:wwww:0014'], ['j:wwww:0014']]],
	  16: [1, 3, 'dlp',	[['f:lwww:0016'], ['h:l:6', ':www:001'], ['b:l:6', ':www:001']]],
	  34: [1, 3, 'dlp',	[['b:l:3', ':www:004'], ['j:lwww:0034'], ['c:l:3', ':www:004']]],
	  36: [2, 2, 'lw',	[[':ll:36', 't:ww:00'], [':ll:36', 's:ww:00'], ['h:ll:36', ':ww:00'], ['p:ll:36', ':ww:00']]],
	 174: [1, 3, 'dlp',	[['b:lwww:0174'], ['h:lwww:0174'], ['p:l:7', ':www:014'], ['c:l:7', ':www:014']]],
	 176: [2, 2, 'lw',	[[':ll:76', 't:ww:01'], ['c:ll:76', ':ww:01'], ['h:ll:76', ':ww:01'], [':ll:76', 's:ww:01']]],
	 374: [2, 2, 'lw',	[['b:ll:37', ':ww:04'], [':ll:37', 'f:ww:04'], ['c:ll:37', ':ww:04'], [':ll:37', 'j:ww:04']]],
	 376: [3, 1, 'dwp',	[[':lll:376', 't:w:0'], ['s:lllw:0376'], [':lll:376', 'j:w:0'], ['b:lllw:0376']]],
	1414: [0, 4, 'w',	[['s:wwww:1414'], ['t:wwww:1414'], [':ww:14', 'j:ww:14']]],
	1416: [1, 3, 'dlp',	[['c:lwww:1416'], ['p:l:6', ':www:141'], ['s:lw:16', ':ww:14']]],
	#1434: [1, 3, 'dlp',	[['t:lw:43', ':ww:14'], ['p:lwww:1434'], ['p:l:3', ':www:144']]],
	1434: [1, 3, 'dlp',	[['t:lw:43', ':ww:14'], ['p:lwww:1434'], ['h:l:3', ':www:144']]],
	1436: [2, 2, '2pw',	[[':ll:36', 'f:ww:14'], ['bs:llww:1436']]],
	#1616: [2, 2, '2p',	[['cj:llww:1616'], [':ll:66', 'f:w:1', 's:w:1'], ['c:l:6', 'h:l:6', ':ww:11']]],
	1616: [2, 2, '2p',	[['cj:llww:1616'], [':ll:66', 'f:w:1', 's:w:1'], ['c:l:6', 'p:l:6', ':ww:11']]],
	1634: [2, 2, '2pl',	[['b:ll:63', ':ww:14'], ['pt:llww:1634']]],
	1636: [3, 1, 'dwp',	[[':lll:636', 's:w:1'], [':ll:36', 'h:lw:16'], ['j:lllw:1636']]],
	1774: [2, 2, 'lw',	[['p:ll:77', ':ww:14'], [':ll:77', 'j:ww:14'], [':ll:77', 'f:ww:14'], ['b:ll:77', ':ww:14']]],
	1776: [3, 1, 'dwp',	[['p:lllw:1776'], [':lll:776', 's:w:1'], [':lll:776', 'f:w:1']]],
	3434: [2, 2, '2p',	[[':ll:33', 'j:w:4', 't:w:4'], ['b:l:3', 'h:l:3', ':ww:44'], ['fh:llww:3434']]],
	3436: [3, 1, 'dwp',	[[':ll:36', 'c:lw:34'], ['t:lllw:3436'], [':lll:336', 'f:w:4']]],
	3636: [4, 0, 'l',	[['h:llll:3636'], ['c:llll:3636'], [':ll:36', 'p:ll:36']]],
	3774: [3, 1, 'dwp',	[[':lll:377', 't:w:4'], ['f:lllw:3774'], [':lll:377', 'j:w:4']]],
	3776: [4, 0, 'l',	[['h:llll:3776'], ['p:llll:3776'], ['c:llll:3776'], ['b:llll:3776']]],
	7777: [4, 0, 'l',	[['f:l:7', 'j:l:7', 's:l:7', 't:l:7'], ['bchp:llll:7777']]],
}

"""
0000 	B	C	F	H	J	P	S	T
0014 			F		J		S	T
0016 	B		F	H
0034 	B	C			J
0036 				H		P	S	T
0174 	B	C		H		P
0176 		C		H			S	T
0374 	B	C	F		J
0376 	B				J		S	T
1414 					J		S	T
1416 		C				P	S
1434 						PP		T
1436 	B		F				S
1616 		CC	F	H	J		S
1634 	B					P		T
1636 				H	J		S
1774 	B		F		J	P
1776 			F			P	S
3434 	B		F	HH	J			T
3436 		C	F					T
3636 		C		H		P
3774 			F		J			T
3776 	B	C		H		P
7777 	B	C	F	H	J	P	S	T
"""

print 'island test'
print 'decks =', decks

# Track card types
deck_card_types = {}
for k,v in card_info.iteritems():
	type = v[2]
	deck_card_types[type] = 0

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

# Three edge count
edge3_count_cards = []
for e1 in range(8):
	edge3_count_cards.append([])
	for e2 in range(8):
		edge3_count_cards[e1].append([])
		for e3 in range(8):
			edge3_count_cards[e1][e2].append(0)

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

def add_card(card):
	global valid
	valid += 1

	deck.append(card)

	info = card_info[card2val(card)]
	deck_card_types[info[2]] += 1

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

	edge3s = {}
	for x in xrange(0,4):
		edge1 = card[x]
		edge2 = card[(x+1)%4]
		edge3 = card[(x+2)%4]
		e3 = '%d-%d-%d' % (edge1, edge2, edge3)
		edge3s[e3] = True
	for e3 in edge3s:
		(edge1, edge2, edge3) = e3.split('-')
		edge3_count_cards[int(edge1)][int(edge2)][int(edge3)] += 1

def print_card(card):
	out = '.'.join([side_map[x] for x in card])
	num = ''.join([str(x) for x in card])
	print '%s = %s' % (out, num)

def print_global_stats():
	print_card_types()
	print_edge_count()
	print_corner_count()
	print_edge3_count()

def print_card_types():
	print
	print 'card types'
	for k in sorted(deck_card_types.iterkeys()):
		print k, deck_card_types[k]

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

def print_edge3_count():
	print
	print 'edge3 count (total cards match edge3)'
	data = []
	data_max = 10
	for e1 in sides:
		for e2 in sides:
			# Make sure the edges have a valid connection.
			if side_map[e1][-1] == side_map[e2][0]:
				for e3 in sides:
					# Make sure the edges have a valid connection.
					if side_map[e2][-1] == side_map[e3][0]:
						count = '*' * edge3_count_cards[e1][e2][e3]
						while len(count) < data_max:
							count += ' '
						data.append([e1, e2, e3, count])
	for x in reversed(xrange(0,data_max)):
		for d in data:
			sys.stdout.write(d[3][x])
		sys.stdout.write('\n')
	for x in xrange(0,3):
		for d in data:
			sys.stdout.write(str(d[x]))
		sys.stdout.write('\n')

def print_total_deck_info():
	# Verify card_info
	land_edges = 0
	water_edges = 0
	connections = {'b':'', 'c':'', 'h':'', 'p':'', 'f':'', 'j':'', 's':'', 't':'', '':''}
	res_count = {'b':0, 'c':0, 'h':0, 'p':0, 'f':0, 'j':0, 's':0, 't':0}
	p_res_count = {'b':0, 'c':0, 'h':0, 'p':0, 'f':0, 'j':0, 's':0, 't':0}
	dp_res_count = {'b':0, 'c':0, 'h':0, 'p':0, 'f':0, 'j':0, 's':0, 't':0}
	deadend_res_count = {'b':0, 'c':0, 'h':0, 'p':0, 'f':0, 'j':0, 's':0, 't':0}
	res_cards = {'b':{}, 'c':{}, 'h':{}, 'p':{}, 'f':{}, 'j':{}, 's':{}, 't':{}}
	res_card_edges = {'b':{}, 'c':{}, 'h':{}, 'p':{}, 'f':{}, 'j':{}, 's':{}, 't':{}}
	for k,v in card_info.iteritems():
		land = v[0]
		water = v[1]
		card_resources = v[3]
		land_edges += land
		water_edges += water
		for res in card_resources:
			card_land_edges = 0
			card_water_edges = 0
			card_edges = ''
			for res_connect in res:
				(res, type, edges) = res_connect.split(':')
				for r in res:
					connections[r] += type
					res_count[r] += 1
					if not type in res_cards[r]:
						res_cards[r][type] = []
					res_cards[r][type].append(k)
					if 'l' in type and 'w' in type:
						if len(res) == 2:
							dp_res_count[r] += 1
						else:
							p_res_count[r] += 1
					elif len(type) == 1:
						deadend_res_count[r] += 1
					for e in edges:
						if not e in res_card_edges[r]:
							res_card_edges[r][e] = 0
						res_card_edges[r][e] += 1
				if res == '':
					connections[''] += type
				for t in type:
					if t == 'l':
						card_land_edges += 1
					if t == 'w':
						card_water_edges += 1
				card_edges += edges

			if card_land_edges != land or card_water_edges != water:
				print 'mismatch l/w edges for', k
				sys.exit(1)

			if len(card_edges) != 4:
				print 'mismatch edges for', k
				sys.exit(1)
			edges1 = ''.join(sorted([str(x) for x in ('%04d' % k)]))
			edges2 = ''.join(sorted([str(x) for x in card_edges]))
			if edges1 != edges2:
				print 'mismatch edges for', k, ':', edges1, '!=', edges2
				sys.exit(1)

	print
	print 'land', land_edges, 'water', water_edges
	for r in res_count:
		if res_count[r] != 12:
			print 'invalid res count for', r
			print res_count
			sys.exit(1)
	for r in p_res_count:
		if p_res_count[r] != 2:
			print 'invalid p res count for', r
			print p_res_count
			sys.exit(1)
	for r in dp_res_count:
		if dp_res_count[r] != 1:
			print 'invalid dp res count for', r
			print dp_res_count
			sys.exit(1)
	for r in deadend_res_count:
		if deadend_res_count[r] != 4:
			print 'invalid deadend res count for', r
			print deadend_res_count
			sys.exit(1)

	for k in ['', 'b', 'c', 'h', 'p', 'f', 'j', 's', 't']:
		land = 0
		water = 0
		for c in connections[k]:
			if c == 'l':
				land += 1
			if c == 'w':
				water += 1
		print k, '%s%s' % ('l'*land, 'w'*water), land, water

	for k in ['b', 'c', 'h', 'p', 'f', 'j', 's', 't']:
		sys.stdout.write(k)
		for c in sorted(res_cards[k].iterkeys()):
			print '\t', c, res_cards[k][c]

	print
	for e in [0, 1, 3, 4, 6, 7]:
		sys.stdout.write('\t%d' % e)
	print
	for k in ['b', 'c', 'h', 'p', 'f', 'j', 's', 't']:
		sys.stdout.write(k)
		for e in [0, 1, 3, 4, 6, 7]:
			sys.stdout.write('\t%d' % res_card_edges[k][str(e)])
		print


for s1 in sides:
	for l1 in sides:
		for s2 in sides:
			for l2 in sides:
				card = [s1, l1, s2, l2]
				if validate(card):
					print_card(card)
					for d in xrange(decks):
						add_card(card)

print 'auto-gen cards', valid

print_global_stats()

# process extra cards
if process_extra_cards:
	bad_cards = 0
	print
	print 'with extra cards'
	for card in extra_cards:
		if validate(card):
			add_card(card)
			print_card(card)
		else:
			print 'ERROR - invalid extra card:', card
			bad_cards += 1

	print_global_stats()

	if bad_cards != 0:
		print 'ERROR - bad cards found'

print_total_deck_info()
