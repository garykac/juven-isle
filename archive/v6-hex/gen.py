import sys

# Global count of valid cards
valid = 0

#sides = ['00','02','05','20','25','50','52','55']
sides = ['00','02','20','22']
#sides = ['000','001','011','100','110','111']

#cardtype = 'square' # 'square' or 'hex'
cardtype = 'hex' # 'square' or 'hex'

deck = []

edge_count = {}
for s in sides:
	edge_count[s] = 0

print 'island test (hex with mountains)'

def card2string(card):
	return '-'.join(card)

def card2code(card):
	return ''.join([edge2code(x) for x in card])

def edge2val(edge):
	if len(edge) == 3:
		return int(edge[0])*4 + int(edge[1])*2 + int(edge[2])
	else:
		return int(edge[0])

def edge2code(edge):
	return '%d' % edge2val(edge)
	
def card2val(card):
	if cardtype == 'square':
		return edge2val(card[0])*1000 + edge2val(card[1])*100 + edge2val(card[2])*10 + edge2val(card[3])
	if cardtype == 'hex':
		return edge2val(card[0])*100000 + edge2val(card[1])*10000 + edge2val(card[2])*1000 + edge2val(card[3])*100  + edge2val(card[4])*10  + edge2val(card[5])
	return 0;

def validate(card):
	# Make sure the edges have a valid connection.
	for i in range(len(card)):
		next = i + 1
		if next >= len(card):
			next = 0
		if card[i][-1] != card[next][0]:
			return False

	# Remove symmetry tiles.
	if True:
		val = card2val(card)

		# Square: Remove 90-degree rotation duplicates.
		# Hex: Remove 60-degree rotation duplicates.
		if val > card2val(card[1:] + card[:1]):
			return False

		# Square: Remove 180-degree rotation duplicates.
		# Hex: Remove 120-degree rotation duplicates.
		if val > card2val(card[2:] + card[:2]):
			return False

		# Square: Remove 270-degree rotation duplicates.
		# Hex: Remove 180-degree rotation duplicates.
		if val > card2val(card[3:] + card[:3]):
			return False

		if cardtype == 'hex':
			# Remove 240-degree rotation duplicates.
			if val > card2val(card[4:] + card[:4]):
				return False

			# Remove 300-degree rotation duplicates.
			if val > card2val(card[5:] + card[:5]):
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
				if cardtype == 'square':
					card = [s1, l1, s2, l2]
					if validate(card):
						print_card(card)
						add_card(card)
				elif cardtype == 'hex':
					for s3 in sides:
						for l3 in sides:
							card = [s1, l1, s2, l2, s3, l3]
							if validate(card):
								print_card(card)
								add_card(card)

print 'auto-gen cards', valid

print
print 'Edge counts'
for k in sorted(edge_count.keys()):
	print k, edge_count[k]
	
