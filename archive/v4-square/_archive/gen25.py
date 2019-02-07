import sys

# Global count of valid cards
valid = 0

# Include 2 and 5 edges
sides = [0,1,2,3,4,5,6,7]

side_map = ['000','001','010','011','100','101','110','111']

# Number of auto-gen decks (excluding extra cards)
decks = 1

deck = []

process_extra_cards = False

extra_cards = [
]

print 'island test'

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

	return True

def add_card(card):
	global valid
	valid += 1

	deck.append(card)

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
	print_edge_count()
	print_corner_count()
	print_edge3_count()

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
