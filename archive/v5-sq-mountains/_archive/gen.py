import sys

# Global count of valid cards
valid = 0

#sides = ['000','001','011','012','100','110','111','112','210','211','222']
sides = ['000','011','012','110','111','112','210','211','222']

# Which topo lines occur on each edge.
# shoreline, med, high, mountain-line, med, high
topo_info = {
	'000': [0,0,0,0,0,0],
	'011': [1,1,0,0,0,0],
	'012': [1,1,1,1,1,0],
	'110': [1,1,0,0,0,0],
	'111': [0,0,1,0,0,0],
	'112': [0,0,1,1,1,0],
	'210': [1,1,1,1,1,0],
	'211': [0,0,1,1,1,0],
	'222': [0,0,0,0,0,1],
}
num_topo_lines = 6

# cards to ignore (don't auto-gen)
bad_cards = {
	'@@@@': 'All water. Not useful for generating islands',
}

deck = []

card_type_count = {
	'@@dL': 3, # 000.000.011.110
	'@@eu': 3, # 000.000.012.210
	'@dNu': 3, # 000.011.112.210
	'@evL': 3, # 000.012.211.110
	'dLdL': 3, # 011.110.011.110
	'dLeu': 3, # 011.110.012.210
	'dmmL': 3, # 011.111.111.110
	'dNvL': 3, # 011.112.211.110
	'eueu': 3, # 012.210.012.210
	'evNu': 3, # 012.211.112.210
	'ezzu': 3, # 012.222.222.210
	'mmmm': 2, # 111.111.111.111
	'mmNv': 3, # 111.111.112.211
	'NvNv': 3, # 112.211.112.211
	'Nzzv': 3, # 112.222.222.211
	'zzzz': 2, # 222.222.222.222
}

edge_count = {}
for s in sides:
	edge_count[s] = 0

print 'island test (with mountains)'

def card2string(card):
	return '-'.join(card)

def card2code(card):
	return ''.join([edge2code(x) for x in card])

def edge2val(edge):
	return int(edge[0])*9 + int(edge[1])*3 + int(edge[2])

codes = '@abcdefghijkLmNopqrstuvwxyz'
def edge2code(edge):
	return codes[edge2val(edge)]
	
def card2val(card):
	return edge2val(card[0])*2700 + edge2val(card[1])*900 + edge2val(card[2])*30 + edge2val(card[3])

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

	# Make sure topo lines match (# incoming == # outgoing)
	topo_count = [0] * num_topo_lines
	for i in range(len(card)):
		topo = topo_info[card[i]]
		for j in xrange(num_topo_lines):
			topo_count[j] += topo[j]
	for j in xrange(num_topo_lines):
		if topo_count[j] % 2 != 0:
			#print card, topo_count
			return False

	return True

def add_card(card):
	global valid
	valid += 1

	deck.append(card)
	
	for i in range(len(card)):
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
