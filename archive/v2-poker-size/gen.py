
short_sides = [0,1,3,4,6,7]
long_sides = [0,1,3,4,6,7]

side_map = ['000','001','010','011','100','101','110','111']

extra_cards = [
	[0, 1, 7, 4],
	[0, 1, 7, 6],
	[0, 3, 7, 4],
	[0, 3, 7, 6],
	[1, 7, 4, 0],
	[1, 7, 6, 0],
	[3, 7, 4, 0],
	[3, 7, 6, 0],
]

deck = []

print 'island test'

valid = 0

# Track count of short edge type.
# If type occurs twice on a single card, it is counted twice.
short_count = {}
for x in short_sides:
	short_count[x] = 0

# Track count of long edge type.
# If type occurs twice on a single card, it is counted twice.
long_count = {}
for x in long_sides:
	long_count[x] = 0

# Track count of short edge type.
# If type occurs twice on a single card, it is counted once.
short_count_card = {}
for x in short_sides:
	short_count_card[x] = 0

# Track count of long edge type.
# If type occurs twice on a single card, it is counted once.
long_count_card = {}
for x in long_sides:
	long_count_card[x] = 0

sl_count = []
for s in range(8):
	sl_count.append([])
	for l in range(8):
		sl_count[s].append(0)

ls_count = []
for l in range(8):
	ls_count.append([])
	for s in range(8):
		ls_count[l].append(0)

sls_count = []
for s1 in range(8):
	sls_count.append([])
	for l in range(8):
		sls_count[s1].append([])
		for s2 in range(8):
			sls_count[s1][l].append(0)

lsl_count = []
for l1 in range(8):
	lsl_count.append([])
	for s in range(8):
		lsl_count[l1].append([])
		for l2 in range(8):
			lsl_count[l1][s].append(0)

def card2string(card):
	return ''.join([str(x) for x in card])
	
def validate(card):
	# Make sure the edges have a valid connection.
	for i in range(len(card)):
		next = i + 1
		if next >= len(card):
			next = 0
		if side_map[card[i]][-1] != side_map[card[next]][0]:
			return False

	# Remove 180-degree rotation duplicates.
	if card[0]*10 + card[1] > card[2]*10 + card[3]:
		return False
		
	return True

def add_card(card):
	global valid
	valid += 1

	deck.append(card)
	
	short_count[card[0]] += 1
	short_count[card[2]] += 1
	long_count[card[1]] += 1
	long_count[card[3]] += 1

	short_count_card[card[0]] += 1
	if card[0] != card[2]:
		short_count_card[card[2]] += 1
	long_count_card[card[1]] += 1
	if card[1] != card[3]:
		long_count_card[card[3]] += 1

	sl_count[card[0]][card[1]] += 1
	#if card[0] != card[2] or card[1] != card[3]:
	sl_count[card[2]][card[3]] += 1
	ls_count[card[1]][card[2]] += 1
	#if card[1] != card[3] or card[2] != card[0]:
	ls_count[card[3]][card[0]] += 1

	sls_count[card[0]][card[1]][card[2]] += 1
	#if card[0] != card[2] or card[1] != card[3]:
	sls_count[card[2]][card[3]][card[0]] += 1
	lsl_count[card[1]][card[2]][card[3]] += 1
	#if card[1] != card[3] or card[2] != card[0]:
	lsl_count[card[3]][card[0]][card[1]] += 1

def print_card(card):
	out = '.'.join([side_map[x] for x in card])
	num = ''.join([str(x) for x in card])
	print '%s = %s' % (out, num)

def print_global_stats():
	print_edge_count()
	print_edge_pair_count()
	#print_edge_triple_count()
	card_match_probs()

def print_edge_count():
	print
	print 'edge count'
	for x in short_sides:
		print 'short', side_map[x], '=', short_count[x], short_count_card[x]
	for x in long_sides:
		print 'long', side_map[x], '=', long_count[x], long_count_card[x]

def print_edge_pair_count():
	edge_count = 0

	print
	print 'short-long'
	print ' '.join(list('   long'))
	print ' ', ' ',
	for x in range(8):
		print x,
	print
	col_label = ' short   '
	for s in range(8):
		print col_label[s], s,
		for l in range(8):
			if side_map[s][-1] != side_map[l][0]:
				print '-',
			else:
				print sl_count[s][l],
				edge_count += sl_count[s][l]
		print

	print
	print 'long-short'
	print ' '.join(list('   short'))
	print ' ', ' ',
	for x in range(8):
		print x,
	print
	col_label = '  long   '
	for l in range(8):#long_sides:
		print col_label[l], l,
		for s in range(8):#short_sides:
			if side_map[l][-1] != side_map[s][0]:
				print '-',
			else:
				print ls_count[l][s],
				edge_count += ls_count[l][s]
		print

	print 'total edges', edge_count
	print 'total cards (calc from edges)', (edge_count / 4)

def print_edge_triple_count():
	print 'short-long-short'
	for s1 in range(8):
		for l in range(8):
			for s2 in range(8):
				if sls_count[s1][l][s2] != 0:
					print s1, l, s2, '=', sls_count[s1][l][s2]

	print 'long-short-long'
	for l1 in range(8):
		for s in range(8):
			for l2 in range(8):
				if lsl_count[l1][s][l2] != 0:
					print l1, s, l2, '=', lsl_count[l1][s][l2]

def card_match_probs():
	print
	print 'table'
	cards = len(deck)
	done = {}
	for c1 in range(len(deck)):
		d2 = list(deck)
		del d2[c1]

		print deck[c1],
		
		# Prob of matching with 1 card
		count = 0
		for c2 in range(len(d2)):
			if card_match(deck[c1], d2[c2]):
				count += 1
		print '%0.01f%%' % (100.0 * count / (cards-1)),

		# Prob of matching with 2 cards
		count = 0
		for c2 in range(len(d2)):
			d3 = list(d2)
			del d3[c2]
			for c3 in range(len(d3)):
				if (card_match(deck[c1], d2[c2])
						or card_match(deck[c1], d3[c3])):
					count += 1
		print '%0.01f%%' % (100.0 * count / ((cards-1) * (cards-2))),

		# Prob of matching with 3 cards
		count = 0
		for c2 in range(len(d2)):
			d3 = list(d2)
			del d3[c2]
			for c3 in range(len(d3)):
				d4 = list(d3)
				del d4[c3]
				for c4 in range(len(d4)):
					if (card_match(deck[c1], d2[c2])
							or card_match(deck[c1], d3[c3])
							or card_match(deck[c1], d4[c4])):
						count += 1
		print '%0.01f%%' % (100.0 * count / ((cards-1) * (cards-2) * (cards-3)))

def card_match(c1, c2):
	if edge_match(c1[0], c2[0]) or edge_match(c1[0], c2[2]):
		return True
	if edge_match(c1[2], c2[0]) or edge_match(c1[2], c2[2]):
		return True
	if edge_match(c1[1], c2[1]) or edge_match(c1[1], c2[3]):
		return True
	if edge_match(c1[3], c2[1]) or edge_match(c1[3], c2[3]):
		return True
	return False

def edge_match(e1, e2):
	edge = [0, 4, 2, 6, 1, 5, 3, 7]
	return e2 == edge[e1]

for s1 in short_sides:
	for l1 in short_sides:
		for s2 in short_sides:
			for l2 in short_sides:
				card = [s1, l1, s2, l2]
				if validate(card):
					add_card(card)
					print_card(card)

print 'auto-gen cards', valid

print_global_stats()

# process extra cards
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
