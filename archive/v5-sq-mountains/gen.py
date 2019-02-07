import sys

# Global count of valid cards
valid = 0

sides = ['00','02','05','20','25','50','52','55']

# cards to ignore (don't auto-gen)
bad_cards = {
	'00.00.00.00': 'All water. Not useful for generating islands',
	'02.23.32.20': 3, # 011.111.111.110  L2
	'05.56.65.50': 3, # 012.222.222.210  L3
	'23.32.23.32': 3, # 111.111.111.111  L2
	'23.32.25.52': 3, # 111.111.112.211  L2
	'55.55.56.65': 'topo lines must go down from 55 edge',
	'25.56.65.52': 3, # 112.222.222.211  L3
	'56.65.56.65': 3, # 222.222.222.222  L3
}

deck = []

card_type_count = {
	'00.00.02.20': 3, # 000.000.011.110  L1
	'00.00.05.50': 3, # 000.000.012.210  L1
	'00.02.25.50': 3, # 000.011.112.210  L1
	'00.05.52.20': 3, # 000.012.211.110  L1
	'00.05.55.50': 3,
	'02.20.02.20': 3, # 011.110.011.110  L1
	'02.20.05.50': 3, # 011.110.012.210  L2
	'02.25.52.20': 3, # 011.112.211.110  L2
	'02.25.55.50': 3,
	'05.50.05.50': 3, # 012.210.012.210  L3
	'05.52.25.50': 3, # 012.211.112.210  L3
	'05.55.52.20': 3,
	'05.55.55.50': 3,
	'25.52.25.52': 3, # 112.211.112.211  L2
	'25.55.55.52': 3,
	'55.55.55.55': 3,
}

"""
Card edge links:
      00  02  05  20  23  25  32  50  52  56  65
  00   2   2   2   2       1       2   1              L1
  02   2   1   1   5   1   2   1   2   1              L1
  05   2   1   1   2       1       5   2   1   1      L1/3
  20   2   5   2   1   1   1   1   1   2              L1
  23       1       1   1   1   3       1              L2
  25   1   2   1   1   1   1   1   2   5   1   1      L2/3
  32       1       1   3   1   1       1              L2
  50   2   2   5   1       2       1   1   1   1      L1/3
  52   1   1   2   2   1   5   1   1   1   1   1      L2/3
  56           1           1       1   1   1   3      L3
  65           1           1       1   1   3   1      L3
"""

edge_count = {}
for s in sides:
	edge_count[s] = 0

print 'island test (with mountains)'

def card2string(card):
	return '-'.join(card)

def card2code(card):
	return '.'.join([edge2code(x) for x in card])

def edge2val(edge):
	return int(edge[0])*10 + int(edge[1])

def edge2code(edge):
	return '%02d' % edge2val(edge)
	
def card2val(card):
	return edge2val(card[0])*1000000 + edge2val(card[1])*10000 + edge2val(card[2])*100 + edge2val(card[3])

def validate(card):
	# Make sure the edges have a valid connection.
	for i in range(len(card)):
		next = i + 1
		if next >= len(card):
			next = 0
		if card[i][-1] != card[next][0]:
			return False

	if card2code(card) in bad_cards:
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
	
	#print 'adding card', card
	for i in range(len(card)):
		#print '  inc edge', card[i]
		edge_count[card[i]] += 1

def print_card(card):
	out = '.'.join(card)
	code = card2code(card)
	print '%s - %s' % (code, out)

for s1 in sides:
	for l1 in sides:
		for s2 in sides:
			for l2 in sides:
				card = [s1, l1, s2, l2]
				if validate(card):
					print_card(card)
					for i in range(card_type_count[card2code(card)]):
						add_card(card)

print 'auto-gen cards', valid

print
print 'Edge counts'
for k in sorted(edge_count.keys()):
	print k, edge_count[k]
	
	
def print_gen_select_header(nselect, ntypes, allowWild):
	print
	print ntypes, 'different cards, select', nselect,
	if allowWild:
		print 'with wilds'
	else:
		print 'no wilds'

def gen_select_2(ntypes, allowWild=False):
	print_gen_select_header(2, ntypes, allowWild)		
	cards = []
	for i in xrange(0, ntypes):
		for j in xrange(0, ntypes):
			cards.append([i, j])
	print_summary(cards, ntypes, allowWild)
	
def gen_select_3(ntypes, allowWild=False):
	print_gen_select_header(3, ntypes, allowWild)		
	cards = []
	for i in xrange(0, ntypes):
		for j in xrange(0, ntypes):
			for k in xrange(0, ntypes):
				cards.append([i, j, k])
	print_summary(cards, ntypes, allowWild)
	
def gen_select_4(ntypes, allowWild=False):
	print_gen_select_header(4, ntypes, allowWild)		
	cards = []
	for i1 in xrange(0, ntypes):
		for i2 in xrange(0, ntypes):
			for i3 in xrange(0, ntypes):
				for i4 in xrange(0, ntypes):
					cards.append([i1, i2, i3, i4])
	print_summary(cards, ntypes, allowWild)

def gen_select_5(ntypes, allowWild=False):
	print_gen_select_header(5, ntypes, allowWild)		
	cards = []
	for i1 in xrange(0, ntypes):
		for i2 in xrange(0, ntypes):
			for i3 in xrange(0, ntypes):
				for i4 in xrange(0, ntypes):
					for i5 in xrange(0, ntypes):
						cards.append([i1, i2, i3, i4, i5])
	print_summary(cards, ntypes, allowWild)

# cards is the array of cards
# ntypes is the number of different card types
# allowWild means interpret cardtype 0 as wild	
def print_summary(cards, ntypes, allowWild):
	s = {}
	for card in cards:
		#print card
		# Note: counts[0] is not used.
		counts = [0] * 8
		for t in xrange(ntypes):
			count = 0
			wilds = 0
			for v in card:
				if allowWild:
					if v == 0:
						wilds += 1
					elif v == t:
						count += 1
				elif v == t:
					count += 1
			#print count, 'cards with value', t
			if count != 0:
				counts[count] += 1
		if allowWild and wilds != 0:
			#print counts
			#print 'wilds', wilds
			# Adjust counts with wild
			i = len(counts) - 1
			found = False
			while i >= 0 and not found:
				if counts[i] > 0:
					counts[i] -= 1
					counts[i + wilds] = 1
					found = True
				i -= 1
			if not found:
				# all wildcards
				counts[0] = 1
			#print counts
		key = '-'.join([str(x) for x in counts])
		if not key in s:
			s[key] = 0
		s[key] += 1
	
	# Assumes all cards are equal prob
	desc = ['all wilds', 'singles', 'doubles', 'triples', 'quadruples', 'quintuples']
	for k in s.keys():
		m = k.split('-')
		print '%5.2f%% with' % (100.0 * float(s[k]) / len(cards)),
		for i in xrange(len(m)):
			if m[i] != '0':
				print m[i], desc[i],
		print
	
def gen_probs():
	print
	print 'probs'

	#gen_select_2(3)
	#gen_select_2(3, True)
	gen_select_2(4, True)

	#gen_select_3(3)
	#gen_select_3(3, True)
	gen_select_3(4, True)

	#gen_select_4(3)
	#gen_select_4(4)
	gen_select_4(4, True)

	gen_select_5(4, True)
	
gen_probs()
